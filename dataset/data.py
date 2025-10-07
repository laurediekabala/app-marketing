#@callback(
    #Output('login-error', 'children'),
    #Input('login-button', 'n_clicks'),
    #State('username-input', 'value'),
    #State('password-input', 'value')
#)
def check_login(n_clicks, username, password):
    if n_clicks:
        if not username or not password:
            return "Veuillez remplir tous les champs."
        # Ici, ajoutez la vérification réelle des identifiants si besoin
        # Exemple : if username != "admin" or password != "1234": return "Identifiants incorrects."
    return ""
# ...existing code...