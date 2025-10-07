# app.py
import dash
import dash_bootstrap_components as dbc
import os
from flask_login import LoginManager

# Initialise l'application Dash
app = dash.Dash(__name__, 
                suppress_callback_exceptions=True, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
               )

# Récupération du serveur Flask sous-jacent
server = app.server

# Configuration du serveur pour Flask-Login
server.config.update(
    SECRET_KEY=os.urandom(24), # Clé secrète pour la gestion des sessions
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# Initialisation de LoginManager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login' # Redirige les utilisateurs non connectés vers cette page

