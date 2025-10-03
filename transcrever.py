"""Script de linha de comando para transcrever áudios e vídeos com Whisper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import whisper


EXTENSOES_SUPORTADAS: set[str] = {
    ".mp3",
    ".mp4",
    ".m4a",
    ".wav",
    ".flac",
    ".ogg",
    ".webm",
    ".wma",
    ".aac",
    ".mov",
    ".mkv",
}


def analisar_argumentos(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Transcreve arquivos de áudio ou vídeo usando o modelo Whisper e gera "
            "um arquivo .txt com a transcrição."
        )
    )
    parser.add_argument(
        "arquivo",
        help="Caminho para o arquivo de áudio ou vídeo a ser transcrito.",
    )
    parser.add_argument(
        "-m",
        "--modelo",
        default="base",
        help="Nome do modelo Whisper a ser carregado (padrão: base).",
    )
    return parser.parse_args(list(argv))


def validar_caminho(entrada: Path) -> None:
    if not entrada.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {entrada}")
    if not entrada.is_file():
        raise ValueError(f"O caminho precisa apontar para um arquivo: {entrada}")
    if entrada.suffix.lower() not in EXTENSOES_SUPORTADAS:
        extensoes = ", ".join(sorted(EXTENSOES_SUPORTADAS))
        raise ValueError(
            "Extensão de arquivo não suportada. Use um dos formatos: " f"{extensoes}."
        )


def transcrever_arquivo(caminho: Path, modelo: str) -> Path:
    validar_caminho(caminho)
    modelo_carregado = whisper.load_model(modelo)
    resultado = modelo_carregado.transcribe(str(caminho))
    texto_transcrito = resultado.get("text", "").strip()

    arquivo_saida = caminho.with_suffix(".txt")
    with open(arquivo_saida, "w", encoding="utf-8") as saida:
        saida.write(texto_transcrito)

    return arquivo_saida


def main(argv: Iterable[str] | None = None) -> int:
    args = analisar_argumentos(sys.argv[1:] if argv is None else argv)
    caminho = Path(args.arquivo).expanduser().resolve()

    try:
        arquivo_saida = transcrever_arquivo(caminho, args.modelo)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    print(f"Transcrição concluída. Arquivo salvo em: {arquivo_saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
