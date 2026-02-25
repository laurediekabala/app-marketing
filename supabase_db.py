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
# supabase_db.py
import os
from supabase import create_client, Client
import hashlib

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL et SUPABASE_KEY doivent être définis dans les variables d'environnement")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password):
    """Hash le mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_user(email, password):
    """Valide les identifiants utilisateur avec Supabase Auth"""
    try:
        # Utiliser l'authentification Supabase
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            # Récupérer le profil utilisateur
            profile_response = supabase.table("profiles").select("*").eq("id", response.user.id).execute()
            
            if profile_response.data:
                profile = profile_response.data[0]
                return {
                    'id': response.user.id,
                    'email': response.user.email,
                    'username': profile.get('username', response.user.email),
                    'role': profile.get('role', 'user')
                }
        return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

def get_user_by_id(user_id):
    """Récupère un utilisateur par son ID"""
    try:
        # Récupérer depuis la table profiles
        response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        if response.data:
            profile = response.data[0]
            return {
                'id': profile['id'],
                'email': profile.get('email', ''),
                'username': profile.get('username', ''),
                'role': profile.get('role', 'user')
            }
        return None
    except Exception as e:
        print(f"Erreur récupération utilisateur : {e}")
        return None

def get_all_users():
    """Récupère tous les utilisateurs depuis Supabase"""
    try:
        response = supabase.table("profiles").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erreur récupération utilisateurs : {e}")
        return []

def add_user(email, password, username=None, role='user'):
    """Ajoute un nouvel utilisateur"""
    try:
        # Créer l'utilisateur avec Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if auth_response.user:
            # Ajouter/Mettre à jour le profil
            profile_data = {
                'id': auth_response.user.id,
                'email': email,
                'username': username or email,
                'role': role
            }
            
            profile_response = supabase.table("profiles").upsert(profile_data).execute()
            return True
        return False
    except Exception as e:
        print(f"Erreur ajout utilisateur : {e}")
        return False

def delete_user(user_id):
    """Supprime un utilisateur (seulement le profil, pas l'auth)"""
    try:
        # Supprimer le profil
        response = supabase.table("profiles").delete().eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Erreur suppression utilisateur : {e}")
        return False

def update_user_role(user_id, new_role):
    """Met à jour le rôle d'un utilisateur"""
    try:
        response = supabase.table("profiles").update({"role": new_role}).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Erreur mise à jour rôle : {e}")
        return False

        
