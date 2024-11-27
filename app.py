import os
from flask import Flask, request
from dotenv import load_dotenv
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration des clés API depuis les variables d'environnement
twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
deepgram_api_key = os.getenv('DEEPGRAM_API_KEY')

# Configuration Twilio
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Créer l'application Flask
app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    """Gérer les appels entrants avec Twilio"""
    response = VoiceResponse()
    response.say("Bonjour, vous pouvez commencer à parler après le bip.", language="fr-FR")
    # Débuter l'enregistrement de l'audio en streaming
    response.start_stream(url="votre_url_de_streaming_ici")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
