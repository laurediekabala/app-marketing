FROM python:3.11.5-slim

WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Copier ton dataset dans le conteneur
COPY dataset/ /app/data/

RUN pip install -r requirements.txt

CMD ["python", "api.py"]
