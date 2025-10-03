"""Ferramentas para transcrever arquivos de áudio/vídeo usando Whisper."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Iterable

import whisper

EXTENSOES_SUPORTADAS: frozenset[str] = frozenset(
    {".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".flac", ".wma", ".aac"}
)


def validar_caminho(caminho: str | Path) -> Path:
    """Valida o caminho para o arquivo que será transcrito.

    Args:
        caminho: Caminho para o arquivo de áudio ou vídeo.

    Returns:
        Um objeto :class:`Path` pronto para uso.

    Raises:
        FileNotFoundError: Se o caminho não existir.
        IsADirectoryError: Se o caminho apontar para um diretório.
        ValueError: Se a extensão do arquivo não estiver na lista suportada.
    """

    caminho_path = Path(caminho).expanduser().resolve()
    if not caminho_path.exists():
        raise FileNotFoundError(f"Arquivo '{caminho_path}' não encontrado.")
    if caminho_path.is_dir():
        raise IsADirectoryError(f"O caminho '{caminho_path}' é um diretório.")

    if caminho_path.suffix.lower() not in EXTENSOES_SUPORTADAS:
        extensoes_formatadas = ", ".join(sorted(EXTENSOES_SUPORTADAS))
        raise ValueError(
            "Extensão não suportada. Use arquivos com as seguintes extensões: "
            f"{extensoes_formatadas}."
        )

    return caminho_path


def transcrever_arquivo(caminho: str | Path, modelo: str = "base") -> Path:
    """Transcreve o arquivo indicado e salva um `.txt` com o resultado.

    Args:
        caminho: Caminho para o arquivo de áudio/vídeo.
        modelo: Nome do modelo Whisper a ser utilizado.

    Returns:
        Caminho para o arquivo ``.txt`` gerado com a transcrição.
    """

    arquivo = validar_caminho(caminho)
    modelo_whisper = whisper.load_model(modelo)
    resultado = modelo_whisper.transcribe(str(arquivo))
    texto = resultado.get("text", "")

    destino = arquivo.with_suffix(".txt")
    destino.write_text(texto, encoding="utf-8")
    return destino


def _criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcreve arquivos de áudio e vídeo utilizando Whisper."
    )
    parser.add_argument(
        "arquivo",
        help="Caminho para o arquivo de áudio ou vídeo a ser transcrito.",
    )
    parser.add_argument(
        "-m",
        "--modelo",
        default="base",
        help="Modelo Whisper a ser utilizado (padrão: base).",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    """Ponto de entrada principal do script."""

    parser = _criar_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        arquivo_saida = transcrever_arquivo(args.arquivo, args.modelo)
    except Exception as exc:  # pragma: no cover - mantido simples para CLI
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    print(f"Transcrição salva em: {arquivo_saida}")
    return 0


if __name__ == "__main__":  # pragma: no cover - fluxo de execução direto
    sys.exit(main())
