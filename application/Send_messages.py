import requests

port = 3000
endpoint = lambda x: f'http://bot:{port}/{x}'

def send_message(number, text,  path_file = None) -> bool:
    """
        Envia a mensagem para a API controlar o envio

        :param number: número do telefone
        :param text: texto a ser enviado
    """
    try:
        r = requests.post(endpoint('send'), json= {'number': number, 
                                                   'text': text, 
                                                   #'timestamp':'2023-07-23 13:21:21'
                                                   'send_file': path_file
                                                   }, timeout=100)
        return r.status_code == 200
    except Exception as e:
        print('Falha em enviar a mensagem',e)
        return False