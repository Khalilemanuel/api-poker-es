from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.modules.usuarios.schemas import CadastroJogadorRequest, CadastroJogadorResponse
from app.modules.usuarios.services import CadastroJogadorError, cadastrar_jogador

router = APIRouter(tags=["Usuários"])


@router.post(
    "/cadastro",
    response_model=CadastroJogadorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastro de novos jogadores (US01)",
    description=(
        "Permite que um visitante ou novo usuário crie sua conta e perfil de jogador na plataforma.\n\n"
        "**Regras de Negócio e Validações:**\n"
        "- Nome, e-mail, username e senha são obrigatórios.\n"
        "- Formato de e-mail é validado estruturalmente.\n"
        "- Senha deve possuir no mínimo 6 caracteres.\n"
        "- O e-mail informado deve ser único (retorna 409 Conflict se duplicado).\n"
        "- O username informado deve ser único (retorna 409 Conflict se duplicado).\n"
        "- Ao ser cadastrado, o jogador recebe um ID único e saldo inicial de fichas."
    ),
    responses={
        201: {
            "description": "Jogador cadastrado com sucesso.",
            "model": CadastroJogadorResponse,
        },
        400: {
            "description": "Dados de requisição inválidos.",
            "model": CadastroJogadorResponse,
        },
        409: {
            "description": "Conflito: e-mail ou username já cadastrado.",
            "model": CadastroJogadorResponse,
        },
    },
)
def cadastrar_novo_jogador(dados: CadastroJogadorRequest):
    try:
        return cadastrar_jogador(dados)
    except CadastroJogadorError as erro:
        return JSONResponse(
            status_code=erro.status_code,
            content=CadastroJogadorResponse(
                sucesso=False,
                mensagem=erro.mensagem,
            ).model_dump(),
        )
