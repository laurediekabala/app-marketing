# pages/login.py
from dash import dcc, html, callback, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

def layout():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader([
                        html.H3("🔐 Connexion", className="text-center mb-0"),
                        html.P("Connectez-vous avec votre email", className="text-center text-muted mb-0")
                    ]),
                    dbc.CardBody([
                        html.Div(id='login-error', className='mb-3'),
                        
                        dbc.Label("📧 Email", html_for="email-input"),
                        dbc.Input(
                            id='email-input',
                            type='email',
                            placeholder="votre.email@gmail.com",
                            className="mb-3",
                            persistence=True,
                            persistence_type="session"
                        ),
                        dbc.Label("🔒 Mot de passe", html_for="password-input"),
                        dbc.Input(
                            id='password-input',
                            type='password',
                            placeholder="Entrez votre mot de passe...",
                            className="mb-3"
                        ),
                        dbc.Button(
                            [
                                DashIconify(icon="mdi:login", className="me-2"),
                                "Se connecter"
                            ],
                            id='login-button',
                            color="primary",
                            n_clicks=0,
                            className="w-100 mb-3",
                            size="lg"
                        ),
                        html.Hr(),
                        html.Div([
                            html.P([
                                "Pas de compte ? ",
                                html.A(
                                    [
                                        html.I(className="fas fa-user-plus me-1"),
                                        "Demander un accès"
                                    ], 
                                    id="request-access-link",
                                    href="#", 
                                    className="text-primary text-decoration-none fw-bold"
                                )
                            ], className="text-center mb-0")
                        ])
                    ])
                ], className="shadow-lg border-0"),
                width=12,
                sm=10,
                md=6,
                lg=4
            ),
            className="justify-content-center align-items-center",
            style={"min-height": "100vh"}
        ),
        
        # Modal pour demande d'accès
        dbc.Modal([
            dbc.ModalHeader([
                dbc.ModalTitle([
                    html.I(className="fas fa-user-plus me-2 text-primary"),
                    "Demande de création de compte"
                ], className="d-flex align-items-center")
            ]),
            dbc.ModalBody([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-info-circle me-2 text-info"),
                        "Remplissez ce formulaire pour demander un accès à l'application BankPredict."
                    ], className="alert alert-info d-flex align-items-center mb-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Label([
                                html.I(className="fas fa-user me-2 text-secondary"),
                                "Nom complet *"
                            ], className="fw-bold"),
                            dbc.Input(
                                id="request-name",
                                type="text",
                                placeholder="Ex: Jean Dupont",
                                className="mb-3"
                            ),
                        ], md=6),
                        dbc.Col([
                            dbc.Label([
                                html.I(className="fas fa-envelope me-2 text-secondary"),
                                "Email *"
                            ], className="fw-bold"),
                            dbc.Input(
                                id="request-email",
                                type="email",
                                placeholder="jean.dupont@exemple.com",
                                className="mb-3"
                            ),
                        ], md=6),
                    ]),
                    
                    dbc.Label([
                        html.I(className="fas fa-building me-2 text-secondary"),
                        "Organisation"
                    ], className="fw-bold"),
                    dbc.Input(
                        id="request-organization",
                        type="text",
                        placeholder="Nom de votre entreprise ou organisation (optionnel)",
                        className="mb-3"
                    ),
                    
                    dbc.Label([
                        html.I(className="fas fa-comment-alt me-2 text-secondary"),
                        "Justification *"
                    ], className="fw-bold"),
                    dbc.Textarea(
                        id="request-message",
                        placeholder="Décrivez votre besoin d'accès (rôle souhaité, utilisation prévue, contexte professionnel, etc.)...",
                        rows=4,
                        className="mb-3"
                    ),
                    
                    html.Div([
                        html.I(className="fas fa-clock me-2 text-primary"),
                        "Votre demande sera envoyée à l'administrateur : ",
                        html.Strong("laurediekabala@gmail.com", className="text-primary"),
                        html.Br(),
                        html.Small("Vous recevrez une réponse dans les meilleurs délais.", className="text-muted")
                    ], className="alert alert-light border-primary mb-0")
                ]),
                
                html.Div(id="request-response", className="mt-3")
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    [
                        html.I(className="fas fa-times me-2"),
                        "Annuler"
                    ], 
                    id="close-request-modal", 
                    className="me-2",
                    color="light",
                    outline=True
                ),
                dbc.Button(
                    [
                        html.I(className="fas fa-paper-plane me-2"),
                        "Envoyer la demande"
                    ],
                    id="send-request-button",
                    color="primary"
                )
            ])
        ], 
        id="request-modal", 
        is_open=False, 
        backdrop="static", 
        keyboard=False,
        size="lg",
        scrollable=True
        ),
        
    ], fluid=True, className="bg-light")

