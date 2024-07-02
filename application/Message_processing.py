from flask import Flask, request, jsonify
from queue import Queue
import csv 

app = Flask(__name__)
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

def get_messages():
    while True:
        message = message_queue.get()
        messages_to_save = [{'number': message['number'], 'message': message['text']}]
        #save_to_csv(messages_to_save)
        yield message
