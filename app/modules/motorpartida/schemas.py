from pydantic import BaseModel, Field

from app.modules.motorpartida.cartas import Carta


class InicioPartidaResponse(BaseModel):
    sucesso: bool
    mensagem: str
    idPartida: int
    idJogador: int
    numeroMao: int | None = None
    jogadores: list[int] = Field(default_factory=list)
    cartasPorJogador: int | None = None
    suasCartas: list[Carta] = Field(default_factory=list)
