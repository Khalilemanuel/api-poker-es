import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.modules.usuarios import services
from app.modules.usuarios.schemas import Jogador


@pytest.fixture(autouse=True)
def reset_jogadores():
    """Reseta a base em memória antes de cada teste."""
    services.jogadores.clear()
    services.jogadores.update(
        {
            10: Jogador(id=10, nome="Carlos Silva", email="carlos@poker.com", username="carlos_poker", avatar="avatar1.png", saldo=1500.0),
            20: Jogador(id=20, nome="Ana Souza", email="ana@poker.com", username="ana_poker", avatar="avatar2.png", saldo=2000.0),
        }
    )
    services._proximo_id = 100


@pytest.fixture
def client():
    return TestClient(app)


def test_cadastro_jogador_com_sucesso(client):
    payload = {
        "nome": "Khalil Angelim",
        "email": "khalil@poker.com",
        "username": "khalil_pro",
        "senha": "senhaSegura123",
        "avatar": "avatar_khalil.png",
        "saldo_inicial": 1000.0,
    }

    resposta = client.post("/poker/cadastro", json=payload)
    dados = resposta.json()

    assert resposta.status_code == 201
    assert dados["sucesso"] is True
    assert dados["nome"] == "Khalil Angelim"
    assert dados["email"] == "khalil@poker.com"
    assert dados["username"] == "khalil_pro"
    assert dados["avatar"] == "avatar_khalil.png"
    assert dados["saldo"] == 1000.0
    assert dados["idJogador"] == 100
    assert 100 in services.jogadores


def test_cadastro_jogador_valores_padrao(client):
    payload = {
        "nome": "Novo Jogador",
        "email": "novo@poker.com",
        "username": "novo_player",
        "senha": "senhaValida456",
    }

    resposta = client.post("/poker/cadastro", json=payload)
    dados = resposta.json()

    assert resposta.status_code == 201
    assert dados["sucesso"] is True
    assert dados["avatar"] == "avatar_padrao.png"
    assert dados["saldo"] == 1000.0


def test_cadastro_jogador_email_duplicado(client):
    payload = {
        "nome": "Outro Carlos",
        "email": "carlos@poker.com",  # Email já existente
        "username": "outro_carlos",
        "senha": "senhaValida123",
    }

    resposta = client.post("/poker/cadastro", json=payload)
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "Já existe um jogador cadastrado com este e-mail."


def test_cadastro_jogador_username_duplicado(client):
    payload = {
        "nome": "Carlos Segundo",
        "email": "carlos2@poker.com",
        "username": "carlos_poker",  # Username já existente
        "senha": "senhaValida123",
    }

    resposta = client.post("/poker/cadastro", json=payload)
    dados = resposta.json()

    assert resposta.status_code == 409
    assert dados["sucesso"] is False
    assert dados["mensagem"] == "Já existe um jogador cadastrado com este nome de usuário."


def test_cadastro_jogador_email_invalido(client):
    payload = {
        "nome": "Jogador Invalido",
        "email": "email-invalido-sem-arroba",
        "username": "jogador_inv",
        "senha": "senhaValida123",
    }

    resposta = client.post("/poker/cadastro", json=payload)
    assert resposta.status_code == 422


def test_cadastro_jogador_senha_curta(client):
    payload = {
        "nome": "Jogador Senha Curta",
        "email": "curta@poker.com",
        "username": "senha_curta",
        "senha": "123",  # Menos de 6 caracteres
    }

    resposta = client.post("/poker/cadastro", json=payload)
    assert resposta.status_code == 422


def test_cadastro_jogador_campos_faltando(client):
    resposta = client.post("/poker/cadastro", json={})
    assert resposta.status_code == 422
