const venom = require('venom-bot');
const { post_message } = require('./post');
const { saveMediaToFile } = require('./config');

let clientInstance;

async function store_messages(message, client) {
  const messageFromGroup = message.isGroupMsg;

  if (!messageFromGroup) {
    let number = message.from.split("@")[0];
    const ddd = number.slice(2, 4);
    number = number.slice(4);
    number = Number('55' + ddd + '9' + number);

    try {
      let msg_filebuff;
      let msg_mimetype = '';
      let msg_text = '';
      const timestamp_value = new Date().toISOString().replace(/[:.]/g, '-');
      if (Object.keys(message.mediaData).length > 0) {
        if ('caption' in message) msg_text = message.caption;
        msg_filebuff = await client.decryptFile(message);
        msg_mimetype = message.mediaData.mimetype;
        await saveMediaToFile(msg_filebuff, msg_mimetype, timestamp_value); // Save file with timestamp
      } else {
        msg_text = message.body;
      }

      const received_message = {
        number,
        text: msg_text,
        mimetype: msg_mimetype,
        buffer: msg_filebuff,
        timestamp: timestamp_value  // Adding timestamp
      };

      await post_message(received_message);
      console.log("Mensagem enviada para processamento!");
    } catch (error) {
      console.error('Error processing message:', error);
    }
  }
}

async function start(client) {
  console.log('Client Started!');
  clientInstance = client;
  client.onMessage(message => store_messages(message, client));
}

async function start_venom_client() {
  try {
    const client = await venom.create({ session: 'session-name' });
    await start(client);
  } catch (error) {
    console.error('Error starting Venom client:', error);
  }
}

module.exports = start_venom_client;
module.exports.getClient = () => clientInstance;
