from fastapi import FastAPI

app = FastAPI(
    title="API de Pôquer - Engenharia de Software",
    description="API para gerenciamento e partidas do sistema de pôquer.",
    version="0.1.0"
)


@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "online",
        "message": "Bem-vindo à API de Pôquer!",
        "version": "0.1.0"
    }
