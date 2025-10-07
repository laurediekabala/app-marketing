# pages/prediction.py
import dash
from dash import dcc, html, callback, Input, Output, State
from dash.exceptions import PreventUpdate 
import dash_bootstrap_components as dbc
import requests # Pour appeler l'API Flask
import json
import plotly.graph_objects as go

# URL de votre API Flask (à adapter)
FLASK_API_URL = "http://api_flask:5000/predict"
# Exemple de formulaire basé sur les colonnes du dataset
# Dans une vraie application, cela pourrait être plus dynamique
JOB_OPTIONS = ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 
               'retired', 'self-employed', 'services', 'student', 'technician', 
               'unemployed', 'unknown']

MARITAL_OPTIONS = ['divorced', 'married', 'single', 'unknown']

EDUCATION_OPTIONS = ['primary', 'secondary', 'tertiary', 'unknown']

CONTACT_OPTIONS = ['cellular', 'telephone', 'unknown']

MONTH_OPTIONS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

POUTCOME_OPTIONS = ['failure', 'success', 'other', 'unknown']

YES_NO_OPTIONS = ['yes', 'no']
FORM_LABEL_STYLE = {
    "width": "100%",
    "margin-bottom": "0px",
    "padding": "6px"
}

INPUT_STYLE = {
    "width": "100%",
    "height": "38px",
    "padding": "6px 12px",
    "fontSize": "16px",
    "border": "1px solid #ced4da",
    "borderRadius": "4px"
}

DROPDOWN_STYLE = {
    "width": "100%",
    "height": "38px"
}

