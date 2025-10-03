"""Implementação simplificada para permitir testes sem a dependência real."""

from __future__ import annotations


class WhisperModel:
    def transcribe(self, _caminho: str):
        raise NotImplementedError("Substitua WhisperModel nas execuções de teste.")


def load_model(_modelo: str) -> WhisperModel:  # pragma: no cover - apenas placeholder
    raise RuntimeError(
        "O pacote whisper real não está instalado. Utilize monkeypatch nos testes."
    )
