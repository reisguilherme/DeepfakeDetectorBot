// arquivo para o envio da mensagem com o post

// message_sender.js
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const configFilePath = path.join(__dirname, 'server_config.json');


// funcao para carregar as configuracoes do servidor
function loadConfig() {
  try {
    const rawData = fs.readFileSync(configFilePath);
    return JSON.parse(rawData);
    
  } catch (error) {
    console.error('Erro ao carregar configurações:', error.message);
    return null;
      /*
    { 
        "enble": false, // "true" para habilitar o envio de mensagens via post
        "serverIP": "http://127.0.0.1",
        "serverPort": 3001, 
        "postRoute": "/api/mensagem"
      } 
      */   

  }
}
const post_config = loadConfig();


if (post_config) {
  console.log('Configurações carregadas com sucesso:');
  console.log(post_config);

  if (!post_config.enble) 
    console.log('Envio de mensagens via post desabilitado.');
  else
    console.log('Envio de mensagens via post habilitado.');

} else {
  console.error('As configurações não puderam ser carregadas. Verifique o arquivo config.json.');
}


// 
//  Funcao para enviar a mensagem \\ 
//


async function post_message(message) {
    if (!post_config) return;
    if (!post_config.enble) return;

  try {
    const response = await axios.post( `${post_config.serverIP}:${post_config.serverPort}${post_config.postRoute}`, {
      message: message,
    });

    console.log(`[POST]- ${response.data}`);
  } catch (error) {
    console.error('Erro ao enviar mensagem:', error.message);
  }
}


module.exports = { post_message, post_config };
