# gestion.py
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from supabase_db import get_all_users, add_user, delete_user, update_user_role

dash.register_page(__name__, path='/manage-users', name='Gestion des Utilisateurs')

def generate_users_table():
    """Crée la table des utilisateurs à partir de Supabase"""
    users_data = get_all_users()
    return dash_table.DataTable(
        id='users-table',
        columns=[
            {"name": "ID", "id": "id", "width": "200px"},
            {"name": "Email", "id": "email"},
            {"name": "Nom d'utilisateur", "id": "username"},
            {"name": "Rôle", "id": "role"},
        ],
        data=users_data,
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontSize': '14px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{role} = admin'},
                'backgroundColor': '#e8f5e8',
                'color': 'black',
            }
        ],
        row_selectable="single",
        selected_rows=[],
        page_size=10
    )

def layout():
    return dbc.Container([
        html.H2("👥 Gestion des Utilisateurs", className="mb-4"),
        
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("➕ Ajouter un nouvel utilisateur"),
                    dbc.CardBody([
                        dbc.Label("📧 Email"),
                        dbc.Input(
                            id="new-email", 
                            placeholder="email@example.com", 
                            type="email", 
                            className="mb-2"
                        ),
                        dbc.Label("🔒 Mot de passe"),
                        dbc.Input(
                            id="new-password", 
                            placeholder="Mot de passe", 
                            type="password", 
                            className="mb-2"
                        ),
                        dbc.Label("👤 Nom d'utilisateur (optionnel)"),
                        dbc.Input(
                            id="new-username", 
                            placeholder="Nom d'utilisateur", 
                            type="text", 
                            className="mb-2"
                        ),
                        dbc.Label("🎭 Rôle"),
                        dbc.Select(
                            id="new-role",
                            options=[
                                {"label": "👑 Admin", "value": "admin"},
                                {"label": "📊 Analyste", "value": "analyste"},
                                {"label": "👤 Utilisateur", "value": "user"},
                            ],
                            placeholder="Sélectionner un rôle",
                            className="mb-3"
                        ),
                        dbc.Button(
                            "✅ Ajouter l'utilisateur", 
                            id="add-user-button", 
                            color="primary",
                            className="w-100"
                        ),
                        html.Div(id="add-user-output", className="mt-3")
                    ])
                ]),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("📋 Liste des utilisateurs existants"),
                    dbc.CardBody([
                        html.Div(id='users-table-container', children=[generate_users_table()]),
                        html.Hr(),
                        html.H6("🔧 Actions sur l'utilisateur sélectionné"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Select(
                                    id="update-role-select",
                                    options=[
                                        {"label": "👑 Admin", "value": "admin"},
                                        {"label": "📊 Analyste", "value": "analyste"},
                                        {"label": "👤 Utilisateur", "value": "user"},
                                    ],
                                    placeholder="Nouveau rôle",
                                ),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "🔄 Modifier rôle", 
                                    id="update-role-button", 
                                    color="info",
                                    size="sm"
                                ),
                                width=6
                            )
                        ], className="mb-2"),
                        dbc.Button(
                            "🗑️ Supprimer utilisateur", 
                            id="delete-user-button", 
                            color="danger",
                            size="sm",
                            className="w-100"
                        ),
                        html.Div(id="user-action-output", className="mt-2")
                    ])
                ]),
                md=8
            )
        ]),
    ], fluid=True)

@callback(
    [Output('add-user-output', 'children'),
     Output('users-table-container', 'children', allow_duplicate=True),
     Output('new-email', 'value'),
     Output('new-password', 'value'),
     Output('new-username', 'value'),
     Output('new-role', 'value')],
    Input('add-user-button', 'n_clicks'),
    [State('new-email', 'value'),
     State('new-password', 'value'),
     State('new-username', 'value'),
     State('new-role', 'value')],
    prevent_initial_call=True
)
def handle_add_user(n_clicks, email, password, username, role):
    if not all([email, password, role]):
        return dbc.Alert("Veuillez remplir les champs obligatoires (email, mot de passe, rôle).", color="warning"), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    try:
        success = add_user(email, password, username, role)
        if success:
            alert = dbc.Alert(f"✅ Utilisateur '{email}' ajouté avec succès.", color="success")
            new_table = generate_users_table()
            return alert, new_table, "", "", "", ""
        else:
            return dbc.Alert("❌ Erreur lors de l'ajout de l'utilisateur.", color="danger"), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    except Exception as e:
        return dbc.Alert(f"❌ Erreur : {e}", color="danger"), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

@callback(
    [Output('users-table-container', 'children', allow_duplicate=True),
     Output('user-action-output', 'children')],
    Input('update-role-button', 'n_clicks'),
    [State('users-table', 'selected_rows'),
     State('users-table', 'data'),
     State('update-role-select', 'value')],
    prevent_initial_call=True
)
def handle_update_role(n_clicks, selected_rows, table_data, new_role):
    if not selected_rows or not new_role:
        return dash.no_update, dbc.Alert("Veuillez sélectionner un utilisateur et un nouveau rôle.", color="warning")
    
    try:
        user_id = table_data[selected_rows[0]]['id']
        success = update_user_role(user_id, new_role)
        
        if success:
            new_table = generate_users_table()
            alert = dbc.Alert(f"✅ Rôle mis à jour avec succès.", color="success")
            return new_table, alert
        else:
            return dash.no_update, dbc.Alert("❌ Erreur lors de la mise à jour du rôle.", color="danger")
    except Exception as e:
        return dash.no_update, dbc.Alert(f"❌ Erreur : {e}", color="danger")

@callback(
    [Output('users-table-container', 'children', allow_duplicate=True),
     Output('user-action-output', 'children', allow_duplicate=True)],
    Input('delete-user-button', 'n_clicks'),
    [State('users-table', 'selected_rows'),
     State('users-table', 'data')],
    prevent_initial_call=True
)
def handle_delete_user(n_clicks, selected_rows, table_data):
    if not selected_rows:
        return dash.no_update, dbc.Alert("Veuillez sélectionner un utilisateur à supprimer.", color="warning")
    
    try:
        user_id = table_data[selected_rows[0]]['id']
        user_email = table_data[selected_rows[0]]['email']
        
        success = delete_user(user_id)
        
        if success:
            new_table = generate_users_table()
            alert = dbc.Alert(f"✅ Utilisateur '{user_email}' supprimé.", color="info")
            return new_table, alert
        else:
            return dash.no_update, dbc.Alert("❌ Erreur lors de la suppression.", color="danger")
    except Exception as e:
        return dash.no_update, dbc.Alert(f"❌ Erreur : {e}", color="danger")