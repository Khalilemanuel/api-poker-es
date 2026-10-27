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
            2: Partida(id=2, jogadores=[10, 11], max_jogadores=2, iniciada=False, id_criador=10),
            3: Partida(id=3, jogadores=[20, 21], max_jogadores=6, iniciada=True, id_criador=20),
        }
    )


@pytest.fixture
def client():
    return TestClient(app)


def test_consultar_partidas_abertas_com_sucesso(client):
    """Testa se o endpoint retorna 200 e a lista de partidas abertas com os campos esperados."""
    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert isinstance(dados, list)
    assert len(dados) == 2

    partida1 = next(p for p in dados if p["id"] == 1)
    assert partida1["id"] == 1
    assert partida1["participantesAtuais"] == 0
    assert partida1["numeroMaximoPermitidos"] == 6
    assert partida1["jogadores"] == []

    partida2 = next(p for p in dados if p["id"] == 2)
    assert partida2["id"] == 2
    assert partida2["participantesAtuais"] == 2
    assert partida2["numeroMaximoPermitidos"] == 2
    assert partida2["jogadores"] == [10, 11]


def test_partidas_iniciadas_nao_sao_listadas(client):
    """Garante que partidas já iniciadas (iniciada=True) não constam nas partidas abertas."""
    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    ids_retornados = [p["id"] for p in dados]
    assert 3 not in ids_retornados


def test_consultar_partidas_abertas_lista_vazia(client):
    """Testa o retorno de lista vazia quando todas as partidas estão iniciadas."""
    services.partidas[1].iniciada = True
    services.partidas[2].iniciada = True

    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados == []


def test_consultar_partidas_abertas_sem_partidas_cadastradas(client):
    """Testa quando não há nenhuma partida no sistema."""
    services.partidas.clear()

    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert dados == []


def test_filtro_apenas_com_vagas(client):
    """Testa o parâmetro opcional apenasComVagas=True para excluir mesas cheias."""
    resposta = client.get("/poker/partidasAbertas?apenasComVagas=true")
    dados = resposta.json()

    assert resposta.status_code == 200
    assert len(dados) == 1
    assert dados[0]["id"] == 1
    assert dados[0]["participantesAtuais"] == 0
    assert dados[0]["numeroMaximoPermitidos"] == 6


def test_participantes_atualizados_apos_entrada(client):
    """Verifica se a contagem de participantes reflete a entrada de um novo jogador."""
    client.post("/poker/1/entrar?idJogador=99")

    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    partida1 = next(p for p in dados if p["id"] == 1)
    assert partida1["participantesAtuais"] == 1
    assert 99 in partida1["jogadores"]


def test_partida_deixa_de_ser_aberta_ao_ser_iniciada(client):
    """Verifica que quando uma partida é iniciada, ela é removida da listagem de abertas."""
    services.partidas[1].jogadores = [10, 11]
    services.partidas[1].id_criador = 10

    client.post("/poker/1/iniciar?idJogador=10")

    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()

    ids_retornados = [p["id"] for p in dados]
    assert 1 not in ids_retornados


def test_compatibilidade_aliases_de_campos(client):
    """Garante que aliases para convenções snake_case e idPartida estão presentes."""
    resposta = client.get("/poker/partidasAbertas")
    dados = resposta.json()
    p = dados[0]

    assert p["idPartida"] == p["id"]
    assert p["participantes_atuais"] == p["participantesAtuais"]
    assert p["numero_maximo_permitidos"] == p["numeroMaximoPermitidos"]
    assert p["numeroMaximoPermitido"] == p["numeroMaximoPermitidos"]
    assert p["max_jogadores"] == p["numeroMaximoPermitidos"]
