# 🚀 Marketune – Application de Prédiction et d’Analyse Financière

Marketune est une plateforme complète d’analyse et de visualisation des données financières.  
Le projet combine **une API Flask** (pour la prédiction et le traitement des données) et **une application Dash** (pour la visualisation et l’interaction utilisateur).  
L’ensemble est conçu pour être **containerisé avec Docker** et facilement déployable sur le cloud.

---

## 📁 **Structure du projet**

APP_MARKETING/
│
├── api_flask/ # Contient l’API Flask
│ ├── app.py # Fichier principal Flask
│ ├── Dockerfile # Dockerfile de l’API Flask
│ ├── requirements_api.txt # Dépendances de l’API Flask
│ └── ...
│
├── pages/ # Pages de l'application Dash
│ ├── home.py
│ ├── dashboard.py
│ └── ...
│
├── index.py # Fichier principal Dash
├── Dockerfile # Dockerfile pour l’application Dash
├── requirements_dash.txt # Dépendances Dash
├── docker-compose.yml # Orchestration API + Dash
└── README.md # Ce fichier

---

## ⚙️ **Installation locale (sans Docker)**

### 1️⃣ Créer un environnement virtuel
```bash
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements_dash.txt
cd api_flask
pip install -r requirements_api.txt
cd api_flask
python app.py

cd ..
python index.py

🐳 Déploiement avec Docker
1️⃣ Construire les images

Depuis la racine du projet :
docker-compose build
docker-compose up

2️⃣ Lancer les conteneurs
docker-compose up

✅ Dash sera accessible sur :
👉 http://localhost:8050

✅ L’API Flask sur :
👉 http://localhost:5000

🧰 Fichiers Docker importants
🔹 Dockerfile (Dash)
FROM python:3.13-slim
WORKDIR /app
COPY requirements_dash.txt .
RUN pip install --no-cache-dir -r requirements_dash.txt
COPY . .
CMD ["python", "index.py"]

🔹 Dockerfile (API Flask)
FROM python:3.13-slim
WORKDIR /app
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt
COPY . .
CMD ["python", "app.py"]

🔹 docker-compose.yml
version: '3'
services:
  api:
    build: ./api_flask
    ports:
      - "5000:5000"

  dash:
    build: .
    ports:
      - "8050:8050"
    depends_on:
      - api
🔒 Bonnes pratiques

Toujours utiliser un environnement virtuel avant installation locale.

Vérifier la compatibilité des versions Python (3.11 ou 3.13).

Nettoyer les conteneurs avec :
docker-compose down
docker system prune -f

👨‍💻 Auteur

Laurenzo Kabala
Projet académique et professionnel de Data Science
📧 Contact disponible sur demande

📄 Licence

Projet distribué sous licence MIT.

---



