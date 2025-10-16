FROM python:3.11.5-slim

WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Copier ton dataset dans le conteneur
COPY dataset/ /app/dataset/

RUN pip install -r requirements_dash.txt

# Exposer le port Dash
EXPOSE 8050

CMD ["python", "index.py"]
