from dash import dcc, html, callback
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def layout():
    return dbc.Container([  # Ajout du return ici
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H3("Connexion", className="text-center")),
                    dbc.CardBody([
                        html.Div(id='login-error', className='text-danger mb-2'),
                        dbc.Label("Nom d'utilisateur"),
                        dbc.Input(
                            id='username-input',
                            type='text',
                            placeholder="Entrez votre nom d'utilisateur...",
                            className="mb-3"
                        ),
                        dbc.Label("Mot de passe"),
                        dbc.Input(
                            id='password-input',
                            type='password',
                            placeholder="Entrez votre mot de passe...",
                            className="mb-3"
                        ),
                        dbc.Button(
                            "Se connecter",
                            id='login-button',
                            color="primary",
                            n_clicks=0,
                            className="w-100"
                        )
                    ])
                ]),
                width=12,
                sm=10,
                md=6,
                lg=4
            ),
            className="justify-content-center align-items-center",
            style={"min-height": "100vh"}
        )
    ], fluid=True)