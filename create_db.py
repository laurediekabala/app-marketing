# create_db.py
import sqlite3
from werkzeug.security import generate_password_hash
import pandas as pd

# Nom de la base de données
DB_NAME = 'users.db'

def create_database():
    """Crée la table des utilisateurs avec les rôles 'admin' et 'analyste'."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Mise à jour de la table pour accepter 'analyste' au lieu de 'viewer'
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'analyste'))
        )
    ''')
    conn.commit()
    conn.close()
    
    print("Table 'users' créée/vérifiée avec succès.")
    
    # Fonction pour ajouter un utilisateur
    
       
def add_user(username="kabala", password="kabala", role="admin"):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is None:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute('''
                INSERT INTO users (username, password, role) VALUES (?, ?, ?)
            ''', (username, hashed_password, role))
            print(f"Utilisateur '{username}' avec le rôle '{role}' ajouté.")
        else:
            print(f"L'utilisateur '{username}' existe déjà.")
        conn.commit()
        conn.close()    

    # Demander pour l'utilisateur admin
    #add_admin = input("Voulez-vous ajouter un utilisateur 'admin' par défaut (mdp: password) ? (o/n): ")
    #if add_admin.lower() == 'o':
        #add_user('admin', 'password', 'admin')

    # Demander pour l'utilisateur analyste
    #add_analyst = input("Voulez-vous ajouter un utilisateur 'analyste' par défaut (mdp: password) ? (o/n): ")
    #if add_analyst.lower() == 'o':
        #add_user('analyste', 'password', 'analyste')

   
if __name__ == '__main__':
    # Avant de lancer, supprimez l'ancien fichier 'users.db' s'il existe
    import os
    if os.path.exists(DB_NAME):
        print(f"Suppression de l'ancienne base de données '{DB_NAME}'.")
        os.remove(DB_NAME)   
    create_database()
    add_user("kabala","kabala","admin")
    print(pd.DataFrame( add_user("kabala","kabala","admin"),columns=["nom","pass","role"]))
  