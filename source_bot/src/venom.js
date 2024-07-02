const venom = require('venom-bot');
const Database = require("./db/config");
const mime = require('mime-types');
const fs = require('fs');

var db;

async function check_msg(client) {
    /*  função para verificar se tem mensagens para serem enviadas
        :param client: cliente do venom
    */

    cursor = await db.get_messagens_to_send()

    await Promise.all(cursor.map(async record => {
        console.log(record)

        const number = record.number;
        const id = record.id;
        const text = record.message;
        const send_file = record.file;

        try {
                // verifica se o arquivo existe
              var result;

                if ((send_file !== '') && (fs.existsSync(send_file))) {
                    console.log('Envinando o arquivo:',send_file);
                    result =  await client.sendFile(`${number}@c.us`, send_file, '','');
                    //.then((result) => {console.log('Result: ', result);}).catch((erro) => {console.error('Error when sending: ', erro)});
                } else {
                    result = await client.sendText(`${number}@c.us`, text);
                    //.then((result) => {console.log('Result: ', result);}).catch((erro) => {console.error('Error when sending: ', erro)});
                }

            await db.set_state(id) // Atualiza para o id de sucesso da mensagem

            console.log("Result: ", result)
        } catch (error) {
            console.log(error)
        }
    }));

}

async function store_messages(message, client) {
    /*  
        função para armazenar mensagens recebidas
        :param message: objeto com dados da mensagem recebida
    */
    

    // Garante que a origem da mensagem não seja de um grupo
    const messageFromGroup = message.isGroupMsg;

    if (!messageFromGroup) {
        // Recebe número de quem enviou a mensagem. O número é recebido no formato 0000000000@c.us
        let number = message.from.split("@")[0];

        console.log(number.indexOf("55"));

        // Recupera DDD
        const ddd = number.slice(2, 4);

        // Retira 55 e DDD
        number = number.slice(4)
        
        // Adiciona 55, ddd e 9 antes do número para aramazenar informação no padrão Brasil
        number = Number('55' + ddd + '9' + number); 
        
        console.log(number)

        try {

            var msg_filebuff = undefined;
            var msg_mimetype = '';
            var msg_text = '';
            
            if (Object.keys(message.mediaData).length > 0) {
                console.log("Mensagem com arquivo")
                if ('caption' in message)
                    msg_text = message.caption;

                msg_filebuff = await client.decryptFile(message);
                msg_mimetype = message.mediaData.mimetype;
            } else 
                msg_text = message.body;

            
            

            await db.store_received_messages(number, msg_text, msg_filebuff, msg_mimetype);

            console.log("Mensagem armazenada com sucesso!");


        } catch (error) {
            console.log(error)
        }
    }

}

async function start(client) {
    console.log('Client Started!');

    client.onMessage(message => store_messages(message, client));

    client.onStateChange((state) => {
        //todo:
        console.log('State changed: ', state);
    });

    // Verifica se há mensagens a serem enviadas a cada 2 minutos = 120s = 120000ms
    setInterval(async () => {
        await check_msg(client);
        console.log("Varredura feita.")
    }, 5000)
}

async function start_venom_client() {
    try {

        if (db === undefined) // done: banco de dados precisa inicar antes do venom
            db = await Database();

        
        const client = await venom.create({ session: 'session-name' })
        start(client);


    } catch (error) {
        console.log(error);
    }
}

module.exports = start_venom_client;