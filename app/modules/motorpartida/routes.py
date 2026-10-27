from fastapi import APIRouter, Path, Query, status
from fastapi.responses import JSONResponse

from app.modules.motorpartida.distribuicao import CARTAS_POR_JOGADOR
from app.modules.motorpartida.schemas import InicioPartidaResponse
from app.modules.motorpartida.services import InicioPartidaError, iniciar_partida

router = APIRouter(tags=["Motor da Partida"])


@router.post(
    "/{idPartida}/iniciar",
    response_model=InicioPartidaResponse,
    status_code=status.HTTP_200_OK,
    summary="Início de uma partida (US12) com distribuição das cartas (US13)",
    description=(
        "Permite que o jogador que criou a mesa inicie a partida. Ao iniciar, o sistema embaralha "
        "o baralho e distribui duas cartas para cada jogador, uma de cada vez, em ordem.\n\n"
        "**Regras e Validações:**\n"
        "- A partida deve existir (retorna 404 se inexistente).\n"
        "- Somente o criador da mesa pode iniciá-la (retorna 403 para os demais).\n"
        "- A partida não pode ter sido iniciada antes (retorna 409).\n"
        "- São necessários pelo menos 2 jogadores na mesa (retorna 409).\n\n"
        "A resposta traz apenas as cartas do próprio jogador que iniciou a partida."
    ),
    responses={
        200: {"description": "Partida iniciada e cartas distribuídas.", "model": InicioPartidaResponse},
        403: {"description": "Jogador sem autorização para iniciar a partida.", "model": InicioPartidaResponse},
        404: {"description": "Partida não encontrada.", "model": InicioPartidaResponse},
        409: {
            "description": "Conflito: partida já iniciada ou jogadores insuficientes.",
            "model": InicioPartidaResponse,
        },
    },
)
def iniciar_a_partida(
    idPartida: int = Path(..., description="Identificador único da partida a ser iniciada.", examples=[2]),
    idJogador: int = Query(..., description="Identificador do jogador que criou a mesa.", examples=[10]),
):
    try:
        distribuicao = iniciar_partida(id_partida=idPartida, id_jogador=idJogador)
    except InicioPartidaError as erro:
        return JSONResponse(
            status_code=erro.status_code,
            content=InicioPartidaResponse(
                sucesso=False,
                mensagem=erro.mensagem,
                idPartida=idPartida,
                idJogador=idJogador,
            ).model_dump(),
        )

    mao = distribuicao.maos.get(idJogador)
    return InicioPartidaResponse(
        sucesso=True,
        mensagem=f"Partida {idPartida} iniciada. As cartas foram distribuídas.",
        idPartida=idPartida,
        idJogador=idJogador,
        numeroMao=distribuicao.numero_mao,
        jogadores=list(distribuicao.maos),
        cartasPorJogador=CARTAS_POR_JOGADOR,
        suasCartas=mao.visualizar_cartas() if mao else [],
    )
