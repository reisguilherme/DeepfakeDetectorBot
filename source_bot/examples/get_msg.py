from flask import Flask, request, jsonify
import threading
from queue import Queue
import csv 
from server import send_message

app = Flask(__name__)

# Fila para armazenar mensagens
message_queue = Queue()

def save_to_csv(messages):
    csv_file_path = 'messages.csv'
    with open(csv_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Number', 'Message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for message in messages:
            writer.writerow({
                'Number': message['number'],
                'Message': message['message']  
            })

@app.route('/api/mensagem', methods=['POST'])
def post_message():
    data = request.get_json()
    message = data.get('message')
    message_queue.put(message)
    return jsonify({'message': 'Mensagem recebida com sucesso!'})

def model(text):
    model_output = text + text
    return model_output

def process_messages():
    while True:
        message = message_queue.get()
        print(f'Mensagem recebida: {message}')
        messages_to_save = [{'number': message['number'], 'message': message['text']}]
        output_processed = model(message['text'])
        send_message(str(message['number']), str(output_processed))
        save_to_csv(messages_to_save)

if __name__ == '__main__':
    message_thread = threading.Thread(target=process_messages)
    message_thread.start()
    app.run(port=3001)
