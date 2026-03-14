# gestion.py
import dash
from dash import html, dcc, callback, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from supabase_db import get_all_users, add_user, delete_user, update_user_role

dash.register_page(__name__, path='/manage-users', name='Gestion des Utilisateurs')


def generate_users_table():
    """Crée la table des utilisateurs responsive"""
    users_data = get_all_users()
    return dash_table.DataTable(
        id='users-table',
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Email", "id": "email"},
            {"name": "Utilisateur", "id": "username"},
            {"name": "Rôle", "id": "role"},
        ],
        data=users_data,
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%',
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px 8px',
            'fontSize': '13px',
            'minWidth': '80px',
            'maxWidth': '200px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': 'id'},
                'maxWidth': '100px',
                'display': 'none',
            },
            {
                'if': {'column_id': 'email'},
                'minWidth': '150px',
            },
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'fontSize': '13px',
            'padding': '10px 8px',
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
        page_size=10,
    )


def layout():
    return dbc.Container([
        
        # 📱 CSS Responsive
        html.Style("""
            /* Table responsive */
            .users-table-wrapper {
                width: 100%;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
            }
            
            .users-table-wrapper .dash-table-container {
                overflow-x: auto !important;
            }
            
            /* Actions responsive */
            .action-buttons {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                align-items: center;
            }
            
            @media (max-width: 768px) {
                /* Formulaire pleine largeur */
                .form-card, .table-card {
                    margin-bottom: 1rem;
                }
                
                /* Table font plus petit */
                .dash-cell {
                    font-size: 12px !important;
                    padding: 6px !important;
                }
                
                .dash-header {
                    font-size: 12px !important;
                    padding: 6px !important;
                }
                
                /* Actions empilées */
                .action-buttons {
                    flex-direction: column;
                }
                
                .action-buttons .btn {
                    width: 100%;
                }
                
                /* Role select pleine largeur */
                .role-action-row > div {
                    margin-bottom: 8px;
                }
            }
            
            @media (max-width: 480px) {
                .dash-cell {
                    font-size: 11px !important;
                    padding: 4px !important;
                }
            }
        """),
        
        # Titre
        html.H2([
            html.I(className="fas fa-users-cog me-2"),
            "Gestion des Utilisateurs"
        ], className="mb-3 mb-md-4"),
        
        dbc.Row([
            
            # ═══════════════════════════════════
            # ➕ FORMULAIRE AJOUT UTILISATEUR
            # ═══════════════════════════════════
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-user-plus me-2"),
                            "Nouvel utilisateur"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        # Email
                        dbc.Label([
                            html.I(className="fas fa-envelope me-1"),
                            " Email"
                        ], className="fw-bold small"),
                        dbc.Input(
                            id="new-email",
                            placeholder="email@example.com",
                            type="email",
                            className="mb-2",
                            size="sm"
                        ),
                        
                        # Mot de passe
                        dbc.Label([
                            html.I(className="fas fa-lock me-1"),
                            " Mot de passe"
                        ], className="fw-bold small"),
                        dbc.Input(
                            id="new-password",
                            placeholder="Mot de passe",
                            type="password",
                            className="mb-2",
                            size="sm"
                        ),
                        
                        # Nom d'utilisateur
                        dbc.Label([
                            html.I(className="fas fa-user me-1"),
                            " Nom d'utilisateur ",
                            html.Small("(optionnel)", className="text-muted")
                        ], className="fw-bold small"),
                        dbc.Input(
                            id="new-username",
                            placeholder="Nom d'utilisateur",
                            type="text",
                            className="mb-2",
                            size="sm"
                        ),
                        
                        # Rôle
                        dbc.Label([
                            html.I(className="fas fa-id-badge me-1"),
                            " Rôle"
                        ], className="fw-bold small"),
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
                        
                        # Bouton Ajouter
                        dbc.Button([
                            html.I(className="fas fa-plus-circle me-2"),
                            "Ajouter l'utilisateur"
                        ],
                            id="add-user-button",
                            color="primary",
                            className="w-100"
                        ),
                        
                        html.Div(id="add-user-output", className="mt-3")
                    ])
                ], className="shadow-sm form-card"),
                xs=12, lg=4, className="mb-3"
            ),
            
            # ═══════════════════════════════════
            # 📋 LISTE DES UTILISATEURS
            # ═══════════════════════════════════
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-list me-2"),
                            "Utilisateurs existants"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        
                        # Table responsive
                        html.Div(
                            id='users-table-container',
                            children=[generate_users_table()],
                            className="users-table-wrapper mb-3"
                        ),
                        
                        html.Hr(),
                        
                        # Actions sur l'utilisateur sélectionné
                        html.H6([
                            html.I(className="fas fa-cog me-2"),
                            "Actions"
                        ], className="mb-3"),
                        
                        # Modification du rôle
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
                                xs=12, sm=6, className="mb-2"
                            ),
                            dbc.Col(
                                dbc.Button([
                                    html.I(className="fas fa-sync-alt me-1"),
                                    "Modifier rôle"
                                ],
                                    id="update-role-button",
                                    color="info",
                                    size="sm",
                                    className="w-100"
                                ),
                                xs=12, sm=6, className="mb-2"
                            )
                        ], className="role-action-row mb-2"),
                        
                        # Suppression
                        dbc.Button([
                            html.I(className="fas fa-trash-alt me-2"),
                            "Supprimer l'utilisateur sélectionné"
                        ],
                            id="delete-user-button",
                            color="danger",
                            size="sm",
                            className="w-100"
                        ),
                        
                        html.Div(id="user-action-output", className="mt-3")
                    ])
                ], className="shadow-sm table-card"),
                xs=12, lg=8, className="mb-3"
            )
        ]),
    ], fluid=True, className="py-3 py-md-4")


