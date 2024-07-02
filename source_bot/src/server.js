const start_venom_client = require("./venom");
const express = require("express");
const cors = require("cors");
// Biblioteca que trata de erros de forma assíncrona
require("express-async-errors");

const app = express();
const router = require("./routes");

// middleware de permissão para outras portas/servidores acessarem rotas
app.use(cors());

// middleware para recebimento e envio de json pelo servidor
app.use(express.json());

// done: criar um endpoint que recebe o numero, a mensagem e a hora que deve ser enviada a mensagem
app.use(router);


// middleware tratar erros assíncronos, o que impede que o servidor pare por eles
// next é uma função que permite passar para o próximo middleware
app.use((error, req, res, next) => {
  // Verifica se é um erro tratado pela aplicação
  if (error instanceof Error) {
    return res.status(400).json({
      error: error.message
    });
  }

  // Se não é tratado
  return res.status(500).json({
    status: "error",
    message: "Internal Server Error"
  });
})


// Porta arbitrária para executar o express
const PORT = 3000;

process.on('SIGINT', function () {
  client.close();
  db.close();
});

app.listen(PORT, async () => {
  try {

    await start_venom_client();
    console.log(`Server is running on http://localhost:${PORT}`)

  } catch (error) {
    console.log(error);
  }

})

//TODO: Alterar a ordem de execução
// O banco de dados precisa inicar antes de todos os outros modulos
// apenas uma conexão do banco de dados é necessária
// todo o codigo acessa sempre o mesmo objeto db