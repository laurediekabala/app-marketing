# utils/theme.py
from dash import callback, Output, Input
import dash_bootstrap_components as dbc

# Styles pour le contenu principal
CONTENT_STYLE = {
    "transition": "margin-left .3s, background-color 0.3s ease, color 0.3s ease",
    "margin-left": "18rem",
    "padding": "2rem 1rem",
    "min-height": "100vh"
}

# Style pour la sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "1rem",
    "transition": "all 0.3s ease",
    "overflow-y": "auto",
    "z-index": 1000,
    "border-right": "1px solid #dee2e6",
    "display": "flex",
    "flex-direction": "column"
}

# Définition des thèmes clair et sombre
THEMES = {
    'light': {
        'sidebar-bg': '#f8f9fa',
        'content-bg': '#ffffff', 
        'text-color': '#212529',
        'plotly': 'plotly_white',
        'card-bg': '#ffffff',
        'border-color': '#dee2e6'
    },
    'dark': {
        'sidebar-bg': '#212529',
        'content-bg': '#1a1a1a',
        'text-color': '#f8f9fa',
        'plotly': 'plotly_dark',
        'card-bg': '#343a40',
        'border-color': '#495057'
    }
}

# SUPPRIMÉ : Le callback serveur qui causait le conflit
# @callback(...)

def get_theme_colors(theme='light'):
    """Retourne les couleurs du thème spécifié"""
    return THEMES.get(theme, THEMES['light'])