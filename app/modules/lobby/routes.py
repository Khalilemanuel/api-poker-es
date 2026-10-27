from fastapi import APIRouter, Path, Query, status
from fastapi.responses import JSONResponse

from app.modules.lobby.schemas import EntradaPartidaResponse, PartidaAbertaResponse
from app.modules.lobby.services import (
    EntradaPartidaError,
    entrar_partida,
    listar_partidas_abertas,
)

router = APIRouter(tags=["Lobby e Mesas"])


@router.get(
    "/partidasAbertas",
    response_model=list[PartidaAbertaResponse],
    status_code=status.HTTP_200_OK,
    summary="Consulta de partidas abertas / disponíveis (US09)",
    description=(
        "Retorna a lista de partidas abertas que ainda não foram iniciadas.\n\n"
        "Cada item da lista contém:\n"
        "- `id`: Identificador único da partida\n"
        "- `participantesAtuais`: Quantidade de participantes atualmente na mesa\n"
        "- `numeroMaximoPermitidos`: Número máximo permitido de jogadores na mesa\n"
        "- `jogadores`: Lista com os identificadores dos jogadores na mesa\n\n"
        "Opcionalmente, o parâmetro `apenasComVagas` permite filtrar apenas partidas que ainda não lotaram."
    ),
    responses={
        200: {
            "description": "Lista de partidas abertas retornada com sucesso.",
            "model": list[PartidaAbertaResponse],
        },
    },
)
def consultar_partidas_abertas(
    apenasComVagas: bool = Query(
        False,
        description="Se True, filtra apenas as partidas que possuem vagas disponíveis.",
        examples=[False],
    ),
):
    return listar_partidas_abertas(apenas_com_vagas=apenasComVagas)



@router.post(
    "/{idPartida}/entrar",
    response_model=EntradaPartidaResponse,
    status_code=status.HTTP_200_OK,
    summary="Entrada de jogador em uma partida (US10)",
    description=(
        "Permite que um jogador entre em uma mesa de pôquer disponível.\n\n"
        "**Regras e Validações:**\n"
        "- A partida deve existir (retorna 404 se inexistente).\n"
        "- A partida não pode ter sido iniciada (retorna 409 se em andamento).\n"
        "- A mesa não pode estar cheia (retorna 409 se lotação atingida).\n"
        "- O jogador não pode já estar presente na mesa (retorna 409 se duplicado)."
    ),
    responses={
        200: {
            "description": "Jogador entrou na partida com sucesso.",
            "model": EntradaPartidaResponse,
        },
        404: {
            "description": "Partida não encontrada.",
            "model": EntradaPartidaResponse,
        },
        409: {
            "description": "Conflito: mesa cheia, partida iniciada ou jogador duplicado.",
            "model": EntradaPartidaResponse,
        },
    },
)
def entrar_na_partida(
    idPartida: int = Path(..., description="Identificador único da partida desejada.", examples=[1]),
    idJogador: int = Query(..., description="Identificador único do jogador que deseja entrar.", examples=[99]),
):
    try:
        return entrar_partida(id_partida=idPartida, id_jogador=idJogador)
    except EntradaPartidaError as erro:
        return JSONResponse(
            status_code=erro.status_code,
            content=EntradaPartidaResponse(
                sucesso=False,
                mensagem=erro.mensagem,
                idPartida=idPartida,
                idJogador=idJogador,
            ).model_dump(),
        )