# Callback pour ouvrir/fermer le modal
@callback(
    Output("request-modal", "is_open"),
    [Input("request-access-link", "n_clicks"),
     Input("close-request-modal", "n_clicks")],
    [State("request-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_request_modal(open_clicks, close_clicks, is_open):
    """Ouvre/ferme le modal de demande d'accès"""
    if open_clicks or close_clicks:
        return not is_open
    return is_open

# Callback pour traiter la demande d'accès
@callback(
    [Output("request-response", "children"),
     Output("request-name", "value"),
     Output("request-email", "value"), 
     Output("request-organization", "value"),
     Output("request-message", "value"),
     Output("request-modal", "is_open", allow_duplicate=True),
     Output("send-request-button", "disabled"),
     Output("send-request-button", "children")],
    Input("send-request-button", "n_clicks"),
    [State("request-name", "value"),
     State("request-email", "value"),
     State("request-organization", "value"),
     State("request-message", "value")],
    prevent_initial_call=True
)
def handle_access_request(n_clicks, name, email, organization, message):
    """Gère l'envoi de la demande d'accès"""
    if not n_clicks:
        return "", "", "", "", "", False, False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]
    
    # Validation des champs obligatoires
    if not name or not email or not message:
        return dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            html.Strong("Champs manquants ! "),
            "Veuillez remplir tous les champs obligatoires (*)"
        ], color="warning"), name or "", email or "", organization or "", message or "", True, False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]
    
    # Validation email
    if "@" not in email or "." not in email:
        return dbc.Alert([
            html.I(className="fas fa-envelope-open-text me-2"),
            html.Strong("Email invalide ! "),
            "Veuillez entrer une adresse email valide"
        ], color="warning"), name, email, organization or "", message, True, False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]
    
    # Validation longueur message
    if len(message.strip()) < 20:
        return dbc.Alert([
            html.I(className="fas fa-comment-slash me-2"),
            html.Strong("Justification trop courte ! "),
            "Veuillez fournir une justification plus détaillée (minimum 20 caractères)"
        ], color="warning"), name, email, organization or "", message, True, False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]
    
    try:
        # Tentative d'envoi d'email
        success = send_access_request_email(name, email, organization, message)
        
        if success:
            return dbc.Alert([
                html.I(className="fas fa-check-circle me-2"),
                html.Div([
                    html.Strong("Demande envoyée avec succès ! 🎉"),
                    html.Br(),
                    "L'administrateur a reçu votre demande et vous contactera sous peu à l'adresse : ",
                    html.Code(email, className="text-primary"),
                    html.Br(),
                    html.Small("Pensez à vérifier vos spams si vous ne recevez pas de réponse.", className="text-muted")
                ])
            ], color="success"), "", "", "", "", False, True, [html.I(className="fas fa-check me-2"), "Envoyé"]
        else:
            # Fallback avec mailto
            mailto_link = f"mailto:laurediekabala@gmail.com?subject=Demande de compte BankPredict - {name}&body=Bonjour,%0A%0AJe souhaiterais obtenir un accès à l'application BankPredict.%0A%0ANom : {name}%0AEmail : {email}%0AOrganisation : {organization or 'Non spécifiée'}%0A%0AJustification :%0A{message}%0A%0AMerci pour votre attention.%0A%0ACordialement,%0A{name}"
            
            return dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                html.Div([
                    html.Strong("Envoi automatique échoué"),
                    html.Br(),
                    "Vous pouvez envoyer votre demande manuellement : ",
                    html.A(
                        [
                            html.I(className="fas fa-external-link-alt me-1"),
                            "Cliquez ici pour ouvrir votre client email"
                        ],
                        href=mailto_link,
                        className="alert-link fw-bold",
                        target="_blank"
                    )
                ])
            ], color="warning"), name, email, organization or "", message, True, False, [html.I(className="fas fa-paper-plane me-2"), "Réessayer"]
            
    except Exception as e:
        print(f"❌ Erreur dans handle_access_request: {e}")
        import traceback
        traceback.print_exc()
        
        return dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            html.Div([
                html.Strong("Erreur technique"),
                html.Br(),
                "Contactez directement l'administrateur : ",
                html.A(
                    "laurediekabala@gmail.com",
                    href="mailto:laurediekabala@gmail.com",
                    className="alert-link fw-bold"
                )
            ])
        ], color="danger"), name, email, organization or "", message, True, False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]

