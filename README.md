# PROJETO TO DO LIST - backend (FastAPI)

Este repositório contém uma API simples construída com FastAPI.

## Pré-requisitos

- Python 3.14 ou superior
- Poetry (recomendado) ou pip

> As dependências principais são FastAPI e Uvicorn (definidas em pyproject.toml).

## Instalação (usando Poetry)

1. Instale o Poetry (se ainda não tiver):

   python -m pip install --user poetry

2. Instale dependências do projeto:

   poetry install

> Se quiser também instalar dependências de desenvolvimento (linters/tests):

   poetry install --with dev

3. Ative o ambiente do Poetry e execute a aplicação:

   poetry run uvicorn todolist.app:app --reload

## Alternativa (sem Poetry)

1. Crie e ative um ambiente virtual:

   python -m venv .venv
   # Linux / macOS
   source .venv/bin/activate
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1

2. Instale as dependências necessárias:

   pip install "fastapi[standard]" uvicorn

3. Execute a aplicação:

   uvicorn todolist.app:app --reload
   # ou
   python -m uvicorn todolist.app:app --reload

## Como testar

Com a aplicação em execução (por padrão em http://127.0.0.1:8000), abra o navegador ou use curl:

- Abra: http://127.0.0.1:8000/
- Ou via terminal:

  curl http://127.0.0.1:8000/

Você deve receber uma resposta JSON: {"message": "olá mundo"}

## Executando testes

Se instalou dependências de desenvolvimento, execute os testes com:

- Usando Poetry:

  poetry run pytest -s -x --cov=todolist -vv

- Ou, se preferir, usando taskipy (definido em pyproject.toml):

  poetry run task test


---

Se quiser que eu adicione instruções específicas para Docker, deployment ou GitHub Actions, diga qual opção prefere que eu inclua.