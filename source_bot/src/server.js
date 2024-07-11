const start_venom_client = require("./venom");
const express = require("express");
const cors = require("cors");
require("express-async-errors");

const app = express();
const router = require("./routes");

app.use(cors());
app.use(express.json());
app.use(router);

app.use((error, req, res, next) => {
  if (error instanceof Error) {
    console.error('Error:', error.message);
    return res.status(400).json({
      error: error.message
    });
  }
  console.error('Internal Server Error:', error);
  return res.status(500).json({
    status: "error",
    message: "Internal Server Error"
  });
});

const PORT = 3000;

process.on('SIGINT', function () {
  client.close();
});

app.listen(PORT, async () => {
  try {
    await start_venom_client();
    console.log(`Server is running on http://localhost:${PORT}`);
  } catch (error) {
    console.error('Failed to start Venom client:', error);
  }
});
