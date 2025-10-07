# index.py
import dash
from dash import dcc, html, Input, Output, State
from dash.dependencies import ClientsideFunction
import dash_bootstrap_components as dbc
from flask_login import current_user, logout_user, login_user

from app import app, login_manager
from user import User
from database import get_user_by_id, validate_user
from utils.theme import CONTENT_STYLE

# Import des layouts des pages
from pages.home import layout as home_layout
from pages.analyse import layout as analyse_layout
from pages.prediction import layout as prediction_layout
from pages.login import layout as login_layout
from pages.gestion import layout as manage_users_layout
from components.sidebar import layout as sidebar_layout

# Configuration pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    db_user = get_user_by_id(user_id)
    if db_user:
        # CORRECTION : Le mot de passe n'est nécessaire que pour la validation lors de la connexion.
        # Pour recharger l'utilisateur depuis la session, il n'est plus requis.
        # On passe une chaîne vide pour éviter une erreur si la base de données ne le retourne pas.
        return User(user_id=db_user['id'], username=db_user['username'], password="", role=db_user['role'])
    return None
# Layout principal de l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='theme-store', storage_type='session', data='light'),
    html.Div(id='page-container')
])

# Callback pour gérer la logique de connexion
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True), Output('login-error', 'children')],
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not username or not password:
        return dash.no_update, "Veuillez entrer un nom d'utilisateur et un mot de passe."
    user_data = validate_user(username, password)
    if user_data:
        user = User(user_id=user_data['id'], username=user_data['username'], 
                   password=user_data['password'], role=user_data['role'])
        login_user(user)
        # Modification ici : redirection vers la page d'accueil pour tous les utilisateurs
        return '/', ""
    else:
        return dash.no_update, "Nom d'utilisateur ou mot de passe incorrect."

# Callback côté client pour le changement de thème
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_theme_styles'
    ),
    Output('theme-store', 'data', allow_duplicate=True),
    Input('theme-switch', 'value'),
    prevent_initial_call=True
)

# Callback principal pour afficher la bonne page et gérer les accès
@app.callback(
  Output('page-container', 'children'),
    [Input('url', 'pathname'),
     Input('theme-store', 'data')]
)
def display_page(pathname,theme_value):
    try:
        if not current_user.is_authenticated:
            if pathname == '/logout':
                return dcc.Location(id='redirect-to-login', pathname='/')
            return login_layout()

        if pathname == '/logout':
            logout_user()
            return dcc.Location(id='redirect-after-logout', pathname='/')

        user_role = current_user.role
        allowed_pages = {
            'admin': ['/', '/analyse', '/prediction', '/gestion'],
            'analyste': ['/', '/analyse', '/prediction']
        }

        # Vérification des permissions
        if pathname not in allowed_pages.get(user_role, []):
            default_page = '/' if user_role == 'analyste' else '/'
            return dcc.Location(id='redirect-unauthorized', pathname=default_page)

        # Construction du contenu
        content = None
        if pathname == '/':
            content = home_layout()
        elif pathname == '/analyse':
            content = analyse_layout()
        elif pathname == '/prediction':
            content = prediction_layout()
        elif pathname == '/gestion':
            content = manage_users_layout()
        else:
            return dcc.Location(id='redirect-404', pathname='/')

        if content is None:
            raise ValueError(f"No content found for path: {pathname}")

        # Retour du layout complet
        return html.Div([
            sidebar_layout(),
            html.Div(
                content, 
                id='page-content', 
                style=CONTENT_STYLE
            ),
            html.Div(
                dbc.Button(
                    "Déconnexion", 
                    href="/logout", 
                    color="danger", 
                    outline=True, 
                    className="mt-auto"
                ),
                style={
                    'position': 'fixed',
                    'bottom': '20px',
                    'left': '20px',
                    'width': 'calc(18rem - 40px)'
                }
            )
        ])
    except Exception as e:
        print(f"Error in display_page: {str(e)}")  # Pour le debugging
        return html.Div([
            html.H1("Une erreur est survenue"),
            html.P("Veuillez réessayer ultérieurement.")
        ])

if __name__ == '__main__':
    app.run(debug=True)