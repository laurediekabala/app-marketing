# utils/theme.py

CONTENT_STYLE = {
    "transition": "margin-left .3s, background-color 0.3s ease, color 0.3s ease",
    "marginLeft": "18rem",
    "padding": "2rem 1rem",
    "minHeight": "100vh"
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "1rem",
    "transition": "all 0.3s ease",
    "overflowY": "auto",
    "zIndex": 1000,
    "borderRight": "1px solid #dee2e6",
    "display": "flex",
    "flexDirection": "column"
}

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


def get_theme_colors(theme='light'):
    return THEMES.get(theme, THEMES['light'])