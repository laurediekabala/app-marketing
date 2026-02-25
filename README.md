📊 Application Dash – Analyse et Prédiction de Souscription à une Offre Bancaire

🏦 Contexte du projet

Dans un contexte de campagnes marketing bancaires, il est stratégique pour une banque d’identifier à l’avance :

les clients susceptibles de souscrire à une nouvelle offre,

et ceux qui ne vont probablement pas souscrire.

Ce projet repose sur le jeu de données d’une banque portugaise, largement utilisé dans les études de marketing bancaire, et vise à aider la banque à optimiser ses futures campagnes en ciblant efficacement les bons profils clients.

🎯 Objectifs de l’application

L’application a pour objectif principal :

d’analyser les caractéristiques des clients afin de comprendre les différences entre :

les clients qui souscrivent à l’offre,

et ceux qui ne souscrivent pas ;

de prédire la probabilité de souscription lors d’une prochaine campagne marketing ;

d’expliquer les décisions du modèle de Machine Learning afin de garantir la transparence et l’interprétabilité.

🧠 Approche méthodologique

Le projet s’articule autour de trois axes majeurs :

1️⃣ Analyse exploratoire et descriptive

Étude des variables socio-démographiques et comportementales

Comparaison des profils des clients souscripteurs vs non-souscripteurs

Visualisations interactives via Dash

2️⃣ Statistique inférentielle

Tests statistiques pour vérifier l’existence de différences significatives entre les deux groupes

Analyse de la dépendance entre les variables explicatives et la souscription

3️⃣ Machine Learning et interprétabilité

Modélisation avec XGBoost

Estimation de la probabilité de souscription

Interprétation des prédictions à l’aide de SHAP pour expliquer :

les variables les plus influentes,

le raisonnement du modèle pour chaque client.

2️⃣ Statistique inférentielle

Tests statistiques pour vérifier l’existence de différences significatives entre les deux groupes

Analyse de la dépendance entre les variables explicatives et la souscription

3️⃣ Machine Learning et interprétabilité

Modélisation avec XGBoost

Estimation de la probabilité de souscription

Interprétation des prédictions à l’aide de SHAP pour expliquer :

les variables les plus influentes,

le raisonnement du modèle pour chaque client. 

🧩 Architecture de l’application

L’application suit une architecture modulaire et professionnelle, orientée production.

🔐 Authentification

Page Login

Accès réservé aux utilisateurs authentifiés

En cas d’absence de compte, l’utilisateur doit contacter l’administrateur

Gestion des rôles (utilisateur / administrateur)

🏠 Pages principales

Page Accueil

Présentation générale de l’application

Page Analyse

Analyse des données et statistiques

Page Prédiction (Machine Learning)

Prédictions et explications SHAP

Page Gestion (Administrateur uniquement)

Gestion des accès et des utilisateurs

🏗️ Architecture technique
🔧 Technologies utilisées

Langage : Python

Frontend : Dash

Backend (API ML) : Flask

Modèle de Machine Learning : XGBoost

Interprétabilité : SHAP

Visualisation : Plotly, Matplotlib

Déploiement : Render (API Flask & Dash)

🔄 Séparation des responsabilités

Application Dash

Interfaces utilisateurs

Visualisation

Interaction avec l’API

API Flask

Chargement du modèle XGBoost

Prédictions

Calcul des explications SHAP

Cette séparation garantit :

une meilleure scalabilité,

une maintenance simplifiée,

une architecture conforme aux bonnes pratiques MLOps.

🚀 Valeur ajoutée pour la banque

Meilleure ciblage des campagnes marketing

Réduction des coûts liés aux campagnes inefficaces

Décisions basées sur les données et les probabilités

Transparence grâce à l’interprétabilité des modèles

📌 Conclusion

Cette application constitue un outil décisionnel complet, combinant :

analyse statistique,

machine learning avancé,

interprétabilité des modèles,

et interfaces interactives professionnelles.

Elle permet à la banque d’anticiper le comportement de ses clients et d’améliorer significativement la performance de ses campagnes marketing futures.
.
├── index.py               # Point d'entrée principal (Gestion du routage)
├── app.py                 # Initialisation de l'application Dash
├── supabase_db.py         # Intégration et requêtes vers Supabase
├── transformation.py      # Scripts de nettoyage et processing
├── requirements.txt       # Dépendances de l'application
├── api_flask/             # Backend de service ML
│   ├── api.py             # API Flask servant le modèle XGBoost
│   └── requirement.txt    # Dépendances spécifiques à l'API
├── pages/                 # Modules de contenu
│   ├── login.py           # Authentification sécurisée
│   ├── home.py            # Page d'accueil
│   ├── analyse.py         # Analyse statistique et inférentielle
│   └── prediction.py      # Interface de prédiction (XGBoost + SHAP)
├── component/             # Éléments d'interface réutilisables
│   └── sidebar.py         # Menu latéral de navigation
├── utils/                 # Fonctions utilitaires
│   ├── theme.py           # Configuration visuelle et CSS-in-JS
│   └── traitement.py      # Fonctions de traitement transverses
├── dataset/               # Répertoire des données sources
├── assets/                # Logos, CSS personnalisés et images
└── email_config           # Configuration des services d'emailing