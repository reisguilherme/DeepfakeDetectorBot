from Send_messages import send_message
from Message_processing import get_messages
from Message_processing import app
import threading
import requests
import os
import time
import json

URL = "http://model:6969/predict/"

def process_audio(message):
    if 'audio' in message['mimetype']:
        # Notify the user that the audio is being processed
        answer = "Recebemos seu áudio e estamos analisando se ele foi gerado por uma inteligência artificial.\n\n*Isso pode levar alguns segundos*."
        send_message(message['number'], answer)
        # Simulate processing time
        time.sleep(2)
        # Prepare the file path and URL
        filename = f"{message['timestamp']}.oga"
        filepath = os.path.join('/app/audio_samples', filename)
        try:
            # Open the audio file and prepare for upload
            with open(filepath, 'rb') as audio_file:
                files = {'audio_file': audio_file}
                response = requests.post(URL, files=files)
            if response.status_code == 200:
                data = response.json()
                result = f"Seu áudio foi processado com êxito!\n\nNossos algoritmos de classificação apontam que o áudio é: {data['predicted_class']}!\n\nObrigado por usar nosso serviço!"
            else:
                result = "Hmmm...\n\nHouve um erro ao processar o áudio. Tente novamente mais tarde."
        except Exception as e:
            result = f"Hmmm...\n\nHouve um erro ao processar o áudio: {str(e)}. Tente novamente mais tarde."
        # Send the final result to the user
        send_message(message['number'], result)

def send_welcome(message):
    answer = "Olá! Este é o bot de detecção de *áudios gerados por inteligência artificial* (DeepFakes) do CEIA-UFG.\n\n*Envie um áudio* para verificar se ele foi gerado por uma IA e garantir sua segurança."
    send_message(message['number'], answer)

def Master():
    for message in get_messages():
        """
        Processa as mensagens recebidas e envia a resposta.
        Configurar o endpoint do modelo de DeepFake aqui.
        
        """
        print(message)     
        if message['mimetype'].startswith('audio') and message['text'] == '':
            process_audio(message)
        else:
            send_welcome(message)

if __name__ == '__main__':
    message_thread = threading.Thread(target=Master)
    message_thread.start()
    app.run(host='0.0.0.0', port=3001)
