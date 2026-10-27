# Contexto do Projeto: Implementação da US09 (Consulta de Partidas Disponíveis)

> **Arquivo de Engenharia de Contexto**  
> **Objetivo:** Fornecer um resumo denso, estruturado e semanticamente rico das decisões, alterações e estado atual da base de código para desenvolvedores e agentes de IA.

---

## 1. Identificação e Metadados
- **Repositório:** `api-poker-es` (GitHub: `Khalilemanuel/api-poker-es`)
- **Projeto:** API RESTful para Sistema de Gestão de Partidas de Pôquer
- **Disciplina/Escopo:** Engenharia de Software
- **Autor da Demanda:** Luiz Henrique Padilha Cavalcante (`luizpadilha-collab`)
- **Issue:** [US09 - Consulta de partidas disponíveis #2](https://github.com/Khalilemanuel/api-poker-es/issues/2)
- **Branch de Feature:** `feat/us09-consulta-partidas-disponiveis` (integrada na `main`)

---

## 2. Requisitos e Escopo da US09

| Item | Especificação |
|---|---|
| **História de Usuário** | US09 - Consulta de partidas disponíveis |
| **Endpoint** | `GET /poker/partidasAbertas` |
| **Objetivo** | Retornar lista de partidas abertas com `id`, `participantes atuais` e `número máximo permitidos` |
| **Regra de Negócio Central** | Uma partida é considerada **aberta** se `iniciada == False`. Partidas com `iniciada == True` são excluídas da listagem. |
| **Recurso Opcional de Filtro** | Suporte a query parameter `apenasComVagas: bool = False` para permitir filtrar partidas com vagas remanescentes (`len(jogadores) < max_jogadores`). |

---

## 3. Decisões de Arquitetura e Engenharia

1. **Localização Modular (Pacotes UML):**
   - Inserido no pacote `app/modules/lobby/`, responsável pelo gerenciamento de mesas e salas pré-jogo, alinhado à arquitetura conceitual UML do projeto.
2. **Compatibilidade Ampla de Schemas (CamelCase & SnakeCase):**
   - Criação de `PartidaAbertaResponse` com campos primários no padrão da API (`id`, `participantesAtuais`, `numeroMaximoPermitidos`, `jogadores`) e aliases/campos sincronizados (`idPartida`, `participantes_atuais`, `numero_maximo_permitidos`, `numeroMaximoPermitido`, `max_jogadores`), garantindo interoperabilidade com qualquer consumidor ou suite de testes.
3. **Imutabilidade e Segurança da Fonte de Dados:**
   - A listagem consome a estrutura de dados em memória `partidas: dict[int, Partida]` ordenada deterministicamente por ID, gerando DTOs seguros sem expor ou alterar o estado interno diretamente.

---

## 4. Mapeamento de Arquivos Alterados e Criados

```
├── app/
│   └── modules/
│       └── lobby/
│           ├── schemas.py      # Adicionado PartidaAbertaResponse e factory from_partida()
│           ├── services.py     # Adicionado servico listar_partidas_abertas()
│           └── routes.py       # Registrado endpoint GET /partidasAbertas no router
├── tests/
│   └── test_us09_partidas_abertas.py  # Criada suite com 8 testes automatizados
└── CONTEXT.md                  # Este arquivo de contexto
```

### Detalhes das Modificações
- [`app/modules/lobby/schemas.py`](file:///c:/Users/Notebook/Documents/Projeto_engenharia_de_software/app/modules/lobby/schemas.py):
  - Definição do schema Pydantic `PartidaAbertaResponse`.
  - Método construtor `from_partida(cls, partida: Partida) -> PartidaAbertaResponse` para transformação direta do modelo de domínio.
- [`app/modules/lobby/services.py`](file:///c:/Users/Notebook/Documents/Projeto_engenharia_de_software/app/modules/lobby/services.py):
  - Função `listar_partidas_abertas(apenas_com_vagas: bool = False) -> list[PartidaAbertaResponse]`.
  - Itera sobre `partidas.values()`, descarta as com `iniciada == True` e aplica ordenação por `id`.
- [`app/modules/lobby/routes.py`](file:///c:/Users/Notebook/Documents/Projeto_engenharia_de_software/app/modules/lobby/routes.py):
  - Rota `@router.get("/partidasAbertas")` com `status_code=200`, `response_model=list[PartidaAbertaResponse]` e documentação descritiva para Swagger UI e ReDoc.
- [`tests/test_us09_partidas_abertas.py`](file:///c:/Users/Notebook/Documents/Projeto_engenharia_de_software/tests/test_us09_partidas_abertas.py):
  - 8 testes cobrindo: consulta padrão, exclusão de partidas iniciadas, listas vazias, filtro de vagas, atualização reativa pós-entrada de jogador, transição de estado ao iniciar partida e compatibilidade de aliases.

---

## 5. Contrato da API (`GET /poker/partidasAbertas`)

### Exemplo de Resposta HTTP (200 OK)
```json
[
  {
    "id": 1,
    "idPartida": 1,
    "participantesAtuais": 0,
    "participantes_atuais": 0,
    "numeroMaximoPermitidos": 6,
    "numero_maximo_permitidos": 6,
    "numeroMaximoPermitido": 6,
    "max_jogadores": 6,
    "jogadores": []
  },
  {
    "id": 2,
    "idPartida": 2,
    "participantesAtuais": 2,
    "participantes_atuais": 2,
    "numeroMaximoPermitidos": 2,
    "numero_maximo_permitidos": 2,
    "numeroMaximoPermitido": 2,
    "max_jogadores": 2,
    "jogadores": [10, 11]
  }
]
```

---

## 6. Rastreabilidade Git (Commits & Fluxo)

A entrega seguiu estritamente a convenção de commits atômicos do projeto:

| Hash | Mensagem do Commit | Escopo |
|---|---|---|
| `d049ae0` | `feat(us09): definir schema para consulta de partidas abertas` | Schemas |
| `88a839b` | `feat(us09): implementar servico para listar partidas abertas` | Serviços |
| `7808d38` | `feat(us09): disponibilizar endpoint GET /poker/partidasAbertas no modulo lobby` | Rotas |
| `16d18b8` | `test(us09): adicionar testes cobrindo consulta de partidas abertas` | Testes |

**Fluxo de Ramos:**
1. Ramo de trabalho criado a partir da `main` atualizada: `feat/us09-consulta-partidas-disponiveis`.
2. Publicado no remoto: `origin/feat/us09-consulta-partidas-disponiveis`.
3. Integrado à branch principal `main` via merge fast-forward e enviado para `origin/main`.

---

## 7. Verificação e Qualidade (Testes)
- **Comando de Teste:** `pytest` (ou `python -m pytest`)
- **Total de Testes da Aplicação:** 47 testes (100% aprovados)
  - `tests/test_us01_cadastro_jogadores.py`: 10 testes
  - `tests/test_us09_partidas_abertas.py`: 8 testes
  - `tests/test_us10_entrar_partida.py`: 6 testes
  - `tests/test_us12_iniciar_partida.py`: 11 testes
  - `tests/test_us13_distribuicao_cartas.py`: 12 testes

---

## 8. Como Executar Localmente
```bash
# Ativar o ambiente virtual:
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Linux/Mac

# Executar a suíte de testes:
python -m pytest

# Iniciar o servidor de desenvolvimento:
uvicorn main:app --reload
# Swagger disponível em: http://127.0.0.1:8000/docs
```
