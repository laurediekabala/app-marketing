FROM python:3.11.5-slim

WORKDIR /app

# Copie tout le contenu du dossier Marketune
COPY . /app

# Installation des dépendances Dash
RUN pip install --upgrade pip
RUN pip install -r requirements_dash.txt

EXPOSE 8050

CMD ["python", "index.py"]