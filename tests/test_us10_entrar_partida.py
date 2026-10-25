import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.lobby import services
from app.modules.lobby.schemas import Partida


@pytest.fixture(autouse=True)
def reset_partidas():
    services.partidas.clear()
    services.partidas.update(
        {
            1: Partida(id=1, jogadores=[], max_jogadores=6, iniciada=False),
            2: Partida(id=2, jogadores=[10, 11], max_jogadores=2, iniciada=False),
            3: Partida(id=3, jogadores=[20, 21], max_jogadores=6, iniciada=True),
        }
    )


@pytest.fixture
def client():
    return TestClient(app)


def test_entrar_partida_com_sucesso(client):
    resposta = client.post("/poker/1/entrar?idJogador=99")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["sucesso"] is True
    assert dados["idPartida"] == 1
    assert dados["idJogador"] == 99
    assert 99 in services.partidas[1].jogadores


def test_entrar_partida_mesa_cheia(client):
    resposta = client.post("/poker/2/entrar?idJogador=99")
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "A mesa está cheia."


def test_entrar_partida_ja_iniciada(client):
    resposta = client.post("/poker/3/entrar?idJogador=99")
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "A partida já foi iniciada."


def test_entrar_partida_inexistente(client):
    resposta = client.post("/poker/999/entrar?idJogador=99")
    dados = resposta.json()

    assert resposta.status_code == 404
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "Partida não encontrada."


def test_entrar_partida_jogador_duplicado(client):
    resposta = client.post("/poker/2/entrar?idJogador=10")
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "O jogador já está nesta partida."


def test_entrar_partida_sem_id_jogador(client):
    resposta = client.post("/poker/1/entrar")
    assert resposta.status_code == 422
