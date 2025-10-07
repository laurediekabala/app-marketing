import dash
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user

# Style pour la barre latérale, la couleur sera gérée par le script JS
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa", # Couleur par défaut (thème clair)
    "transition": "background-color 0.3s ease",
}

def layout():
    """
    Crée le layout de la barre latérale de manière dynamique
    en fonction du rôle de l'utilisateur connecté.
    """
    
    nav_links = []
    # Vérifie si un utilisateur est authentifié avant d'accéder à son rôle
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            # L'admin voit tous les liens, y compris la gestion des utilisateurs
            nav_links = [
                dbc.NavLink("Accueil", href="/", active="exact", className="text-decoration-none"),
                dbc.NavLink("Analyse", href="/analyse", active="exact", className="text-decoration-none"),
                dbc.NavLink("Prédiction", href="/prediction", active="exact", className="text-decoration-none"),
                dbc.NavLink("Gérer les utilisateurs", href="/gestion", active="exact", className="text-decoration-none"),
            ]
        elif current_user.role == 'analyste':
            # L'analyste ne voit que le lien vers la page de prédiction
            nav_links = [
                dbc.NavLink("Prédiction", href="/prediction", active="exact", className="text-decoration-none"),
            ]

    return html.Div(
        [
            html.H2("BankPredict", className="display-6 fw-bold"),
            html.Hr(),
            html.P(
                "Menu de navigation", className="lead"
            ),
            dbc.Nav(
                nav_links,
                vertical=True,
                pills=True,
            ),
            html.Hr(className="mt-5"),
            dbc.Label("Thème"),
            dbc.Checklist(
                options=[{"label": "Sombre", "value": 1}],
                value=[],
                id="theme-switch",
                switch=True,
            ),
        ],
        id="sidebar", # ID crucial pour le script de thème
        style=SIDEBAR_STYLE,
    )