# pages/manage_users.py
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table, ALL
import dash_bootstrap_components as dbc
from database import get_all_users, add_user, delete_user
import hashlib

dash.register_page(__name__, path='/manage-users', name='Gestion des Utilisateurs')

def generate_users_table():
    """Crée la table des utilisateurs à partir de la base de données."""
    users_data = get_all_users()
    # On ne veut pas afficher le mot de passe, même hashé, dans la table
    #for user in users_data:
        #del user['password']
    return dash_table.DataTable(
        id='users-table',
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Nom d'utilisateur", "id": "username"},
            {"name": "Rôle", "id": "role"},
            {"name": "Actions", "id": "actions", "type": "text", "presentation": "markdown"}
        ],
        data=[{**user, 'actions': f'[Supprimer]({user["id"]})'} for user in users_data],
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        markdown_options={"link_target": "_self"} # Pour les liens de suppression
    )

def layout():
    return dbc.Container([
        html.H2("Gestion des Utilisateurs", className="mb-4"),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Ajouter un nouvel utilisateur"),
                    dbc.CardBody([
                        dbc.Input(id="new-username", placeholder="Nom d'utilisateur", type="text", className="mb-2"),
                        dbc.Input(id="new-password", placeholder="Mot de passe", type="password", className="mb-2"),
                        dbc.Select(
                            id="new-role",
                            options=[
                                {"label": "Admin", "value": "admin"},
                                {"label": "Analyste", "value": "analyste"},
                            ],
                            placeholder="Sélectionner un rôle",
                            className="mb-3"
                        ),
                        dbc.Button("Ajouter l'utilisateur", id="add-user-button", color="primary"),
                        html.Div(id="add-user-output", className="mt-3")
                    ])
                ]),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                     dbc.CardHeader("Liste des utilisateurs existants"),
                     dbc.CardBody(id='users-table-container', children=[generate_users_table()])
                ]),
                md=8
            )
        ]),
         # Store pour déclencher la suppression
        dcc.Store(id='store-deleted-user-id')
    ], fluid=True)


@callback(
    Output('add-user-output', 'children'),
    Output('users-table-container', 'children', allow_duplicate=True),
    Input('add-user-button', 'n_clicks'),
    State('new-username', 'value'),
    State('new-password', 'value'),
    State('new-role', 'value'),
    prevent_initial_call=True
)
def handle_add_user(n_clicks, username, password, role):
    if not all([username, password, role]):
        return dbc.Alert("Veuillez remplir tous les champs.", color="warning"), dash.no_update

    try:
        add_user(username, password, role)
        alert = dbc.Alert(f"Utilisateur '{username}' ajouté avec succès.", color="success")
        new_table = generate_users_table()
        return alert, new_table
    except Exception as e:
        return dbc.Alert(f"Erreur lors de l'ajout : {e}", color="danger"), dash.no_update

@callback(
    Output('store-deleted-user-id', 'data'),
    Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'delete-button', 'index': ALL}, 'id'),
    prevent_initial_call=True
)
def store_user_to_delete(n_clicks, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = eval(button_id_str) # Convertit la chaîne en dictionnaire
    user_id_to_delete = button_id['index']
    
    return {'user_id': user_id_to_delete}


@callback(
    Output('users-table-container', 'children'),
    Output('add-user-output', 'children', allow_duplicate=True),
    Input('users-table', 'cell_clicked'),
    prevent_initial_call=True
)
def handle_delete_user(cell_clicked):
    if not cell_clicked or cell_clicked['column_id'] != 'actions':
        return dash.no_update

    user_id_to_delete = cell_clicked['row_id']
    try:
        delete_user(user_id_to_delete)
        alert = dbc.Alert(f"Utilisateur ID {user_id_to_delete} supprimé.", color="info")
        new_table = generate_users_table()
        return new_table, alert
    except Exception as e:
        alert = dbc.Alert(f"Erreur lors de la suppression : {e}", color="danger")
        return dash.no_update, alert