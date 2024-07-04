from Send_messages import send_message
from Message_processing import get_messages
from Message_processing import app
import threading
import requests
import os
import time
import json

URL = "http://0.0.0.0:6969/predict/"

def process_audio(message):
    if 'audio' in message['mimetype']:
        answer = "Recebemos seu áudio e estamos analisando se ele foi gerado por uma inteligência artificial.\n\n*Isso pode levar alguns segundos*."
        send_message(message['number'], answer)
        time.sleep(2) 
        filename = f"{message['timestamp']}.oga"
        filepath = os.path.join('/home/reis/DeepfakeDetection/audio_samples', filename)
        files = {'audio_file':open(filepath, 'rb')}
        response = requests.post(URL, files=files)
        if response.status_code == 200:
            data = json.loads(response.text)
            result = f"Seu aúdio foi processado com êxito!\n\nNossos algoritmos de classificação apontam que o aúdio é: {data['predicted_class']}!\n\nObrigado por usar nosso serviço!"
        else:
            result = "Hmmm...\n\nHouve um erro ao processar o áudio.\nTente novamente mais tarde."
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
