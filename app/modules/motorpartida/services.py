from dataclasses import dataclass

from fastapi import status

from app.modules.lobby.services import partidas
from app.modules.motorpartida.baralho import Baralho
from app.modules.motorpartida.distribuicao import MaoJogador, distribuir_cartas

MIN_JOGADORES = 2


class InicioPartidaError(Exception):
    def __init__(self, mensagem: str, status_code: int):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status_code = status_code


@dataclass
class DistribuicaoPartida:
    numero_mao: int
    baralho: Baralho
    maos: dict[int, MaoJogador]


distribuicoes: dict[int, DistribuicaoPartida] = {}


def nova_mao(id_partida: int, jogadores: list[int], baralho: Baralho | None = None) -> DistribuicaoPartida:
    baralho = baralho or Baralho()
    baralho.embaralhar()
    anterior = distribuicoes.get(id_partida)
    distribuicao = DistribuicaoPartida(
        numero_mao=anterior.numero_mao + 1 if anterior else 1,
        baralho=baralho,
        maos=distribuir_cartas(jogadores, baralho),
    )
    distribuicoes[id_partida] = distribuicao
    return distribuicao


def iniciar_partida(id_partida: int, id_jogador: int) -> DistribuicaoPartida:
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

    distribuicao = nova_mao(id_partida, list(partida.jogadores))
    partida.iniciada = True
    return distribuicao
