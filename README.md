# API de Pôquer - Engenharia de Software

Este repositório contém a implementação de uma API RESTful para um sistema de gestão de partidas de Pôquer, desenvolvida como requisito para a disciplina de Engenharia de Software.

## 👥 Equipa
- Emanuel Khalil Fernandes Novaes Angelim
- Luiz Henrique Padilha Cavalcante
- Vitor Leite Medrado Cavalcante
- Jair Ribeiro da Silva Junior

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python 3
- **Framework:** FastAPI
- **Servidor ASGI:** Uvicorn

## ⚙️ Como executar o projeto localmente

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/Khalilemanuel/api-poker-es.git](https://github.com/Khalilemanuel/api-poker-es.git)
   cd api-poker-es

   python -m venv venv

# Criar e ativar um ambiente virtual (recomendado):

No Windows:
venv\Scripts\activate

No Linux/Mac:
source venv/bin/activate

# Instalar as dependências:
pip install -r requirements.txt

# Executar a API:
uvicorn main:app --reload

# 📚 Documentação da API (Swagger)
O FastAPI gera a documentação interativa da API de forma automática. Com o servidor a correr localmente, aceda no seu navegador a:

Interface Swagger UI: http://127.0.0.1:8000/docs

Interface ReDoc: http://127.0.0.1:8000/redoc
