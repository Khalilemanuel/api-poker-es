import re
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


class Credenciais(BaseModel):
    """Classe 7 do Diagrama UML - Credenciais de acesso."""
    email: str = Field(..., description="E-mail único de acesso do usuário.")
    senha: str = Field(..., min_length=6, description="Senha do usuário (mínimo de 6 caracteres).")

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Formato de e-mail inválido.")
        return v


class Perfil(BaseModel):
    """Classe 5 e 6 do Diagrama UML - Perfil e Avatar."""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do jogador.")
    username: str = Field(..., min_length=3, max_length=30, description="Nome de exibição exclusivo na mesa.")
    avatar: str = Field(default="avatar_padrao.png", description="Identificador ou URL da imagem do avatar.")


class Jogador(BaseModel):
    """Classe 1 e 3 do Diagrama UML - Dados completos do Jogador registrado."""
    id: int = Field(..., description="Identificador único gerado para o jogador.")
    nome: str
    email: str
    username: str
    avatar: str
    saldo: float = Field(default=1000.0, ge=0, description="Saldo inicial de fichas para apostas.")
    ativo: bool = True


class CadastroJogadorRequest(BaseModel):
    """Payload de entrada para o endpoint de cadastro (US01)."""
    nome: str = Field(..., min_length=2, max_length=100, examples=["Khalil Angelim"], description="Nome completo do jogador.")
    email: str = Field(..., examples=["khalil@poker.com"], description="E-mail único para login.")
    username: str = Field(..., min_length=3, max_length=30, examples=["khalil_pro"], description="Username único para exibição nas partidas.")
    senha: str = Field(..., min_length=6, examples=["senhaSegura123"], description="Senha de acesso (mínimo 6 caracteres).")
    avatar: str | None = Field(default="avatar_padrao.png", examples=["avatar_padrao.png"], description="Nome ou URL do avatar escolhido.")
    saldo_inicial: float = Field(default=1000.0, ge=0, examples=[1000.0], description="Saldo inicial de fichas concedido.")

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not EMAIL_REGEX.match(v):
            raise ValueError("Formato de e-mail inválido.")
        return v

    @field_validator("username")
    @classmethod
    def validar_username(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username deve ter no mínimo 3 caracteres.")
        return v


class CadastroJogadorResponse(BaseModel):
    """Payload de resposta padronizado para o endpoint de cadastro (US01)."""
    sucesso: bool
    mensagem: str
    idJogador: int | None = None
    nome: str | None = None
    email: str | None = None
    username: str | None = None
    avatar: str | None = None
    saldo: float | None = None