# ═══════════════════════════════════════════════════
# ➕ CALLBACK — AJOUTER UTILISATEUR
# ═══════════════════════════════════════════════════

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
        return (
            dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                "Veuillez remplir les champs obligatoires."
            ], color="warning", className="small"),
            dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update
        )

    try:
        success = add_user(email, password, username, role)
        if success:
            alert = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                f"Utilisateur '{email}' ajouté avec succès."
            ], color="success", className="small")
            new_table = generate_users_table()
            return alert, new_table, "", "", "", ""
        else:
            return (
                dbc.Alert([
                    html.I(className="fas fa-times-circle me-2"),
                    "Erreur lors de l'ajout."
                ], color="danger", className="small"),
                dash.no_update, dash.no_update,
                dash.no_update, dash.no_update, dash.no_update
            )
    except Exception as e:
        return (
            dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                f"Erreur : {e}"
            ], color="danger", className="small"),
            dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update
        )


# ═══════════════════════════════════════════════════
# 🔄 CALLBACK — MODIFIER RÔLE
# ═══════════════════════════════════════════════════

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
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Sélectionnez un utilisateur et un rôle."
        ], color="warning", className="small")

    try:
        user_id = table_data[selected_rows[0]]['id']
        success = update_user_role(user_id, new_role)

        if success:
            new_table = generate_users_table()
            alert = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                "Rôle mis à jour avec succès."
            ], color="success", className="small")
            return new_table, alert
        else:
            return dash.no_update, dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                "Erreur lors de la mise à jour."
            ], color="danger", className="small")
    except Exception as e:
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            f"Erreur : {e}"
        ], color="danger", className="small")


# ═══════════════════════════════════════════════════
# 🗑️ CALLBACK — SUPPRIMER UTILISATEUR
# ═══════════════════════════════════════════════════

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
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            "Sélectionnez un utilisateur à supprimer."
        ], color="warning", className="small")

    try:
        user_id = table_data[selected_rows[0]]['id']
        user_email = table_data[selected_rows[0]]['email']

        success = delete_user(user_id)

        if success:
            new_table = generate_users_table()
            alert = dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                f"Utilisateur '{user_email}' supprimé."
            ], color="info", className="small")
            return new_table, alert
        else:
            return dash.no_update, dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                "Erreur lors de la suppression."
            ], color="danger", className="small")
    except Exception as e:
        return dash.no_update, dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            f"Erreur : {e}"
        ], color="danger", className="small")