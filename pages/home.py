from dash import html
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Bienvenue sur BankPredict", className="text-center mb-4"),
                html.P(
                    "Plateforme d'analyse et de prédiction pour le marketing bancaire",
                    className="lead text-center"
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Analyse", className="text-center")),
                            dbc.CardBody([
                                html.P("Explorez et analysez les données des campagnes marketing."),
                                dbc.Button("Voir les analyses", href="/analyse", color="primary")
                            ])
                        ])
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Prédiction", className="text-center")),
                            dbc.CardBody([
                                html.P("Prédisez les résultats des futures campagnes."),
                                dbc.Button("Faire une prédiction", href="/prediction", color="primary")
                            ])
                        ])
                    ], md=6)
                ], className="mt-4")
            ])
        ])
    ], fluid=True, className="py-4")