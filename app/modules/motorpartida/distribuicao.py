from app.modules.motorpartida.baralho import Baralho
from app.modules.motorpartida.cartas import Carta

CARTAS_POR_JOGADOR = 2


class MaoJogador:
    def __init__(self, id_jogador: int):
        self.id_jogador = id_jogador
        self._cartas: list[Carta] = []

    def receber_carta(self, carta: Carta) -> None:
        if len(self._cartas) >= CARTAS_POR_JOGADOR:
            raise ValueError(f"O jogador {self.id_jogador} já recebeu suas {CARTAS_POR_JOGADOR} cartas.")
        self._cartas.append(carta)

    def visualizar_cartas(self) -> list[Carta]:
        return list(self._cartas)


def distribuir_cartas(jogadores: list[int], baralho: Baralho) -> dict[int, MaoJogador]:
    if not jogadores:
        raise ValueError("Não há jogadores para receber cartas.")
    if len(set(jogadores)) != len(jogadores):
        raise ValueError("Há jogadores repetidos na distribuição.")
    if len(baralho) < len(jogadores) * CARTAS_POR_JOGADOR:
        raise ValueError("O baralho não tem cartas suficientes para todos os jogadores.")

    maos = {id_jogador: MaoJogador(id_jogador) for id_jogador in jogadores}
    for _ in range(CARTAS_POR_JOGADOR):
        for id_jogador in jogadores:
            maos[id_jogador].receber_carta(baralho.comprar())
    return maos
