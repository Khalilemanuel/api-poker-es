import re
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


def validar_senha_forte(v: str) -> str:
    """Valida se a senha atende aos requisitos de segurança: maiúscula, número e caractere especial."""
    if len(v) < 6:
        raise ValueError("A senha deve ter no mínimo 6 caracteres.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r"[0-9]", v):
        raise ValueError("A senha deve conter pelo menos um número.")
    if not re.search(r"[^a-zA-Z0-9]", v):
        raise ValueError("A senha deve conter pelo menos um caractere especial (ex: @, #, $, !, etc.).")
    return v


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

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return validar_senha_forte(v)


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
    senha: str = Field(..., min_length=6, examples=["SenhaSegura@123"], description="Senha de acesso (mínimo 6 caracteres, 1 maiúscula, 1 número e 1 caractere especial).")
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

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        return validar_senha_forte(v)


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
