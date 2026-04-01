# My Mini Blog API

Uma API RESTful desenvolvida em Python para gerenciamento de um mini-blog. Este projeto foi construído para aplicar conceitos de arquitetura de sistemas, autenticação e gerenciamento de banco de dados.

## Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** FastAPI
* **ORM / Banco de Dados:** SQLModel (SQLAlchemy) / SQLite 
* **Autenticação:** JWT
* **Gerenciamento de Dependências:** Poetry
* **Testes:** Pytest

## Funcionalidades

* **Gerenciamento de Usuários:** Criação, leitura, atualização e exclusão de contas de usuário.
* **Autenticação:** Login via token JWT.
* **Postagens:** Usuários autenticados podem criar, editar, listar e deletar suas postagens.
* **Comentários:** Sistema de comentários contidos nas postagens, com controle de permissões.

---

## Executar o Projeto Localmente

### Pré-requisitos

* [Python 3.11+](https://www.python.org/downloads/) (Verifique a versão exata no `pyproject.toml`)
* [Poetry](https://python-poetry.org/docs/#installation) para gerenciamento de pacotes.

### Passos para Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/JerryInterestelar/My-Mini-Blog
   cd my-mini-blog

2. Instale as dependências do projeto utilizando o Poetry:
   ```bash
   poetry install
   ```

3. Ative o ambiente virtual:
   ```bash
   poetry shell
   ```

4. Configuração das Variáveis de Ambiente:
   
   Crie um arquivo `.env` na raiz do projeto ou exporte a variável da chave secreta. O banco de dados SQLite será gerado automaticamente.
   ```bash
   # Exemplo de variáveis
   SECRET_KEY="sua_chave_secreta_aqui"
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   fastapi dev app/main.py
   ```

## Utilização da API

Com o servidor rodando, a documentação nativa do FastAPI com Swagger UI é gerada automaticamente. Será utilizado essa interface para explorar e testar os endpoints.

1. Acesse `http://localhost:8000/docs` no seu navegador.
2. Crie uma conta de usuário utilizando o endpoint `POST /users/`.
3. Faça login no endpoint `POST /auth/token` utilizando o email e senha cadastrados para receber seu token JWT de acesso.
4. No topo da página do Swagger, clique no botão **"Authorize"** e insira suas credenciais (ou o token gerado) para liberar o acesso aos endpoints protegidos.
5. Agora é possível criar posts em `POST /posts/` e adicionar comentários navegando para `POST /posts/{post_id}/comments`.

## Executando os Testes

O projeto possui um conjunto de testes automatizados, utilizando um banco de dados em memória para não interferir nos dados reais.

Para executar todos os testes, rode este comando na raiz do projeto:
```bash
pytest -v
```

## Estrutura do Projeto

A estrutura de arquivos foi dividida em camadas para separar as responsabilidades e facilitar a manutenção.

```text
app/
├── core/         # Configurações gerais, injeção de dependências, segurança e setup do BD
├── models/       # Definição das tabelas do banco de dados
├── routers/      # Endpoints da API
├── schemas/      # Modelos Pydantic para validação de entrada e serialização de saída
└── services/     # Regras de negócio, lógica de aplicação e operações de banco
tests/            # Suíte de testes separados por domínio e fixtures em conftest.py
```
