import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.lobby import services as lobby_services
from app.modules.lobby.schemas import Partida
from app.modules.motorpartida import services as motor_services


@pytest.fixture(autouse=True)
def reset_partidas():
    lobby_services.partidas.clear()
    lobby_services.partidas.update(
        {
            1: Partida(id=1, jogadores=[10, 11, 12], max_jogadores=6, id_criador=10),
            2: Partida(id=2, jogadores=[20], max_jogadores=6, id_criador=20),
            3: Partida(id=3, jogadores=[30, 31], max_jogadores=6, iniciada=True, id_criador=30),
            4: Partida(id=4, jogadores=[40, 41], max_jogadores=6),
        }
    )
    motor_services.distribuicoes.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_iniciar_partida_com_sucesso(client):
    resposta = client.post("/poker/1/iniciar?idJogador=10")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados["sucesso"] is True
    assert dados["idPartida"] == 1
    assert dados["numeroMao"] == 1
    assert dados["jogadores"] == [10, 11, 12]
    assert lobby_services.partidas[1].iniciada is True


def test_iniciar_partida_distribui_as_cartas(client):
    resposta = client.post("/poker/1/iniciar?idJogador=10")
    dados = resposta.json()
    distribuicao = motor_services.distribuicoes[1]

    assert dados["cartasPorJogador"] == 2
    assert set(distribuicao.maos) == {10, 11, 12}
    assert all(len(mao.visualizar_cartas()) == 2 for mao in distribuicao.maos.values())
    assert len(distribuicao.baralho) == 52 - 6


def test_resposta_mostra_apenas_as_cartas_de_quem_iniciou(client):
    resposta = client.post("/poker/1/iniciar?idJogador=10")
    dados = resposta.json()
    cartas_do_criador = [carta.model_dump(mode="json") for carta in motor_services.distribuicoes[1].maos[10].visualizar_cartas()]

    assert dados["suasCartas"] == cartas_do_criador
    assert len(dados["suasCartas"]) == 2


def test_iniciar_partida_inexistente(client):
    resposta = client.post("/poker/999/iniciar?idJogador=10")
    dados = resposta.json()

    assert resposta.status_code == 404
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "Partida não encontrada."


def test_iniciar_partida_por_jogador_que_nao_criou_a_mesa(client):
    resposta = client.post("/poker/1/iniciar?idJogador=11")
    dados = resposta.json()

    assert resposta.status_code == 403
    assert dados["sucesso"] is False
    assert lobby_services.partidas[1].iniciada is False
    assert 1 not in motor_services.distribuicoes


def test_iniciar_partida_sem_criador_definido(client):
    resposta = client.post("/poker/4/iniciar?idJogador=40")

    assert resposta.status_code == 403
    assert resposta.json()["sucesso"] is False


def test_iniciar_partida_ja_iniciada(client):
    resposta = client.post("/poker/3/iniciar?idJogador=30")
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "A partida já foi iniciada."


def test_iniciar_partida_duas_vezes(client):
    client.post("/poker/1/iniciar?idJogador=10")
    resposta = client.post("/poker/1/iniciar?idJogador=10")

    assert resposta.status_code == 409
    assert motor_services.distribuicoes[1].numero_mao == 1


def test_iniciar_partida_com_jogadores_insuficientes(client):
    resposta = client.post("/poker/2/iniciar?idJogador=20")
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "São necessários pelo menos 2 jogadores para iniciar a partida."
    assert lobby_services.partidas[2].iniciada is False


def test_jogador_nao_entra_depois_que_a_partida_foi_iniciada(client):
    client.post("/poker/1/iniciar?idJogador=10")
    resposta = client.post("/poker/1/entrar?idJogador=99")

    assert resposta.status_code == 409
    assert resposta.json()["mensagem"] == "A partida já foi iniciada."


def test_iniciar_partida_sem_id_jogador(client):
    resposta = client.post("/poker/1/iniciar")
    assert resposta.status_code == 422
