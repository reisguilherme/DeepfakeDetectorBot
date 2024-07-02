const { Router } = require("express");
const Database = require("./db/config");
const router = Router();
var db;

// Endpoint para manipulação dos dados
router.post("/send", async (req, res) => {

    if (db === undefined) db = await Database();

    // todo: definir casos de edição pela ferramenta control 
    var { number, text, timestamp, send_file } = req.body;

    if (!number || !text) throw new Error("Number or text is missing");
    
    if (!send_file) send_file = '';

    try {
        await db.store_messages_to_send(number, text, timestamp, send_file);
        console.log("Mensagem armazenada para envio")
        return res.status(200).json({ message: "Mensagem armazenada para envio" });
    } catch (error) {
        console.log(error);
        return res.status(500).json({ message: error})
    }

});

router.post("/history", async (req, res) => {

    if (db === undefined) db = await Database();

    const { number } = req.body;

    if (!number) throw new Error("Number is missing");

    try {
        const history = await db.get_number_history(number);

        if (!history) throw new Error("History could not be retrieved!")
        
        console.log("Histórico enviado!")
        return res.status(200).json( history);

    } catch (error) {
        console.log(error);
        return res.status(500).json({ message: error})
    }
});

router.post("/last", async (req, res) => {
    /* 
        retorna as ultimas mensagens recebidas
    */

    if (db === undefined) db = await Database();

    const { hours } = req.body;

    if (!hours) throw new Error("hours is missing");

    try {
        const history = await db.get_limit_history(hours);

        if (!history) throw new Error("History could not be retrieved!")

        console.log("Histórico enviado!")
        return res.status(200).json(history);

    } catch (error) {
        console.log(error);
        return res.status(500).json({ message: error})
    }
});

module.exports = router;
