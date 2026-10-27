from pydantic import BaseModel, Field


class Partida(BaseModel):
    id: int
    jogadores: list[int] = Field(default_factory=list)
    max_jogadores: int = Field(6, ge=2)
    iniciada: bool = False


class EntradaPartidaResponse(BaseModel):
    sucesso: bool
    mensagem: str
    idPartida: int
    idJogador: int
