# whisper-transcriber

Script em Python para transcrever áudios e vídeos usando o modelo Whisper, com guia passo a passo para configuração e uso no Windows.

## Requisitos

- Python 3.9 ou superior.
- Dependências instaladas com `pip install -r requirements.txt` ou diretamente com `pip install openai-whisper`. O pacote `ffmpeg` precisa estar disponível no sistema para que o Whisper processe os formatos de áudio e vídeo suportados.

## Uso

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
