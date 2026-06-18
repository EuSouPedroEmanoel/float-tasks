# PROJETO TO DO LIST - BACKEND (FASTAPI)
Este repositório contém uma API de gerenciamento de tarefas (To-Do List) desenvolvida com FastAPI, focada em performance e facilidade de manutenção.
## Pré-requisitos
Para rodar este projeto, você precisará dos seguintes itens instalados em sua máquina:
 * Python 3.14 ou superior
 * Poetry (gerenciador de dependências e ambientes virtuais)
 * pipx (recomendado para gerenciar o Poetry)
## Instalação
O projeto utiliza o Poetry para gerenciar bibliotecas. Instale-as com o comando abaixo:
```bash
# Instalar dependências principais
poetry install

# Caso deseje instalar as dependências de desenvolvimento (testes e linters)
poetry install --with dev

```
## Como executar
Para iniciar a aplicação, utilize o comando definido no gerenciador de tarefas:
```bash
task run

```
A API estará rodando em [http://127.0.0.1:8000](http://127.0.0.1:8000).
## Documentação da API
O FastAPI gera automaticamente documentação interativa baseada nos seus endpoints:
 * **Swagger UI:** Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para testar os endpoints diretamente no navegador.
 * **Redoc:** Acesse [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) para uma documentação mais detalhada.
## Qualidade de Código e Testes
O projeto utiliza o taskipy para facilitar a execução de comandos de manutenção e qualidade:
 * **Formatar o código:**
   ```bash
   
   ```
task format
```
- **Executar linters:**
  ```bash
  task lint

```
 * **Executar testes:**
   ```bash
   task test
   
   ```
```

## Estrutura do Projeto

```text
.
├── todolist/         # Módulo principal da aplicação
├── tests/            # Testes automatizados
├── pyproject.toml    # Configurações do Poetry, dependências e tasks
└── README.md         # Documentação do projeto

```