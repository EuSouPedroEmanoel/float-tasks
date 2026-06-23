
# 🧠 Mind Map To-Do List (Backend) — Em Desenvolvimento

Este repositório é um **laboratório de estudos** focado no aprendizado de **FastAPI** e ferramentas do ecossistema Python para testes e qualidade de código. 

A proposta do projeto é desenvolver o backend de uma aplicação de gerenciamento de tarefas **orientada a mapas mentais**. Diferente de listas de tarefas tradicionais e lineares, a API está sendo projetada para gerenciar tarefas estruturadas em formato de **árvore (grafos)**, permitindo que cada tarefa possua sub-tarefas aninhadas infinitamente.

---

## 🚀 Status do Projeto: 🛠️ Em Desenvolvimento (Fase de Estudo)
O projeto encontra-se na fase inicial de especificação e estudos arquiteturais. O objetivo principal no momento é consolidar conceitos de rotas assíncronas, modelagem de dados hierárquicos e, principalmente, a **escrita de testes automatizados e linters** antes de fechar o MVP (MínO que estou praticando aqui:**
* Configuração de ambiente moderno com **Poetry**.
* Automação de tarefas de desenvolvimento com **Taskipy**.
* Estruturação de suíte de testes com **Pytest**.
* Análise estática de código e formatação (linters).

---

## 🏗️ Principais Diferenciais Técnicos (Planejados)
* **Estrutura Hierárquica (Árvore):** Modelagem de dados baseada em Lista de Adjacência para nós filhos e pais.
* **Endpoints Estratégicos:** Rotas para retornar dados formatados em árvores aninhadas (JSON recursivo) e movimentação dinâmica de nós.
* **Performance:** Operações assíncronas nativas com FastAPI.

---

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:
* [Python 3.12+](https://www.python.org/)
* [Poetry](https://python-poetry.org/) (Gerenciador de dependências e ambientes virtuais)
* [pipx](https://github.com/pypa/pipx) (Recomendado para isolar e gerenciar a instalação do Poetry)

---

## 🚀 Instalação e Configuração

O projeto utiliza o **Poetry** para gerenciar as bibliotecas e o ambiente virtual de forma isolada.

```bash
# 1. Clone o repositório
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio

# 2. Instalar apenas as dependências principais de produção
poetry install

# 3. Instalar também as dependências de desenvolvimento (testes e ferramentas de qualidade)
poetry install --with dev

```

---

## 🏃 Como Executar

Para iniciar o servidor de desenvolvimento, utilize o atalho configurado via `taskipy`:

```bash
poetry run task run

```

A API estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📖 Documentação da API

O FastAPI gera automaticamente documentações interativas excelentes para testar os endpoints diretamente do navegador assim que criados:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Ideal para testar as requisições em tempo real)
* **Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (Documentação técnica mais limpa e detalhada)

---

## 🧪 Qualidade de Código e Testes

Um dos focos principais deste repositório é aplicar ferramentas que auxiliam na automação de testes e checagem de qualidade. Utilizamos o `taskipy` para simplificar esses comandos:

```bash
# Formatar o código automaticamente (ex: Black/Ruff)
poetry run task format

# Executar linters para análise estática de código (ex: Flake8/Ruff/Mypy)
poetry run task lint

# Executar a suíte de testes automatizados com Pytest
poetry run task test

```

---

## 📂 Estrutura de Pastas

```text
.
├── todolist/         # Módulo principal da aplicação (regras de negócio, rotas e modelos)
├── tests/            # Testes automatizados (onde estou focando os estudos de pytest)
├── pyproject.toml    # Configurações do Poetry, definições de linters e tasks do taskipy
└── README.md         # Documentação oficial do projeto

```
