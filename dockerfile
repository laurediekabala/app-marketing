FROM python:3.11.5-slim

WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Copier ton dataset dans le conteneur
COPY dataset/ /app/dataset/

RUN pip install -r requirements_dash.txt

CMD ["python", "api.py"]
