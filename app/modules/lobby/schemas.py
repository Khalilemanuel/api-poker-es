from pydantic import BaseModel, Field


class Partida(BaseModel):
    id: int
    jogadores: list[int] = Field(default_factory=list)
    max_jogadores: int = Field(6, ge=2)
    iniciada: bool = False
    id_criador: int | None = None


class EntradaPartidaResponse(BaseModel):
    sucesso: bool
    mensagem: str
    idPartida: int
    idJogador: int


class PartidaAbertaResponse(BaseModel):
    """Schema de resposta para a consulta de partidas abertas/disponíveis (US09)."""
    id: int = Field(..., description="Identificador único da partida.", examples=[1])
    idPartida: int | None = Field(default=None, description="Identificador único da partida (alias de compatibilidade).", examples=[1])
    participantesAtuais: int = Field(..., description="Quantidade de participantes atualmente na mesa.", examples=[2])
    participantes_atuais: int | None = Field(default=None, description="Quantidade de participantes atualmente na mesa (snake_case).", examples=[2])
    numeroMaximoPermitidos: int = Field(..., description="Número máximo de participantes permitidos na mesa.", examples=[6])
    numero_maximo_permitidos: int | None = Field(default=None, description="Número máximo de participantes permitidos (snake_case).", examples=[6])
    numeroMaximoPermitido: int | None = Field(default=None, description="Número máximo permitido (singular).", examples=[6])
    max_jogadores: int | None = Field(default=None, description="Capacidade máxima de jogadores da mesa.", examples=[6])
    jogadores: list[int] = Field(default_factory=list, description="Lista dos IDs dos jogadores atualmente na mesa.", examples=[[10, 11]])

    @classmethod
    def from_partida(cls, partida: Partida) -> "PartidaAbertaResponse":
        total_jogadores = len(partida.jogadores)
        return cls(
            id=partida.id,
            idPartida=partida.id,
            participantesAtuais=total_jogadores,
            participantes_atuais=total_jogadores,
            numeroMaximoPermitidos=partida.max_jogadores,
            numero_maximo_permitidos=partida.max_jogadores,
            numeroMaximoPermitido=partida.max_jogadores,
            max_jogadores=partida.max_jogadores,
            jogadores=list(partida.jogadores),
        )

