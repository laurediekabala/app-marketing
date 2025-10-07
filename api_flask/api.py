from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import shap
from sklearn.pipeline import Pipeline
import logging
import os
from scipy import sparse 
# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Chargement du modèle
MODEL_PATH =  os.path.join(os.getcwd(), "xboost.joblib")
THRESHOLD = 0.45

def get_feature_names_from_pipeline(pipeline, input_data):
    """Récupère les noms des features après transformation par le pipeline"""
    # Applique chaque étape du pipeline sauf la dernière (le modèle)
    temp_pipeline = Pipeline(pipeline.steps[:-1])
    transformed_data = temp_pipeline.transform(input_data)
    # Tente de récupérer les noms des features
    if hasattr(temp_pipeline, 'get_feature_names_out'):
        return temp_pipeline.get_feature_names_out()
    return [f"feature_{i}" for i in range(transformed_data.shape[1])]

@app.route('/predict', methods=['POST'])
def predict():
     try:
        # Récupération des données
        data = request.get_json()
        input_df = pd.DataFrame([data])
        logger.info(f"Données reçues : {data}")
        
        # Chargement du pipeline
        pipeline = joblib.load(MODEL_PATH)
        
        # Récupération du modèle XGBoost
        xgb_model = pipeline.named_steps['xgbclassifier']
        
        # Transformation des données
        preprocessor = Pipeline(pipeline.steps[:-1])
        transformed_data = preprocessor.transform(input_df)
        
        # Prédiction
        probability = pipeline.predict_proba(input_df)[0, 1]
        prediction = int(probability >= THRESHOLD)
        
        # Calcul des valeurs SHAP
        explainer = shap.TreeExplainer(xgb_model)
        # Convertir en array numpy si nécessaire
        if sparse.issparse(transformed_data):
            transformed_data = transformed_data.toarray()
        shap_values = explainer.shap_values(transformed_data)
        
        # Récupération des noms des features
        feature_names = get_feature_names_from_pipeline(pipeline, input_df)
        
        # Traitement des valeurs SHAP
        if isinstance(shap_values, list):
            # Pour les modèles de classification binaire
            shap_values = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        
        # S'assurer que shap_values est un tableau 2D
        shap_values = np.atleast_2d(shap_values)
        try:
            # Création de la liste des importances
            feature_importance = list(zip(feature_names, np.abs(shap_values[0])))
            feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
            top_10_features = feature_importance[:10]
            
            # Création du dictionnaire SHAP
            shap_dict = {
                'features': [f[0] for f in top_10_features],
                'values': [float(v) for v in [shap_values[0][list(feature_names).index(f[0])] 
                          for f in top_10_features]],
                'base_value': float(explainer.expected_value if isinstance(explainer.expected_value, float) 
                                  else explainer.expected_value[1] if isinstance(explainer.expected_value, list) 
                                  else explainer.expected_value)
            }
            logger.info("SHAP values calculées avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul SHAP : {str(e)}")
            shap_dict = None
          # Construction de la réponse
        response = {
            'status': 'success',
            'prediction': prediction,
            'probability': float(probability),
            'threshold': THRESHOLD,
        }  
        if shap_dict is not None:
            response['shap_values'] = shap_dict
        
        return jsonify(response)

     except Exception as e:
        logger.error(f"Erreur : {str(e)}")
        # Ajout de plus de détails dans le log
        import traceback
        logger.error(f"Traceback : {traceback.format_exc()}")
        return jsonify({'status': 'error', 'error': str(e)}), 500  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)