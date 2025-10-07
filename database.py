# database.py
import sqlite3
import hashlib

DB_NAME = 'users.db'

def get_db_connection():
    """Crée une connexion à la base de données."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Permet d'accéder aux colonnes par leur nom
    return conn

def create_table():
    """Crée la table des utilisateurs si elle n'existe pas."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username, password, role):
    """Ajoute un nouvel utilisateur à la base de données avec un mot de passe hashé."""
    conn = get_db_connection()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                     (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        raise Exception(f"Le nom d'utilisateur '{username}' existe déjà.")
    finally:
        conn.close()

def validate_user(username, password):
    """Vérifie si un utilisateur existe avec le bon mot de passe."""
    conn = get_db_connection()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                        (username, hashed_password)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user
    
def get_all_users():
    """Récupère tous les utilisateurs de la base de données."""
    conn = get_db_connection()
    # On exclut le mot de passe pour la sécurité
    users_cursor = conn.execute('SELECT id, username, role FROM users').fetchall()
    conn.close()
    # Convertit les objets Row en dictionnaires pour une manipulation facile
    return [dict(user) for user in users_cursor]

def delete_user(user_id):
    """Supprime un utilisateur par son ID."""
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


        
