# index.py
import dash
from dash import dcc, html, Input, Output, State
from dash.dependencies import ClientsideFunction
import dash_bootstrap_components as dbc
from flask_login import current_user, logout_user, login_user
import os
from app import app, login_manager
from user import User
from supabase_db import get_user_by_id, validate_user
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
        return User(
            user_id=db_user['id'], 
            email=db_user['email'],
            username=db_user['username'], 
            role=db_user['role']
        )
    return None

# Layout principal de l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='theme-store', storage_type='local', data='light'),
    html.Div(id='page-container')
])

# Callback pour gérer la logique de connexion
@app.callback(
    [Output('url', 'pathname', allow_duplicate=True), 
     Output('login-error', 'children')],
    Input('login-button', 'n_clicks'),
    [State('email-input', 'value'), 
     State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not email or not password:
        return dash.no_update, html.Span("⚠️ Veuillez entrer votre email et mot de passe.", className="text-warning")
    
    user_data = validate_user(email, password)
    if user_data:
        user = User(
            user_id=user_data['id'], 
            email=user_data['email'],
            username=user_data['username'], 
            role=user_data['role']
        )
        login_user(user)
        return '/', html.Span("✅ Connexion réussie! Redirection en cours...", className="text-success")
    else:
        return dash.no_update, html.Span("❌ Email ou mot de passe incorrect.", className="text-danger")

# Callback côté client pour le changement de thème
app.clientside_callback(
    """
    function(theme_switch_value) {
        return window.dash_clientside.clientside.update_theme_styles(theme_switch_value);
    }
    """,
    Output('theme-store', 'data', allow_duplicate=True),
    Input('theme-switch', 'value'),
    prevent_initial_call='initial_duplicate'
)

# Callback pour effacer les erreurs lors de la saisie
@app.callback(
    Output('login-error', 'children', allow_duplicate=True),
    [Input('email-input', 'value'),
     Input('password-input', 'value')],
    prevent_initial_call=True
)
def clear_login_error(email, password):
    """Efface les messages d'erreur lors de la saisie"""
    return ""

# Callback principal pour afficher la bonne page et gérer les accès
@app.callback(
    Output('page-container', 'children'),
    [Input('url', 'pathname'),
     Input('theme-store', 'data')]
)
def display_page(pathname, theme_value):
    try:
        # Gestion des utilisateurs non authentifiés
        if not current_user.is_authenticated:
            if pathname == '/logout':
                return dcc.Location(id='redirect-to-login', pathname='/')
            return html.Div([
                login_layout()
            ], style={
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", 
                "min-height": "100vh"
            })

        # Gestion de la déconnexion
        if pathname == '/logout':
            logout_user()
            return dcc.Location(id='redirect-after-logout', pathname='/')

        # Vérification des permissions utilisateur
        user_role = current_user.role
        allowed_pages = {
            'admin': ['/', '/analyse', '/prediction', '/gestion'],
            'user': ['/', '/analyse', '/prediction'],
            'analyste': ['/', '/analyse', '/prediction']
        }

        # Redirection si accès non autorisé
        if pathname not in allowed_pages.get(user_role, ['/']):
            return html.Div([
                sidebar_layout(),
                html.Div([
                    dbc.Container([
                        dbc.Alert([
                            html.H4("🚫 Accès non autorisé", className="alert-heading"),
                            html.P(f"Votre rôle ({user_role}) ne vous permet pas d'accéder à cette page."),
                            html.Hr(),
                            dbc.Button("Retour à l'accueil", href="/", color="primary")
                        ], color="warning")
                    ])
                ], id='page-content', style=CONTENT_STYLE)
            ])

        # Sélection du contenu selon la page
        content = None
        page_title = ""
        
        if pathname == '/':
            content = home_layout()
            page_title = "Accueil"
        elif pathname == '/analyse':
            content = analyse_layout()
            page_title = "Analyse des données"
        elif pathname == '/prediction':
            content = prediction_layout()
            page_title = "Prédiction"
        elif pathname == '/gestion':
            content = manage_users_layout()
            page_title = "Gestion des utilisateurs"
        else:
            # Page non trouvée
            content = html.Div([
                dbc.Container([
                    dbc.Alert([
                        html.H4("🔍 Page non trouvée", className="alert-heading"),
                        html.P("La page que vous recherchez n'existe pas."),
                        html.Hr(),
                        dbc.Button("Retour à l'accueil", href="/", color="primary")
                    ], color="warning")
                ])
            ])
            page_title = "Erreur 404"

        if content is None:
            raise ValueError(f"Aucun contenu trouvé pour le chemin : {pathname}")

        # Construction du layout final avec sidebar et contenu
        return html.Div([
            # Sidebar
            sidebar_layout(),
            
            # Zone de contenu principal
            html.Div([
                # Header de la page CORRIGÉ avec syntaxe breadcrumb correcte
                html.Div([
                    # Breadcrumb seulement si ce n'est pas l'accueil
                    html.Div([
                        dbc.Breadcrumb(
                            items=[
                                {"label": "🏠 Accueil", "href": "/"},
                                {"label": page_title, "active": True}
                            ],
                            className="mb-3"
                        )
                    ] if pathname != "/" else []),
                    
                    # Titre et info utilisateur
                    html.Div([
                        html.H1(page_title, className="display-6 mb-0"),
                        html.P([
                            f"Bienvenue, ",
                            html.Strong(f"{current_user.username}", className="text-primary"),
                            f" • {current_user.role.upper()}"
                        ], className="text-muted mb-0")
                    ], className="d-flex justify-content-between align-items-center mb-4")
                ], className="mb-4"),
                
                # Contenu de la page
                html.Div(content, className="content-area")
                
            ], id='page-content', style=CONTENT_STYLE),
            
        ], className="app-container")

    except Exception as e:
        print(f"❌ Erreur dans display_page: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return html.Div([
            sidebar_layout() if current_user.is_authenticated else html.Div(),
            html.Div([
                dbc.Container([
                    dbc.Alert([
                        html.H4("⚠️ Une erreur est survenue", className="alert-heading"),
                        html.P("Nous nous excusons pour la gêne occasionnée."),
                        html.Hr(),
                        html.P([
                            "Détails de l'erreur : ",
                            html.Code(str(e))
                        ], className="mb-0"),
                        dbc.Button("Retour à l'accueil", href="/", color="primary", className="mt-3")
                    ], color="danger")
                ])
            ], id='page-content', style=CONTENT_STYLE if current_user.is_authenticated else {"padding": "2rem"})
        ])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
    