from Send_messages import send_message
from Message_processing import get_messages
from Message_processing import app
import threading
import requests
import os
import time
import json
import random
import logging

URL = "http://model:6969/predict/"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mime_to_extension = {
    'audio/3gpp': ['3gpp'],
    'audio/aac': ['aac'],
    'audio/aiff': ['aif'],
    'audio/amr': ['amr'],
    'audio/mp4': ['m4a'],
    'audio/mpeg': ['mp3', 'mp2', 'mpga', 'mpega'],
    'audio/ogg': ['oga', 'ogg', 'opus', 'spx'],
    'audio/qcelp': ['qcp'],
    'audio/wav': ['wav'],
    'audio/webm': ['webm'],
    'audio/x-caf': ['caf'],
    'audio/x-ms-wma': ['wma'],
}

def process_audio(message):
    if 'audio' in message['mimetype']:
        logging.info(f"MimeType: {message['mimetype']}")
        # Notificar o usuário que o áudio está sendo processado
        welcome_messages = ["Recebemos seu áudio e estamos analisando se ele foi gerado por uma inteligência artificial.", "Isso pode levar alguns segundos."]
        #answer = "Recebemos seu áudio e estamos analisando se ele foi gerado por uma inteligência artificial.\n\n*Isso pode levar alguns segundos*."
        for welcome_message in welcome_messages:
            send_message(message['number'], welcome_message)
            # Simular o tempo de processamento
            time.sleep(random.choice([2, 3, 4]))
        # Determine the file extension based on the MIME type
        #extensions = mime_to_extension.get(message['mimetype'], ['unknown'])[0]
        # Use the first extension in the list as the file extension
        mimetype = message['mimetype'].split(';')[0]
        file_extension = mime_to_extension.get(mimetype)[0]
        # Preparar o caminho do arquivo e URL
        filename = f"{message['timestamp']}.{file_extension}"
        filepath = os.path.join('/app/audio_samples', filename)
        try:
            # Abrir o arquivo de áudio e preparar para upload
            with open(filepath, 'rb') as audio_file:
                files = {'audio_file': audio_file}
                response = requests.post(URL, files=files)
            if response.status_code == 200:
                data = response.json()
                audio_class = "*não foi gerado por IA*, ufa..." if data['predicted_class'] == 0 else "*foi gerado por IA*, tome cuidado e se atente ao conteúdo da conversa."
                result_messages = ["Seu áudio foi processado com êxito!", f"Nossos algoritmos de classificação apontam que o áudio enviado {audio_class}", "Obrigado por usar nosso serviço!"]
            else:
                result_messages = ["Hmmm...", "Houve um erro ao processar o áudio.", "Tente novamente mais tarde."]  
        except Exception as e:
            result_messages = ["Hmmm...", "Não conseguimos processar o áudio.", "Tente novamente mais tarde."]
        # Enviar o resultado final para o usuário
        for result_message in result_messages:
            send_message(message['number'], result_message)
            time.sleep(random.choice([2, 3, 4, 5, 6]))
        # Excluir o arquivo de áudio após o processamento
        try:
            os.remove(filepath)
        except Exception as e:
            logging.info(f"Erro ao tentar excluir o arquivo: {str(e)}")

def send_welcome(message):
    response_messages = ["Olá! Este é o bot de detecção de *áudios gerados por inteligência artificial* (DeepFakes) do Guilherme.", "Envie um áudio para verificar se ele foi gerado por uma IA e garantir sua segurança."]
    #answer = "Olá! Este é o bot de detecção de *áudios gerados por inteligência artificial* (DeepFakes) do CEIA-UFG.\n\n*Envie um áudio* para verificar se ele foi gerado por uma IA e garantir sua segurança."
    for response_message in response_messages:
        send_message(message['number'], response_message)
        time.sleep(2)

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
