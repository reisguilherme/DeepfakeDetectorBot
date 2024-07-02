async function init(db) {

  /**
   * MENSAGENS QUE ESTÃO NA FILA PARA SEREM ENVIADAS e/ou JÁ FORAM ENVIADAS
   * send_timestamp é o tempo a partid do qual a mensagem pode ser enviada
   * se não informado, o banco assume que ela já pode ser enviada a partir do momento em que chega
   */
  
  await db.exec(`CREATE TABLE IF NOT EXISTS messages_sent (
        id              INTEGER   PRIMARY KEY,
        timestamp       TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime') ),
        send_timestamp  TIMESTAMP NOT NULL DEFAULT (DATETIME('now', 'localtime') ),
        number          INTEGER   NOT NULL,
        state           INTEGER   NOT NULL DEFAULT (0),
        message         TEXT      NOT NULL,
        file            TEXT      DEFAULT  ''
    );`);


   /* MENSAGENS RECEBIDAS */

   await db.exec(`CREATE TABLE IF NOT EXISTS messages_received (
      id             INTEGER      PRIMARY KEY,
      timestamp      TIMESTAMP    NOT NULL DEFAULT (DATETIME('now', 'localtime') ),
      number         INTEGER      NOT NULL,
      message        TEXT         NOT NULL,
      mimetype       TEXT         DEFAULT '',
      filedownloaded INTEGER NOT NULL DEFAULT 0
  );`);


  console.log('Tabelas inicializadas com sucesso!')

}

module.exports = init;