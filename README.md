# Detecção de aúdios gerados por inteligência artificial no WhatsApp. 🤖


Este projeto implementa um bot para detecção de áudios gerados por inteligência artificial (IA) no WhatsApp. O objetivo principal é identificar e sinalizar áudios que foram gerados por modelos de síntese de fala automatizados, dificultando golpes de falsidade ideológica por meio de clonagem de voz e a propagação em massa de notícias falsas.

## Funcionalidades Principais

- **Simplicidade ao usuário:** O bot se integra ao WhatsApp através de um número de telefone, permitindo que os usuários interajam com ele diretamente.
- **Alerta:** O bot notifica, via chat individual ou chat em grupo, quando um conteúdo é classificado como gerado por IA.
- **Nível de Confiança:** O bot informa ao usuário a confiança em sua resposta ao analisar algum conteúdo.
- **Monitoramento em larga escala:** O bot pode interagir com múltiplos chats simultaneamente de forma rápida e precisa

## Requisitos de Instalação

- [Python 3.x](https://www.python.org/)
- [Docker](https://www.docker.com/)

## Configuração (Linux)

1. Clone o repositório:

   ```bash
   git clone https://github.com/reisguilherme/DeepfakeDetectorBot.git
   cd DeepfakeDetectorBot
   ```

   Após clonar o repositório acesse a pasta raiz do projeto:

    ```bash
   cd DeepfakeDetectorBot
   ```

3. Iniciar a aplicação:

   Primeiro é necessário [instalar o Docker](https://docs.docker.com/engine/install/ubuntu/) na sua máquina.

   Verifique se a instalação está correta com o comando abaixo:

   ```bash
   sudo docker run hello-world
   ```
   Isso irá baixar uma imagem do Docker Hub e rodar um container de teste para verificar que tudo está funcionando como devia.

   Verifique a versão da sua instalação do Docker:

   ```bash
   sudo docker --version
   ```
   A saída que você verá será algo parecido com:
   ```bash
   Docker version XX.X.X, build abcd123
   ```

   Após garantir que o Docker está instalado e funcionando corretamente prossiga com os próximos comandos:

   Verifique se você está na pasta raiz do repositório com o comando:
   ```bash
   cd ../..
   ```
   Na pasta raiz, execute:
   ```bash
   sudo docker compose up --build
   ```
   Aguarde a construção das imagens e início dos contâineres (isso pode demorar).

   Por fim, configure as credenciais do WhatsApp quando um Qrcode do bot aparecer na tela (use uma conta secundária do Whatsapp e deixe-a exclusivamente para o bot).

   Uma vez que o servidor do bot e o modelo de detecção de deepfakes estiverem rodando será possível usar a aplicação.

## Uso

- O bot irá ler e responder mensagens recebidas no número que foi usado para a configuração das credenciais.
- Envie mensagens para esse número caso queira realizar a verificação de veracidade de algum aúdio.
- O bot analisará automaticamente os áudios e vídeos recebidos e notificará o usuário quando detectar um áudio gerado por IA.
