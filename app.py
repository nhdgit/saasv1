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
    """Gérer les appels entrants avec Twilio et enregistrer l'audio pour une analyse ultérieure"""
    response = VoiceResponse()
    
    # Annonce de début à l'utilisateur
    response.say("Bonjour, vous pouvez commencer à parler après le bip.", language="fr-FR")
    
    # Démarrer l'enregistrement de l'appel
    response.record(
        recording_status_callback="/recording_status",
        recording_status_callback_method="POST"
    )

    return str(response)

@app.route("/recording_status", methods=['POST'])
def recording_status():
    """Gérer le callback d'enregistrement Twilio et envoyer à Deepgram"""
    recording_url = request.form['RecordingUrl']
    
    # Ajouter l'extension .mp3 pour que Deepgram comprenne le format
    recording_url_mp3 = recording_url + ".mp3"
    
    headers = {
        'Authorization': f'Token {deepgram_api_key}'
    }
    
    data = {
        'url': recording_url_mp3
    }
    
    # Envoyer l'enregistrement à Deepgram pour transcription
    deepgram_response = requests.post(
        'https://api.deepgram.com/v1/listen',
        headers=headers,
        json=data
    )

    # Afficher la réponse de Deepgram dans la console
    if deepgram_response.status_code == 200:
        print("Transcription réussie :", deepgram_response.json())
    else:
        print("Erreur lors de la transcription :", deepgram_response.text)

    return '', 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
