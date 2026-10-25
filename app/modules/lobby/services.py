from fastapi import status

from app.modules.lobby.schemas import EntradaPartidaResponse, Partida


class EntradaPartidaError(Exception):
    def __init__(self, mensagem: str, status_code: int):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code

partidas: dict[int, Partida] = {
    1: Partida(id=1),
    2: Partida(id=2, jogadores=[10, 11], max_jogadores=2),
    3: Partida(id=3, jogadores=[20, 21], iniciada=True),
}

def entrar_partida(id_partida: int, id_jogador: int) -> EntradaPartidaResponse:
    partida = partidas.get(id_partida)

    if partida is None:
        raise EntradaPartidaError("Partida não encontrada.", status.HTTP_404_NOT_FOUND)

    if id_jogador in partida.jogadores:
        raise EntradaPartidaError("O jogador já está nesta partida.", status.HTTP_409_CONFLICT)

    if partida.iniciada:
        raise EntradaPartidaError("A partida já foi iniciada.", status.HTTP_409_CONFLICT)

    if len(partida.jogadores) >= partida.max_jogadores:
        raise EntradaPartidaError("A mesa está cheia.", status.HTTP_409_CONFLICT)

    partida.jogadores.append(id_jogador)

    return EntradaPartidaResponse(
        sucesso=True,
        mensagem=f"Jogador {id_jogador} entrou na partida {id_partida}.",
        idPartida=id_partida,
        idJogador=id_jogador,
    )
