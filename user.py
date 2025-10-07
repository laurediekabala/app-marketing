from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, password, role):
        self.id = user_id
        self.username = username
        self._password = password  # Utilisez un attribut privé pour le mot de passe
        self.role = role

    def get_id(self):
        return str(self.id)

    @property
    def password(self):
        return self._password  # Utilisez la propriété pour accéder au mot de passe