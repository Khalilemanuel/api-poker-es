from fastapi import status

from app.modules.usuarios.schemas import CadastroJogadorRequest, CadastroJogadorResponse, Jogador


class CadastroJogadorError(Exception):
    """Exceção customizada para regras de negócio do cadastro de jogadores."""
    def __init__(self, mensagem: str, status_code: int):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code


# Armazenamento em memória dos jogadores cadastrados (simulando persistência)
jogadores: dict[int, Jogador] = {
    10: Jogador(id=10, nome="Carlos Silva", email="carlos@poker.com", username="carlos_poker", avatar="avatar1.png", saldo=1500.0),
    20: Jogador(id=20, nome="Ana Souza", email="ana@poker.com", username="ana_poker", avatar="avatar2.png", saldo=2000.0),
}

_proximo_id: int = 100


def cadastrar_jogador(dados: CadastroJogadorRequest) -> CadastroJogadorResponse:
    global _proximo_id

    # 1. Validação de Unicidade de Email
    email_normalizado = dados.email.strip().lower()
    for j in jogadores.values():
        if j.email.lower() == email_normalizado:
            raise CadastroJogadorError(
                "Já existe um jogador cadastrado com este e-mail.",
                status.HTTP_409_CONFLICT,
            )

    # 2. Validação de Unicidade de Username
    username_normalizado = dados.username.strip().lower()
    for j in jogadores.values():
        if j.username.lower() == username_normalizado:
            raise CadastroJogadorError(
                "Já existe um jogador cadastrado com este nome de usuário.",
                status.HTTP_409_CONFLICT,
            )

    # 3. Criação do Jogador
    novo_id = _proximo_id
    _proximo_id += 1

    novo_jogador = Jogador(
        id=novo_id,
        nome=dados.nome.strip(),
        email=email_normalizado,
        username=dados.username.strip(),
        avatar=dados.avatar or "avatar_padrao.png",
        saldo=dados.saldo_inicial,
        ativo=True,
    )

    jogadores[novo_id] = novo_jogador

    return CadastroJogadorResponse(
        sucesso=True,
        mensagem=f"Jogador '{novo_jogador.nome}' cadastrado com sucesso.",
        idJogador=novo_jogador.id,
        nome=novo_jogador.nome,
        email=novo_jogador.email,
        username=novo_jogador.username,
        avatar=novo_jogador.avatar,
        saldo=novo_jogador.saldo,
    )
