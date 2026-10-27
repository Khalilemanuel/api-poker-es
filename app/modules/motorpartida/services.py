from fastapi import status

from app.modules.lobby.schemas import Partida
from app.modules.lobby.services import partidas

MIN_JOGADORES = 2


class InicioPartidaError(Exception):
    def __init__(self, mensagem: str, status_code: int):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code


def iniciar_partida(id_partida: int, id_jogador: int) -> Partida:
    partida = partidas.get(id_partida)

    if partida is None:
        raise InicioPartidaError("Partida não encontrada.", status.HTTP_404_NOT_FOUND)

    if partida.id_criador != id_jogador:
        raise InicioPartidaError(
            "Apenas o jogador que criou a mesa pode iniciar a partida.", status.HTTP_403_FORBIDDEN
        )

    if partida.iniciada:
        raise InicioPartidaError("A partida já foi iniciada.", status.HTTP_409_CONFLICT)

    if len(partida.jogadores) < MIN_JOGADORES:
        raise InicioPartidaError(
            f"São necessários pelo menos {MIN_JOGADORES} jogadores para iniciar a partida.",
            status.HTTP_409_CONFLICT,
        )

    partida.iniciada = True
    return partida
