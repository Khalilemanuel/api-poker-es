import sys
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path mesmo se executado diretamente
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastapi import FastAPI
from app.core.config import PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_VERSION, API_PREFIX
from app.modules.autenticacao.routes import router as auth_router
from app.modules.usuarios.routes import router as usuarios_router
from app.modules.lobby.routes import router as lobby_router
from app.modules.motorpartida.routes import router as motor_router
from app.modules.estatisticas.routes import router as estatisticas_router
from app.modules.administracao.routes import router as admin_router

app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
)


@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "online",
        "message": "Bem-vindo à API de Pôquer!",
        "version": PROJECT_VERSION,
    }


# Registro dos roteadores modulares alinhados aos pacotes UML do projeto
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(usuarios_router, prefix=API_PREFIX)
app.include_router(lobby_router, prefix=API_PREFIX)
app.include_router(motor_router, prefix=API_PREFIX)
app.include_router(estatisticas_router, prefix=API_PREFIX)
app.include_router(admin_router, prefix=API_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

