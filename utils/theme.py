# utils/theme.py
from dash import callback, Output, Input
import dash_bootstrap_components as dbc

# Styles pour le contenu principal pour laisser de la place à la sidebar
CONTENT_STYLE = {
    "transition": "margin-left .3s",
    "margin-left": "18rem", # Doit correspondre à la largeur de la sidebar
    "padding": "2rem 1rem",
}

# Définition des thèmes clair et sombre
THEMES = {
    'light': {
        'sidebar-bg': '#f8f9fa',
        'content-bg': '#ffffff',
        'text-color': '#212529',
        'plotly': 'plotly_white'
    },
    'dark': {
        'sidebar-bg': '#343a40',
        'content-bg': '#212529',
        'text-color': '#f8f9fa',
        'plotly': 'plotly_dark'
    }
}

@callback(
    Output('theme-store', 'data'),
    Output('sidebar', 'style'),
    Output('page-content', 'style'),
    Input('theme-switch', 'value'),
    prevent_initial_call=True
)
def toggle_theme(is_dark):
    """
    Callback pour basculer entre le thème clair et le thème sombre.
    Met à jour le dcc.Store et les styles de la sidebar et du contenu.
    """
    theme_choice = 'dark' if is_dark else 'light'
    
    sidebar_style = {
        ##**CONTENT_STYLE, # Utilise le style de base
        "background-color": THEMES[theme_choice]['sidebar-bg'],
        "color": THEMES[theme_choice]['text-color'],
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "18rem",
        "padding": "2rem 1rem",
        "transition": "all 0.3s",
    }
    
    content_style = {
        **CONTENT_STYLE,
        "background-color": THEMES[theme_choice]['content-bg'],
        "color": THEMES[theme_choice]['text-color']
    }
    
    return theme_choice, sidebar_style, content_style