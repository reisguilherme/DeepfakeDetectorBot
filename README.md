# Detecção de aúdios gerados por inteligência artificial no WhatsApp.


Este projeto implementa um bot para detecção de áudios gerados por inteligência artificial (IA) no WhatsApp. O objetivo principal é identificar e sinalizar áudios que foram gerados por modelos de síntese de fala automatizados, dificultando golpes de falsidade ideológica por meio de clonagem de voz e a propagação em massa de notícias falsas.

## Funcionalidades Principais

- **Detecção Simplificada ao usuário:** O bot se integra ao WhatsApp por meio de um número ao qual o usuário pode encaminhar aúdios para verificar sua autenticidade.
- **Alerta:** Notifica o usuário designado quando um áudio é classificado como falso.


## Requisitos de Instalação

- Python 3.x
- Docker 
- Pacotes Python listados em `requirements.txt`

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/reisguilherme/DeepfakeDetectorBot.git
   cd DeepfakeDetectorBot
   ```

2. Instale as dependências:

   ```bash
   cd application
   pip install -r requirements.txt
   cd ..
   ```

3. Iniciar o bot e o modelo de detecção de aúdios deepfake:

   Primeiro é necessário editar as configurações do servidor que irá executar o bot.

   ```bash
   cd source_bot/src
   nano server_config.json
   ```

   Edite a variável 'serverIP' com o ip público da máquina que irá rodar o bot. Salve as mudanças feitas e prossiga com os próximos comandos:

   ```bash
   cd ../..
   sudo docker compose up
   ```
   Configure as credenciais do WhatsApp quando um Qrcode do bot aparecer na tela.

   Uma vez que o servidor do bot e o modelo de detecção de deepfakes estiverem rodando, use o comando abaixo para iniciar a integração:

    ```bash
    cd application
    python3 Main.py
   ```


## Uso

- O bot irá ler e responder mensagens recebidas pelo número que foi usado para a configuração das credenciais.
- Envie mensagens para esse número caso queira realizar a verificação de veracidade de algum aúdio.
- O bot analisará automaticamente os áudios recebidos e notificará o usuário quando detectar um áudio gerado por IA.

## TO DO

- Configurar DockerFile e editar docker-compose.yaml para a integração automática do módulo 'application'.
- Melhorar a lógica de processamento e resposta das mensagens do WhatsApp.
- Implementar lógica necessária para lidar com vídeos.
- Melhorar a robustez e generalização do modelo de detecção.
- Implementar módulos para funcionamento do modelo em larga escala e módulo de monitoramento automático de mensagens em grupos.
