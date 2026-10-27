from enum import Enum

from pydantic import BaseModel


class Naipe(str, Enum):
    COPAS = "COPAS"
    OUROS = "OUROS"
    ESPADAS = "ESPADAS"
    PAUS = "PAUS"


class ValorCarta(str, Enum):
    DOIS = "2"
    TRES = "3"
    QUATRO = "4"
    CINCO = "5"
    SEIS = "6"
    SETE = "7"
    OITO = "8"
    NOVE = "9"
    DEZ = "10"
    VALETE = "J"
    DAMA = "Q"
    REI = "K"
    AS = "A"


class Carta(BaseModel, frozen=True):
    naipe: Naipe
    valor: ValorCarta

    def __str__(self) -> str:
        return f"{self.valor.value} de {self.naipe.value}"
