import random

from app.modules.motorpartida.cartas import Carta, Naipe, ValorCarta


class BaralhoVazioError(Exception):
    pass


class Baralho:
    def __init__(self, gerador: random.Random | None = None):
        self._gerador = gerador or random.SystemRandom()
        self._cartas: list[Carta] = [
            Carta(naipe=naipe, valor=valor) for naipe in Naipe for valor in ValorCarta
        ]

    @property
    def cartas(self) -> list[Carta]:
        return list(self._cartas)

    def __len__(self) -> int:
        return len(self._cartas)

    def embaralhar(self) -> None:
        self._gerador.shuffle(self._cartas)

    def comprar(self) -> Carta:
        if not self._cartas:
            raise BaralhoVazioError("Não há mais cartas no baralho.")
        return self._cartas.pop()

    def queimar(self) -> None:
        self.comprar()
