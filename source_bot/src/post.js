const fs = require('fs');
const path = require('path');
const axios = require('axios');
const configFilePath = path.join(__dirname, 'server_config.json');

function loadConfig() {
  try {
    const rawData = fs.readFileSync(configFilePath);
    return JSON.parse(rawData);
  } catch (error) {
    console.error('Error loading configurations:', error.message);
    return null;
  }
}

const post_config = loadConfig();

if (post_config) {
  console.log('Configurations loaded successfully:');
  console.log(post_config);

  if (!post_config.enble) {
    console.log('Message posting disabled.');
  } else {
    console.log('Message posting enabled.');
  }
} else {
  console.error('Failed to load configurations. Check the config.json file.');
}

async function post_message(message) {
  if (!post_config) return null;
  if (!post_config.enble) return null;

  try {
    console.log('Sending message:', message);
    const response = await axios.post(`${post_config.serverIP}:${post_config.serverPort}${post_config.postRoute}`, {
      message: message,
    });

    console.log('Response from server:', response.data);
    return response;
  } catch (error) {
    console.error('Error sending message:', error.message);
    return null;
  }
}

module.exports = { post_message, post_config };
