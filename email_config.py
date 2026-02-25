# email_config.py
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_gmail_email(to_email, subject, html_body):
    """
    Envoie un email via Gmail SMTP
    Nécessite un mot de passe d'application Gmail
    """
    try:
        # Configuration Gmail
        smtp_server = "smtp.gmail.com"
        port = 587
        
        # IMPORTANT : Remplacez par VOS informations
        sender_email = os.getenv("SENDER_EMAIL", "votre-email@gmail.com")  # Votre email Gmail
        password = os.getenv("GMAIL_APP_PASSWORD")  # Votre mot de passe d'application
        
        if not password:
            print("❌ ERREUR: GMAIL_APP_PASSWORD non configuré dans .env")
            return False
            
        if not sender_email or sender_email == "votre-email@gmail.com":
            print("❌ ERREUR: SENDER_EMAIL non configuré dans .env")
            return False
        
        print(f"📤 Envoi depuis: {sender_email}")
        print(f"📥 Vers: {to_email}")
        print(f"📋 Sujet: {subject}")
        
        # Créer le message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"BankPredict <{sender_email}>"
        message["To"] = to_email
        
        # Corps HTML
        html_part = MIMEText(html_body, "html", "utf-8")
        message.attach(html_part)
        
        # Créer connexion sécurisée et envoyer
        context = ssl.create_default_context()
        
        print("🔗 Connexion au serveur Gmail...")
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            print("🔐 Authentification...")
            server.login(sender_email, password)
            print("📨 Envoi en cours...")
            server.sendmail(sender_email, to_email, message.as_string())
            print("✅ Email envoyé avec succès !")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ ERREUR D'AUTHENTIFICATION Gmail: {e}")
        print("🔧 Vérifiez votre mot de passe d'application Gmail")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ ERREUR SMTP: {e}")
        return False
    except Exception as e:
        print(f"❌ ERREUR GÉNÉRALE envoi Gmail: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gmail_connection():
    """
    Teste la connexion Gmail
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not all([sender_email, password]):
            print("❌ Configuration manquante dans .env")
            return False
            
        smtp_server = "smtp.gmail.com"
        port = 587
        
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            print("✅ Connexion Gmail testée avec succès !")
            return True
            
    except Exception as e:
        print(f"❌ Test de connexion échoué: {e}")
        return False

if __name__ == "__main__":
    # Test de la configuration
    print("🧪 Test de configuration Gmail...")
    test_gmail_connection()