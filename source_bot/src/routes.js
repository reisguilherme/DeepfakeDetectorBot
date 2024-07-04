const { Router } = require("express");
const router = Router();
const venom = require('./venom');

router.post("/send", async (req, res) => {
  const { number, text, send_file } = req.body;

  if (!number || !text) {
    console.error('Number or text is missing');
    return res.status(400).json({ error: "Number or text is missing" });
  }

  const client = venom.getClient();

  if (!client) {
    console.error('Venom client is not initialized');
    return res.status(500).json({ message: "Venom client is not initialized" });
  }

  try {
    console.log('Received request to send message:', req.body);

    if (send_file) {
      console.log(`Sending file to ${number}`);
      await client.sendFile(`${number}@c.us`, send_file, '', text);
    } else {
      console.log(`Sending text to ${number}`);
      await client.sendText(`${number}@c.us`, text);
    }

    console.log('Message sent successfully');
    return res.status(200).json({ message: "Message sent successfully" });
  } catch (error) {
    console.error('Error sending message:', error);
    return res.status(500).json({ message: "Error sending message" });
  }
});

module.exports = router;