form_inputs = dbc.Row([
    # Première colonne - Informations personnelles
    dbc.Col([
        html.H5("Informations personnelles", className="mb-3"),
        dbc.Row([
            dbc.Col(dbc.Label("Âge", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-age',
                type='number',
                value=40,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Emploi", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-job',
                options=[{'label': job, 'value': job} for job in JOB_OPTIONS],
                value='admin.',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Statut Marital", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-marital',
                options=[{'label': m, 'value': m} for m in MARITAL_OPTIONS],
                value='married',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Education", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-education',
                options=[{'label': e, 'value': e} for e in EDUCATION_OPTIONS],
                value='secondary',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
    ], md=4),

    # Deuxième colonne - Informations financières
    dbc.Col([
        html.H5("Informations financières", className="mb-3"),
        dbc.Row([
            dbc.Col(dbc.Label("Défaut", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-default',
                options=[{'label': yn, 'value': yn} for yn in YES_NO_OPTIONS],
                value='no',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Solde", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-balance',
                type='number',
                value=0,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Prêt immobilier", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-housing',
                options=[{'label': yn, 'value': yn} for yn in YES_NO_OPTIONS],
                value='no',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Prêt personnel", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-loan',
                options=[{'label': yn, 'value': yn} for yn in YES_NO_OPTIONS],
                value='no',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
    ], md=4),

    # Troisième colonne - Informations campagne
    dbc.Col([
        html.H5("Informations campagne", className="mb-3"),
        dbc.Row([
            dbc.Col(dbc.Label("Contact", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-contact',
                options=[{'label': c, 'value': c} for c in CONTACT_OPTIONS],
                value='cellular',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Jour", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-day',
                type='number',
                min=1,
                max=31,
                value=1,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Mois", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-month',
                options=[{'label': m, 'value': m} for m in MONTH_OPTIONS],
                value='may',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Durée (sec)", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-duration',
                type='number',
                value=0,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Nb contacts", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-campaign',
                type='number',
                value=1,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Jours passés", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-pdays',
                type='number',
                value=-1,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Précédents", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Input(
                id='pred-previous',
                type='number',
                value=0,
                style=INPUT_STYLE
            ), width=8),
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col(dbc.Label("Résultat préc.", style=FORM_LABEL_STYLE), width=4),
            dbc.Col(dcc.Dropdown(
                id='pred-poutcome',
                options=[{'label': p, 'value': p} for p in POUTCOME_OPTIONS],
                value='unknown',
                style=DROPDOWN_STYLE
            ), width=8),
        ], className="mb-3"),
    ], md=4),
], className="mb-4 g-3")
# Mise à jour de la fonction layout pour inclure le bouton de prédiction
def layout():
    return dbc.Container([
        html.H1("Prédiction de Souscription"),
        html.P("Remplissez les informations du client pour obtenir une prédiction."),
        html.Hr(),
        form_inputs,
        dbc.Row([
            dbc.Col(
                dbc.Button("Prédire", id="predict-button", color="primary", size="lg", className="w-100"),
                className="mb-4"
            )
        ]),
        dbc.Row([
            dbc.Col([
                html.H4("Résultat de la Prédiction"),
                dcc.Loading(
                    id="loading-prediction",
                    type="circle",
                    children=html.Div(id="prediction-output")
                ),
                html.Hr(),
                html.H4("Explication de la Prédiction (SHAP)"),
                dcc.Loading(
                    id="loading-shap",
                    type="circle",
                    children=html.Div(id="shap-output")
                )
            ])
        ])
    ], fluid=True, className="py-4")


@callback(
    Output('prediction-output', 'children'),
    Output('shap-output', 'children'),
    Input('predict-button', 'n_clicks'),
    [State('pred-age', 'value'),
     State('pred-job', 'value'),
     State('pred-marital', 'value'),
     State('pred-education', 'value'),
     State('pred-default', 'value'),
     State('pred-balance', 'value'),
     State('pred-housing', 'value'),
     State('pred-loan', 'value'),
     State('pred-contact', 'value'),
     State('pred-day', 'value'),
     State('pred-month', 'value'),
     State('pred-duration', 'value'),
     State('pred-campaign', 'value'),
     State('pred-pdays', 'value'),
     State('pred-previous', 'value'),
     State('pred-poutcome', 'value')]
)
def update_prediction(n_clicks, age, job, marital, education, default, balance,
                     housing, loan, contact, day, month, duration, campaign,
                     pdays, previous, poutcome):
    if n_clicks is None:
        raise PreventUpdate

    # Construction du dictionnaire des données
    input_data = {
        'age': age,
        'job': job,
        'marital': marital,
        'education': education,
        'default': default,
        'balance': balance,
        'housing': housing,
        'loan': loan,
        'contact': contact,
        'day': day,
        'month': month,
        'duration': duration,
        'campaign': campaign,
        'pdays': pdays,
        'previous': previous,
        'poutcome': poutcome
    }

    try:
        response = requests.post(
            FLASK_API_URL,
            json=input_data,  # Utilisation directe du dictionnaire
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        response.raise_for_status()
        result = response.json()

        if result['status'] == 'success':
            prediction = result['prediction']
            probability = result['probability']
            
            # Création de la carte de prédiction
            prediction_card = dbc.Card([
                dbc.CardHeader(html.H4("Résultat", className="text-center")),
                dbc.CardBody([
                    html.H5(
                        "Client susceptible de souscrire ✅" if prediction == 1 
                        else "Client peu susceptible de souscrire ❌",
                        className="text-center mb-3",
                        style={'color': 'green' if prediction == 1 else 'red'}
                    ),
                    html.H6(
                        f"Probabilité de souscription : {probability:.2%}",
                        className="text-center"
                    )
                ])
            ], className="mb-4")

            # Le reste du code pour SHAP reste inchangé...
            shap_values = result.get('shap_values', {})
            
            if shap_values:
                   # Dans la fonction update_prediction, remplacez la section "if shap_values:" par :
                colors = ['#ff4d4d' if val > 0 else '#2e86c1' for val in shap_values['values']]
                
                fig = go.Figure(go.Bar(
                    x=shap_values['values'],
                    y=shap_values['features'],
                    orientation='h',
                    marker_color=colors
                ))
                
                fig.update_layout(
                    title="Impact des variables sur la prédiction",
                    xaxis_title="Impact SHAP (négatif = diminue la probabilité, positif = augmente)",
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    showlegend=False,
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                shap_explanation = dbc.Card([
                    dbc.CardHeader(html.H4("Explication de la décision", className="text-center")),
                    dbc.CardBody([
                        html.P([
                            "Les barres ", 
                            html.Span("rouges", style={'color': '#ff4d4d'}),
                            " augmentent la probabilité de souscription, les barres ",
                            html.Span("bleues", style={'color': '#2e86c1'}),
                            " la diminuent."
                        ]),
                        dcc.Graph(figure=fig)
                    ])
                ], className="mt-4")
                
                return prediction_card, shap_explanation
                 
            return prediction_card, "Pas d'explication SHAP disponible"
            
        else:
            return dbc.Alert(
                "Erreur lors de la prédiction: " + result.get('error', 'Erreur inconnue'),
                color="danger"
            ), None

    except Exception as e:
        return dbc.Alert(
            f"Une erreur est survenue: {str(e)}",
            color="danger"
        ), None


        
       
         
        