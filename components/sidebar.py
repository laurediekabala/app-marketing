# components/sidebar.py
import dash
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user
from utils.theme import SIDEBAR_STYLE

def layout():
    """
    Crée le layout de la barre latérale avec espacement optimal et thème dynamique
    """
    
    nav_links = []
    
    # Vérifie si un utilisateur est authentifié
    if current_user.is_authenticated:
        
        # 🏠 ACCUEIL : Accessible à TOUS les utilisateurs authentifiés
        nav_links.append(
            dbc.NavLink(
                [
                    html.I(className="fas fa-home me-2"),
                    "Accueil"
                ], 
                href="/", 
                active="exact", 
                className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
            )
        )
        
        # Permissions selon le rôle
        user_role = current_user.role
        
        if user_role == 'admin':
            # 👑 ADMIN : Accès total
            nav_links.extend([
                dbc.NavLink(
                    [
                        html.I(className="fas fa-chart-line me-2"),
                        "Analyse"
                    ], 
                    href="/analyse", 
                    active="exact", 
                    className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-crystal-ball me-2"),
                        "Prédiction"
                    ], 
                    href="/prediction", 
                    active="exact", 
                    className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-users-cog me-2"),
                        "Gestion"
                    ], 
                    href="/gestion", 
                    active="exact", 
                    className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
                ),
            ])
            
        elif user_role in ['user', 'analyste']:
            # 📊 UTILISATEUR/ANALYSTE : Accès à analyse et prédiction
            nav_links.extend([
                dbc.NavLink(
                    [
                        html.I(className="fas fa-chart-line me-2"),
                        "Analyse"
                    ], 
                    href="/analyse", 
                    active="exact", 
                    className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-crystal-ball me-2"),
                        "Prédiction"
                    ], 
                    href="/prediction", 
                    active="exact", 
                    className="text-decoration-none mb-2 d-flex align-items-center nav-link-custom"
                ),
            ])
        else:
            # 🔍 RÔLE INCONNU
            nav_links.append(
                dbc.Alert(
                    [
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        f"Rôle inconnu: {user_role}"
                    ], 
                    color="warning", 
                    className="mb-2 d-flex align-items-center"
                )
            )

    return html.Div([
        # Header de la sidebar (partie haute fixe)
        html.Div([
            html.Div([
                html.H3([
                    html.I(className="fas fa-university me-2"),
                    "BankPredict"
                ], className="fw-bold text-primary mb-1"),
                html.Small("Système de prédiction", className="text-muted d-block")
            ])
        ], className="mb-3 text-center"),
        
        html.Hr(className="my-3"),
        
        # 👤 Section utilisateur
        html.Div([
            html.Div([
                html.Div([
                    html.I(className="fas fa-user-circle fa-2x text-primary me-2"),
                    html.Div([
                        html.P(
                            f"{current_user.username}", 
                            className="fw-bold mb-0 text-truncate small"
                        ) if current_user.is_authenticated else html.P(
                            "Non connecté", 
                            className="text-muted mb-0"
                        ),
                        html.Small(
                            [
                                html.I(className="fas fa-id-badge me-1"),
                                f"{current_user.role.upper()}"
                            ], 
                            className="text-muted d-flex align-items-center"
                        ) if current_user.is_authenticated else None,
                    ], className="d-flex flex-column justify-content-center flex-grow-1")
                ], className="d-flex align-items-center"),
            ], className="p-2")
        ], className="bg-light rounded mb-3 user-info-card"),
        
        # 🧭 Section navigation (partie extensible)
        html.Div([
            html.H6([
                html.I(className="fas fa-compass me-2"),
                "Navigation"
            ], className="text-muted mb-2 d-flex align-items-center"),
            dbc.Nav(
                nav_links, 
                vertical=True, 
                pills=True, 
                className="flex-column navigation-menu"
            ),
        ], className="flex-grow-1 mb-4"),
        
        # Section du bas (partie basse fixe) - BIEN ESPACÉE DU BOUTON DE DÉCONNEXION
        html.Div([
            html.Hr(className="my-3"),
            
            # 🎨 Section Thème
            html.Div([
                html.Label([
                    html.I(className="fas fa-palette me-2"),
                    "Thème"
                ], className="form-label fw-bold mb-2 d-flex align-items-center"),
                html.Div([
                    dbc.Switch(
                        id="theme-switch",
                        label="Mode sombre",
                        value=False,
                        persistence=True,
                        persistence_type="local",
                        className="theme-switch"
                    ),
                ], className="mb-4")  # Marge importante après le thème
            ], className="theme-section"),
            
            # 🚪 Section Déconnexion - BIEN SÉPARÉE
            html.Div([
                html.Hr(className="my-2 opacity-50"),  # Séparateur léger
                dbc.Button(
                    [
                        html.I(className="fas fa-sign-out-alt me-2"),
                        "Déconnexion"
                    ],
                    href="/logout",
                    color="outline-danger",
                    size="sm",
                    className="w-100 logout-btn"
                ),
            ], className="logout-section")
            
        ], className="mt-auto pt-3")  # Cette classe pousse cette section vers le bas avec padding top
        
    ], id="sidebar", style=SIDEBAR_STYLE, className="sidebar-container")