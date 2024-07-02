const sqlite3 = require("sqlite3");
const { open } = require("sqlite");
const init = require("./init");
const fs = require('fs');
const mime = require('mime-types');
const post_function = require('../post');
let dbInstance = null;

async function set_state(id) {
  /*
     função para mudar o estado da mensagem
     :param id: id da mensagem; 0 = não enviada, 1 = enviada 
  */
  return await this.connection.run(`UPDATE messages_sent SET state = 1 WHERE id = ${id}`);
}

async function get_messagens_to_send() {
  /*
      função para pegar as mensagens que estão na fila para serem enviadas
  */


  const query = await this.connection.all(`SELECT id, number, message, send_timestamp, file FROM messages_sent 
                                               WHERE state = 0 AND send_timestamp <= datetime('now');`)


  return query;
}

async function store_received_messages(number, text, buffer = undefined, mimetype = '') {
  /*
      função para armazenar mensagens recebidas
      :param number: número de quem enviou a mensagem
      :param text: texto da mensagem
      :param buffer: buffer binário do arquivo
      :param mimetype: extensão/tipo do arquivo
  */
  const query = `INSERT INTO messages_received (number,message, mimetype) VALUES (?,?,?)`
  console.log(number, text);

  if (!mimetype) mimetype = '';
  if (!text)  text = ''; 
  
  try {
    const sq_run = await this.connection.run(query, [number, text, mimetype])
    const newID = sq_run.lastID;
    
    if (buffer)
      await store_received_files(this, buffer, mimetype, newID);

    post_function.post_message({number,text,mimetype,newID});

    return sq_run;

  } catch (error) {
    console.log(error)
  }

}

async function store_received_files(db, filebuff, mimetype, id) {
  /*  Salva o anexo em disco */
  const filename = `${db.path_attachment}${id}.${mime.extension(mimetype)}`;

  const arquivo_salvo = await new Promise((resolve, reject) => {
    fs.writeFile(filename, filebuff, err => {
      if (err) {
        console.error(err);
        resolve(false);
      } else {
        console.log(`${filename} was saved in the current directory!`);
        resolve(true);
      }
    });
  });

  if (arquivo_salvo)
    await db.connection.run(`UPDATE messages_received SET filedownloaded = 1 WHERE id = ${id}`);

  return true
}

async function store_messages_to_send(number, text, timestamp = undefined, send_file = '') {

  console.log(number, text, timestamp);

  try {
    if (timestamp === undefined) {
      const query = `INSERT INTO messages_sent (number, message, file) VALUES (?,?,?)`
      return await this.connection.run(query, [number, text, send_file])
    } else {
      const query = `INSERT INTO messages_sent (number, message, send_timestamp, file) VALUES (?,?,?,?)`
      return await this.connection.run(query, [number, text, timestamp, send_file])
    }
  } catch (error) {
    console.log(error)
  }
}

async function get_number_history(number) {

  /*
    função para recuperar histórico de mensagens enviadas e recebidas de um número
    :param number: número do qual se deseja obter o histórico 
  */

  try {
    // verifica se o numero é uma lista de numeros use o operador IN se nao o where
    filter = `number = ${number}`
    // verifica se number é uma lista de numeros, se é do tipo object e se tem a propriedade length
    
    if (typeof number === 'object' && number.length)
      filter = `number IN (${number.join(',')})`

    query = ` SELECT FALSE AS received_messages, 
                  id, 
                  timestamp, 
                  send_timestamp, 
                  state, 
                  message,
                  NULL AS mimetype, 
                  NULL AS filedownloaded,
                  file,
                  number
            FROM messages_sent
            WHERE ${filter}
            UNION ALL
            SELECT TRUE AS received_messages, 
                  id, 
                  timestamp, 
                  NULL AS send_timestamp, 
                  NULL AS state, 
                  message, 
                  mimetype, 
                  filedownloaded,
                  CASE 
                      WHEN filedownloaded = 1 THEN 
                          id || '.' || SUBSTR(mimetype, INSTR(mimetype, '/') + 1)
                      ELSE
                          NULL
                      END AS file,
                  number
            FROM messages_received
            WHERE ${filter}
            ORDER BY timestamp desc;
          `;

    console.log(query)
    return await this.connection.all(query);

  } catch (error) {
    console.log(`Histórico não adquirido! Erro: ${error}`)
  }


}
async function get_limit_history(n) {
  /*
      Função para recuperar as mensagens das ultimas n horas
  */
  try {
    // pesquisa no banco as mensagens recebidas nas ultimas n horas
    const rows = await this.connection.all(`SELECT id,timestamp,number FROM messages_received  WHERE timestamp > datetime('now', '-${n} hours');`);
    return rows.map((row) => [row.id, row.timestamp, row.number]);    

  } catch (error) {
    console.log(`Histórico não adquirido! Erro: ${error}`)
  }
}


async function initializeSQLite() {

  // Retorna objeto de conexão com db criado caso esse módulo já tenha sido chamado
  if (dbInstance) return dbInstance

  const path_root = './docs/';
  const path_attachment = path_root + 'attachments/';

  [path_root, path_attachment].forEach(path => { if (!fs.existsSync(path)) fs.mkdirSync(path); })

  try {
    const db = await open({ filename: `${path_root}database.sqlite`, driver: sqlite3.Database });
    await init(db); // veriifca se as tabelas foram criadas

    // Armazena instancia única da conexão com o banco
    dbInstance = {
      connection: db,
      path_attachment,
      path_root,
      set_state,
      get_messagens_to_send,
      store_received_messages,
      store_messages_to_send,
      store_received_files,
      get_number_history,
      get_limit_history
    }

    return dbInstance

  } catch (error) {
    console.error("Erro ao conectar ao banco de dados SQLite:", error);
    process.exit(1);
  }

}


module.exports = initializeSQLite;


