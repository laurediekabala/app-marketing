# components/sidebar.py
import dash
from dash import html, clientside_callback, Output, Input, State
import dash_bootstrap_components as dbc
from flask_login import current_user
from utils.theme import SIDEBAR_STYLE


def layout():
    nav_links = []

    if current_user.is_authenticated:
        nav_links.append(
            dbc.NavLink([
                html.I(className="fas fa-home me-2"), "Accueil"
            ], href="/", active="exact",
               className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom")
        )

        user_role = current_user.role

        if user_role == 'admin':
            nav_links.extend([
                dbc.NavLink([
                    html.I(className="fas fa-chart-line me-2"), "Analyse"
                ], href="/analyse", active="exact",
                   className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"),
                dbc.NavLink([
                    html.I(className="fas fa-crystal-ball me-2"), "Prédiction"
                ], href="/prediction", active="exact",
                   className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"),
                dbc.NavLink([
                    html.I(className="fas fa-users-cog me-2"), "Gestion"
                ], href="/gestion", active="exact",
                   className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"),
            ])
        elif user_role in ['user', 'analyste']:
            nav_links.extend([
                dbc.NavLink([
                    html.I(className="fas fa-chart-line me-2"), "Analyse"
                ], href="/analyse", active="exact",
                   className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"),
                dbc.NavLink([
                    html.I(className="fas fa-crystal-ball me-2"), "Prédiction"
                ], href="/prediction", active="exact",
                   className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"),
            ])
        else:
            nav_links.append(
                dbc.Alert([
                    html.I(className="fas fa-exclamation-triangle me-2"),
                    f"Rôle inconnu: {user_role}"
                ], color="warning", className="mb-2 d-flex align-items-center")
            )

    return html.Div([
        # ☰ Hamburger
        html.Button(
            html.I(className="fas fa-bars"),
            id="sidebar-toggle",
            className="sidebar-toggle",
            n_clicks=0
        ),

        # Overlay
        html.Div(id="sidebar-overlay", className="sidebar-overlay", n_clicks=0),

        # Sidebar
        html.Div([
            # ✕ Close
            html.Button(
                html.I(className="fas fa-times"),
                id="sidebar-close",
                className="sidebar-close",
                n_clicks=0
            ),

            # Header
            html.Div([
                html.H3([
                    html.I(className="fas fa-university me-2"),
                    "BankPredict"
                ], className="fw-bold text-primary mb-1"),
                html.Small("Système de prédiction", className="text-muted d-block")
            ], className="mb-3 text-center"),

            html.Hr(className="my-3"),

            # User
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-user-circle fa-2x text-primary me-2"),
                        html.Div([
                            html.P(
                                f"{current_user.username}",
                                className="fw-bold mb-0 text-truncate small"
                            ) if current_user.is_authenticated else html.P(
                                "Non connecté", className="text-muted mb-0"
                            ),
                            html.Small([
                                html.I(className="fas fa-id-badge me-1"),
                                f"{current_user.role.upper()}"
                            ], className="text-muted d-flex align-items-center"
                            ) if current_user.is_authenticated else None,
                        ], className="d-flex flex-column justify-content-center flex-grow-1")
                    ], className="d-flex align-items-center"),
                ], className="p-2")
            ], className="bg-light rounded mb-3 user-info-card"),

            # Navigation
            html.Div([
                html.H6([
                    html.I(className="fas fa-compass me-2"), "Navigation"
                ], className="text-muted mb-2 d-flex align-items-center"),
                dbc.Nav(nav_links, vertical=True, pills=True,
                        className="flex-column navigation-menu"),
            ], className="flex-grow-1 mb-4"),

            # Bottom
            html.Div([
                html.Hr(className="my-3"),
                html.Div([
                    html.Label([
                        html.I(className="fas fa-palette me-2"), "Thème"
                    ], className="form-label fw-bold mb-2 d-flex align-items-center"),
                    html.Div([
                        dbc.Switch(
                            id="theme-switch", label="Mode sombre",
                            value=False, persistence=True,
                            persistence_type="local", className="theme-switch"
                        ),
                    ], className="mb-4")
                ]),
                html.Div([
                    html.Hr(className="my-2 opacity-50"),
                    dbc.Button([
                        html.I(className="fas fa-sign-out-alt me-2"), "Déconnexion"
                    ], href="/logout", color="outline-danger", size="sm",
                       className="w-100 logout-btn"),
                ])
            ], className="mt-auto pt-3")

        ], id="sidebar", style=SIDEBAR_STYLE, className="sidebar-container")
    ])


# ═══════════════════════════════
# 📱 JAVASCRIPT CALLBACKS
# ═══════════════════════════════

# Ouvrir sidebar
clientside_callback(
    """
    function(n) {
        if (n > 0) {
            var s = document.getElementById('sidebar');
            var o = document.getElementById('sidebar-overlay');
            if (s) s.classList.add('sidebar-open');
            if (o) o.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("sidebar-toggle", "id"),
    Input("sidebar-toggle", "n_clicks"),
    prevent_initial_call=True
)

# Fermer sidebar (X)
clientside_callback(
    """
    function(n) {
        if (n > 0) {
            var s = document.getElementById('sidebar');
            var o = document.getElementById('sidebar-overlay');
            if (s) s.classList.remove('sidebar-open');
            if (o) o.classList.remove('show');
            document.body.style.overflow = '';
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("sidebar-close", "id"),
    Input("sidebar-close", "n_clicks"),
    prevent_initial_call=True
)

# Fermer sidebar (overlay)
clientside_callback(
    """
    function(n) {
        if (n > 0) {
            var s = document.getElementById('sidebar');
            var o = document.getElementById('sidebar-overlay');
            if (s) s.classList.remove('sidebar-open');
            if (o) o.classList.remove('show');
            document.body.style.overflow = '';
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("sidebar-overlay", "id"),
    Input("sidebar-overlay", "n_clicks"),
    prevent_initial_call=True
)

# Fermer sidebar au changement de page
clientside_callback(
    """
    function(p) {
        if (window.innerWidth <= 768) {
            var s = document.getElementById('sidebar');
            var o = document.getElementById('sidebar-overlay');
            if (s) s.classList.remove('sidebar-open');
            if (o) o.classList.remove('show');
            document.body.style.overflow = '';
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("sidebar", "className"),
    Input("url", "pathname"),
    prevent_initial_call=True
)