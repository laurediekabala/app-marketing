# pages/home.py
from dash import html
import dash_bootstrap_components as dbc


def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.I(className="fas fa-university me-2 d-none d-sm-inline"),
                        "Bienvenue sur BankPredict"
                    ], className="text-center mb-3 fw-bold"),
                    html.P(
                        "Plateforme d'analyse et de prédiction pour le marketing bancaire",
                        className="lead text-center text-muted"
                    ),
                ], className="mb-4"),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H4([
                                    html.I(className="fas fa-chart-line me-2"),
                                    "Analyse"
                                ], className="text-center mb-0")
                            ]),
                            dbc.CardBody([
                                html.P("Explorez et analysez les données des campagnes marketing.",
                                       className="card-text"),
                                dbc.Button([
                                    html.I(className="fas fa-arrow-right me-2"),
                                    "Voir les analyses"
                                ], href="/analyse", color="primary", className="w-100")
                            ])
                        ], className="shadow-sm h-100")
                    ], xs=12, md=6, className="mb-3"),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.H4([
                                    html.I(className="fas fa-crystal-ball me-2"),
                                    "Prédiction"
                                ], className="text-center mb-0")
                            ]),
                            dbc.CardBody([
                                html.P("Prédisez les résultats des futures campagnes.",
                                       className="card-text"),
                                dbc.Button([
                                    html.I(className="fas fa-arrow-right me-2"),
                                    "Faire une prédiction"
                                ], href="/prediction", color="primary", className="w-100")
                            ])
                        ], className="shadow-sm h-100")
                    ], xs=12, md=6, className="mb-3")
                ], className="mt-3")
            ], xs=12)
        ])
    ], fluid=True, className="py-3 py-md-4")