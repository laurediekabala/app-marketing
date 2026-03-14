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

from pages.home import layout as home_layout
from pages.analyse import layout as analyse_layout
from pages.prediction import layout as prediction_layout
from pages.login import layout as login_layout
from pages.gestion import layout as manage_users_layout
from components.sidebar import layout as sidebar_layout


@login_manager.user_loader
def load_user(user_id):
    db_user = get_user_by_id(user_id)
    if db_user:
        return User(
            user_id=db_user['id'], email=db_user['email'],
            username=db_user['username'], role=db_user['role']
        )
    return None


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='theme-store', storage_type='local', data='light'),
    html.Div(id='page-container')
])


@app.callback(
    [Output('url', 'pathname', allow_duplicate=True),
     Output('login-error', 'children')],
    Input('login-button', 'n_clicks'),
    [State('email-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not email or not password:
        return dash.no_update, html.Span(
            "⚠️ Veuillez entrer votre email et mot de passe.",
            className="text-warning"
        )
    user_data = validate_user(email, password)
    if user_data:
        user = User(
            user_id=user_data['id'], email=user_data['email'],
            username=user_data['username'], role=user_data['role']
        )
        login_user(user)
        return '/', html.Span("✅ Connexion réussie!", className="text-success")
    else:
        return dash.no_update, html.Span(
            "❌ Email ou mot de passe incorrect.", className="text-danger"
        )


app.clientside_callback(
    """
    function(v) {
        return window.dash_clientside.clientside.update_theme_styles(v);
    }
    """,
    Output('theme-store', 'data', allow_duplicate=True),
    Input('theme-switch', 'value'),
    prevent_initial_call='initial_duplicate'
)


@app.callback(
    Output('login-error', 'children', allow_duplicate=True),
    [Input('email-input', 'value'), Input('password-input', 'value')],
    prevent_initial_call=True
)
def clear_login_error(email, password):
    return ""


@app.callback(
    Output('page-container', 'children'),
    [Input('url', 'pathname'), Input('theme-store', 'data')]
)
def display_page(pathname, theme_value):
    try:
        if not current_user.is_authenticated:
            if pathname == '/logout':
                return dcc.Location(id='redirect-to-login', pathname='/')
            return html.Div([
                login_layout()
            ], className="login-container", style={
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "minHeight": "100vh"
            })

        if pathname == '/logout':
            logout_user()
            return dcc.Location(id='redirect-after-logout', pathname='/')

        user_role = current_user.role
        allowed = {
            'admin': ['/', '/analyse', '/prediction', '/gestion'],
            'user': ['/', '/analyse', '/prediction'],
            'analyste': ['/', '/analyse', '/prediction']
        }

        if pathname not in allowed.get(user_role, ['/']):
            return html.Div([
                sidebar_layout(),
                html.Div([
                    dbc.Container([
                        dbc.Alert([
                            html.H4("🚫 Accès non autorisé", className="alert-heading"),
                            html.P(f"Votre rôle ({user_role}) ne permet pas cet accès."),
                            html.Hr(),
                            dbc.Button([
                                html.I(className="fas fa-home me-2"), "Accueil"
                            ], href="/", color="primary", className="mt-2")
                        ], color="warning", className="shadow-sm")
                    ], fluid=True, className="py-3")
                ], id='page-content', className="content-container", style=CONTENT_STYLE)
            ], className="app-container")

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
            content = dbc.Container([
                dbc.Alert([
                    html.H4("🔍 Page non trouvée"),
                    html.P("Cette page n'existe pas."),
                    html.Hr(),
                    dbc.Button([
                        html.I(className="fas fa-home me-2"), "Accueil"
                    ], href="/", color="primary")
                ], color="warning", className="shadow-sm")
            ], fluid=True)
            page_title = "Erreur 404"

        if content is None:
            raise ValueError(f"Aucun contenu pour : {pathname}")

        return html.Div([
            sidebar_layout(),
            html.Div([
                # Header
                html.Div([
                    # Breadcrumb
                    html.Div([
                        dbc.Breadcrumb(
                            items=[
                                {"label": "🏠 Accueil", "href": "/"},
                                {"label": page_title, "active": True}
                            ], className="mb-2"
                        )
                    ] if pathname != "/" else []),
                    # Titre + User
                    html.Div([
                        html.Div([
                            html.H1(page_title, className="display-6 mb-0 fw-bold"),
                        ]),
                        html.Div([
                            html.P([
                                "Bienvenue, ",
                                html.Strong(current_user.username, className="text-primary"),
                                html.Span(
                                    f" • {current_user.role.upper()}",
                                    className="d-none d-sm-inline"
                                )
                            ], className="text-muted mb-0 user-greeting")
                        ])
                    ], className="header-flex mb-3"),
                ], className="page-header mb-3"),
                # Contenu
                html.Div(content, className="content-area")
            ], id='page-content', className="content-container", style=CONTENT_STYLE),
        ], className="app-container")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return html.Div([
            sidebar_layout() if current_user.is_authenticated else html.Div(),
            html.Div([
                dbc.Container([
                    dbc.Alert([
                        html.H4("⚠️ Erreur"),
                        html.P("Une erreur est survenue."),
                        html.Hr(),
                        html.Code(str(e), className="d-block text-break small"),
                        dbc.Button([
                            html.I(className="fas fa-home me-2"), "Accueil"
                        ], href="/", color="primary", className="mt-3")
                    ], color="danger", className="shadow-sm")
                ], fluid=True, className="py-3")
            ], id='page-content', className="content-container",
               style=CONTENT_STYLE if current_user.is_authenticated else {"padding": "2rem"})
        ], className="app-container")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)