# Callback pour effacer les messages quand on modifie les champs
@callback(
    Output("request-response", "children", allow_duplicate=True),
    [Input("request-name", "value"),
     Input("request-email", "value"),
     Input("request-message", "value")],
    prevent_initial_call=True
)
def clear_request_response(name, email, message):
    """Efface les messages de réponse quand l'utilisateur modifie les champs"""
    return ""

# Callback pour réactiver le bouton quand on modifie les champs
@callback(
    [Output("send-request-button", "disabled", allow_duplicate=True),
     Output("send-request-button", "children", allow_duplicate=True)],
    [Input("request-name", "value"),
     Input("request-email", "value"),
     Input("request-message", "value")],
    prevent_initial_call=True
)
def reset_send_button(name, email, message):
    """Réactive le bouton d'envoi quand l'utilisateur modifie les champs"""
    return False, [html.I(className="fas fa-paper-plane me-2"), "Envoyer la demande"]

def send_access_request_email(name, email, organization, message):
    """
    Fonction pour envoyer l'email de demande d'accès à l'administrateur
    """
    try:
        from datetime import datetime
        
        # Import du module d'envoi email
        try:
            from email_config import send_gmail_email
        except ImportError as e:
            print(f"❌ Erreur import email_config: {e}")
            return False
        
        admin_email = "laurediekabala@gmail.com"
        
        # Créer le sujet
        subject = f"🔑 Nouvelle demande d'accès BankPredict - {name}"
        
        # Créer le corps HTML de l'email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; background-color: #f8f9fa;">
            <!-- Header avec dégradé -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; color: white; border-radius: 15px 15px 0 0;">
                <h1 style="margin: 0; font-size: 28px; font-weight: 300;">🔑 BankPredict</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">Nouvelle demande d'accès utilisateur</p>
            </div>
            
            <!-- Contenu principal -->
            <div style="background-color: white; padding: 40px; border-radius: 0 0 15px 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                
                <!-- Section informations demandeur -->
                <div style="background: linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #2196f3;">
                    <h2 style="color: #1976d2; margin-top: 0; font-size: 20px; display: flex; align-items: center;">
                        <span style="margin-right: 10px;">👤</span> Informations du demandeur
                    </h2>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 15px 0; background-color: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <tr style="background-color: #f5f5f5;">
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0; font-weight: 600; width: 35%; color: #555;">
                                <span style="margin-right: 8px;">🏷️</span>Nom complet
                            </td>
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0; color: #333;">{name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0; font-weight: 600; color: #555;">
                                <span style="margin-right: 8px;">📧</span>Email
                            </td>
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0;">
                                <a href="mailto:{email}" style="color: #1976d2; text-decoration: none; font-weight: 500;">{email}</a>
                            </td>
                        </tr>
                        <tr style="background-color: #f5f5f5;">
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0; font-weight: 600; color: #555;">
                                <span style="margin-right: 8px;">🏢</span>Organisation
                            </td>
                            <td style="padding: 15px 20px; border-bottom: 1px solid #e0e0e0; color: #333;">{organization or 'Non spécifiée'}</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px 20px; font-weight: 600; color: #555;">
                                <span style="margin-right: 8px;">📅</span>Date demande
                            </td>
                            <td style="padding: 15px 20px; color: #333;">{datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Section justification -->
                <div style="background: linear-gradient(135deg, #fff8e1 0%, #f3e5f5 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #ff9800;">
                    <h3 style="margin-top: 0; color: #f57c00; font-size: 18px; display: flex; align-items: center;">
                        <span style="margin-right: 10px;">📝</span> Justification de la demande
                    </h3>
                    <div style="background-color: white; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <p style="margin: 0; font-style: italic; line-height: 1.8; color: #444; font-size: 15px;">
                            "{message}"
                        </p>
                    </div>
                </div>
                
                <!-- Section actions à effectuer -->
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #4caf50;">
                    <h4 style="margin-top: 0; color: #2e7d32; font-size: 18px; display: flex; align-items: center;">
                        <span style="margin-right: 10px;">⚡</span> Actions recommandées
                    </h4>
                    <ol style="margin: 15px 0; padding-left: 25px; color: #2e7d32;">
                        <li style="margin-bottom: 12px; padding: 8px 0;">
                            <strong>🔍 Vérification :</strong> Contrôler l'identité et la légitimité de la demande
                        </li>
                        <li style="margin-bottom: 12px; padding: 8px 0;">
                            <strong>🔧 Création :</strong> Créer le compte via l'interface Supabase
                        </li>
                        <li style="margin-bottom: 12px; padding: 8px 0;">
                            <strong>🎭 Permissions :</strong> Définir le rôle approprié (admin/analyste/user)
                        </li>
                        <li style="margin-bottom: 12px; padding: 8px 0;">
                            <strong>📧 Notification :</strong> Informer l'utilisateur de la création
                        </li>
                    </ol>
                </div>
                
                <!-- Footer -->
                <div style="text-align: center; margin-top: 40px; padding-top: 25px; border-top: 2px solid #f0f0f0;">
                    <div style="background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%); padding: 20px; border-radius: 10px; display: inline-block;">
                        <p style="margin: 0; font-size: 14px; color: #666; line-height: 1.6;">
                            <span style="font-weight: 600;">🤖 Généré automatiquement</span><br>
                            <span style="color: #1976d2; font-weight: 500;">BankPredict - Système de gestion des accès</span><br>
                            <span style="font-size: 12px; color: #999;">🚀 Demande traitée le {datetime.now().strftime('%d/%m/%Y')}</span>
                        </p>
                    </div>
                </div>
                
            </div>
        </body>
        </html>
        """
        
        # Log détaillé
        print("\n" + "="*70)
        print("📧 TRAITEMENT DEMANDE D'ACCÈS - BankPredict")
        print("="*70)
        print(f"🚀 Statut     : En cours de traitement")
        print(f"📤 Expéditeur : Système BankPredict")
        print(f"📥 Destinataire: {admin_email}")
        print(f"👤 Demandeur  : {name}")
        print(f"📧 Email      : {email}")
        print(f"🏢 Organisation: {organization or 'N/A'}")
        print(f"📅 Horodatage : {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')}")
        print("="*70)
        
        # Tentative d'envoi via Gmail
        email_sent = send_gmail_email(admin_email, subject, html_body)
        
        # Résultat
        status_icon = "✅" if email_sent else "❌"
        status_text = "SUCCÈS" if email_sent else "ÉCHEC"
        print(f"{status_icon} RÉSULTAT   : {status_text}")
        print("="*70 + "\n")
            
        # Log dans fichier (toujours, même en cas d'échec)
        try:
            log_entry = f"[{datetime.now().isoformat()}] REQUEST | {name} | {email} | {organization or 'N/A'} | EMAIL_SENT: {email_sent} | MSG_LEN: {len(message)} chars\n"
            with open("access_requests.log", "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"📁 LOG: Enregistrement sauvegardé dans access_requests.log")
        except Exception as log_error:
            print(f"⚠️ WARN: Erreur de logging: {log_error}")
        
        return email_sent
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE dans send_access_request_email: {e}")
        import traceback
        traceback.print_exc()
        return False