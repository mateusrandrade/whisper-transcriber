from __future__ import annotations

from pathlib import Path

import pytest

import transcrever


class DummyModel:
    def __init__(self, texto: str):
        self.texto = texto
        self.caminhos_recebidos: list[str] = []

    def transcribe(self, caminho: str):
        self.caminhos_recebidos.append(caminho)
        return {"text": self.texto}


def configurar_modelo(monkeypatch: pytest.MonkeyPatch, texto: str) -> DummyModel:
    modelo = DummyModel(texto)

    def carregar_modelo(_nome: str) -> DummyModel:
        return modelo

    monkeypatch.setattr(transcrever.whisper, "load_model", carregar_modelo)
    return modelo


def test_transcrever_arquivo_cria_txt_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    arquivo = tmp_path / "audio.mp3"
    arquivo.write_bytes(b"dados ficticios")

    modelo = configurar_modelo(monkeypatch, "conteúdo")

    saida = transcrever.transcrever_arquivo(arquivo, modelo="base")

    assert saida.suffix == ".txt"
    assert saida.exists()
    assert modelo.caminhos_recebidos == [str(arquivo.resolve())]
    assert saida.read_text(encoding="utf-8") == "conteúdo"


def test_validar_caminho_arquivo_inexistente(tmp_path: Path):
    caminho = tmp_path / "inexistente.mp3"

    with pytest.raises(FileNotFoundError) as erro:
        transcrever.validar_caminho(caminho)

    assert "não encontrado" in str(erro.value)


def test_validar_caminho_diretorio(tmp_path: Path):
    with pytest.raises(IsADirectoryError) as erro:
        transcrever.validar_caminho(tmp_path)

    assert "é um diretório" in str(erro.value)


def test_validar_caminho_extensao_nao_suportada(tmp_path: Path):
    arquivo = tmp_path / "arquivo.txt"
    arquivo.write_text("conteudo")

    with pytest.raises(ValueError) as erro:
        transcrever.validar_caminho(arquivo)

    assert "Extensão não suportada" in str(erro.value)


def test_main_sucesso(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    arquivo = tmp_path / "audio.wav"
    arquivo.write_bytes(b"binario")

    configurar_modelo(monkeypatch, "conteúdo")

    codigo = transcrever.main([str(arquivo)])

    captura = capsys.readouterr()
    esperado = arquivo.with_suffix(".txt")

    assert codigo == 0
    assert esperado.exists()
    assert "Transcrição salva em:" in captura.out
    assert str(esperado) in captura.out
    assert captura.err == ""
    assert esperado.read_text(encoding="utf-8") == "conteúdo"


@pytest.mark.parametrize(
    "caminho",
    [
        "arquivo-inexistente.mp3",
        "arquivo.mp3/",
    ],
)
def test_main_erros(tmp_path: Path, capsys: pytest.CaptureFixture[str], caminho: str):
    if caminho.endswith("/"):
        destino = tmp_path / "pasta"
        destino.mkdir()
        alvo = destino
    else:
        alvo = tmp_path / caminho

    codigo = transcrever.main([str(alvo)])
    captura = capsys.readouterr()

    assert codigo == 1
    assert captura.out == ""
    assert "Erro:" in captura.err
