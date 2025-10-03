# whisper-transcriber

Script em Python para transcrever áudios e vídeos usando o modelo Whisper, com guia passo a passo para configuração e uso no Windows.

## Pré-requisitos

- Python 3.10 ou superior instalado.
- FFmpeg disponível no sistema.

### Como instalar o FFmpeg (Windows)

1. Acesse o site oficial: <https://ffmpeg.org/download.html>.
2. Clique em **Windows builds from gyan.dev** (link confiável indicado pelo site).
3. Na página que abrir, baixe o arquivo chamado **ffmpeg-release-essentials.zip**.
4. Após o download, clique com o botão direito no arquivo e escolha **Extrair tudo**.
5. Uma pasta chamada `ffmpeg-...` será criada (o nome pode variar um pouco). Renomeie essa pasta para apenas:

   ```
   ffmpeg
   ```
6. Mova essa pasta para dentro do diretório principal do Windows. Normalmente: `C:\ffmpeg`.

### Como configurar o FFmpeg no PATH do Windows

Depois de extrair a pasta `ffmpeg` para `C:\ffmpeg`, é preciso informar ao Windows onde o programa está. Isso é feito adicionando o caminho `C:\ffmpeg\bin` na configuração chamada **Path**.

1. Clique no botão Iniciar (canto inferior esquerdo da tela).
2. Digite `variáveis de ambiente`.
   1. Vai aparecer uma opção chamada **Editar variáveis de ambiente do sistema**.
   2. Clique nela.
3. Na janela que abrir, clique no botão **Variáveis de Ambiente...** (fica embaixo).
4. Agora veja duas seções:
   1. Variáveis de usuário (apenas para sua conta no computador)
   2. Variáveis do sistema (para todos os usuários)

   Você pode usar qualquer uma, mas para simplificar, escolha **Variáveis do sistema**.
5. Nessa lista, encontre a variável chamada **Path**.
   1. Clique em **Path**.
   2. Depois clique em **Editar...**.
6. Vai abrir uma janela com vários caminhos (linhas de texto).
   1. **Não apague nada!**
   2. Clique em **Novo**.
   3. Digite exatamente: `C:\ffmpeg\bin`
7. Clique em **OK** em todas as janelas para salvar.

## Instalando as dependências do projeto

1. Abra o Prompt de Comando.
2. Vá até a pasta do projeto:

   ```
   cd C:\Users\SEU_USUARIO\Desktop\transcricao
   ```
3. Instale as dependências, um comando por vez:

   ```
   pip install git+https://github.com/openai/whisper.git
   pip install torch
   ```

## Uso

Após instalar o FFmpeg e as dependências:

1. Salve o arquivo de áudio ou vídeo em um dos formatos suportados (`.mp3`, `.mp4`, `.m4a`, `.wav`, `.flac`, `.ogg`, `.webm`, `.wma`, `.aac`, `.mov`, `.mkv`).
2. Execute o script `transcrever.py`, informando o caminho do arquivo a ser processado:

   ```bash
   python transcrever.py /caminho/para/o/arquivo.mp3
   ```

   Opcionalmente, você pode indicar um modelo específico do Whisper com a flag `--modelo` (por exemplo, `tiny`, `small`, `medium`, `large`):

   ```bash
   python transcrever.py /caminho/para/o/arquivo.mp4 --modelo small
   ```

3. O script valida o caminho informado, verifica a extensão do arquivo e, em seguida, carrega o modelo com `whisper.load_model` para executar `transcribe`. A transcrição é salva em um arquivo `.txt` com o mesmo nome do arquivo original, codificado em UTF-8.

Caso ocorra algum erro (arquivo inexistente, extensão não suportada etc.), o script exibirá uma mensagem explicando o problema.
