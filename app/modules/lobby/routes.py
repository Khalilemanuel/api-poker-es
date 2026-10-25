from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.modules.lobby.schemas import EntradaPartidaResponse
from app.modules.lobby.services import EntradaPartidaError, entrar_partida

router = APIRouter(tags=["Lobby e Mesas"])

@router.post(
    "/{idPartida}/entrar",
    response_model=EntradaPartidaResponse,
    status_code=status.HTTP_200_OK,
)
def entrar_na_partida(idPartida: int, idJogador: int):
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