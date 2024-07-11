// worker.js
const { parentPort } = require('worker_threads');
const { post_message } = require('./post');

parentPort.on('message', async (message) => {
  try {
    const response = await post_message(message);
    parentPort.postMessage(response);
  } catch (error) {
    parentPort.postMessage({ error: error.message });
  }
});
