# Tatame — BJJ Game Mapping Tool

A personal BJJ game mapping tool that organizes techniques and positions as cards, enabling players to build and visualize their game plan.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy + Alembic
- **Auth:** JWT (python-jose) + bcrypt (passlib)

## Features

- JWT authentication (register/login)
- Positions CRUD
- Cards CRUD (nested under positions)
- Deck management (active game plan)
- Training sessions with cards tracking
- User profile management

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL

### Installation

```bash
git clone https://github.com/RenanGonzales/tatame-backend.git
cd tatame-backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user@localhost:5432/tatame
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database

```bash
alembic upgrade head
```

### Run

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

## Frontend

[tatame-frontend](https://github.com/RenanGonzales/tatame-frontend)

---

# Tatame — Ferramenta de Mapeamento de Jogo de BJJ

Ferramenta pessoal para mapear o jogo de BJJ, organizando técnicas e posições como cartas para construir e visualizar o game plan.

## Stack

- **Framework:** FastAPI
- **Banco de dados:** PostgreSQL
- **ORM:** SQLAlchemy + Alembic
- **Auth:** JWT (python-jose) + bcrypt (passlib)

## Funcionalidades

- Autenticação JWT (cadastro/login)
- CRUD de posições
- CRUD de cartas (aninhado em posições)
- Gerenciamento de deck (game plan ativo)
- Sessões de treino com cartas utilizadas
- Gerenciamento de perfil do usuário

## Como Rodar

### Pré-requisitos

- Python 3.11+
- PostgreSQL

### Instalação

```bash
git clone https://github.com/RenanGonzales/tatame-backend.git
cd tatame-backend

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Variáveis de Ambiente

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql://user@localhost:5432/tatame
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Banco de Dados

```bash
alembic upgrade head
```

### Rodar

```bash
uvicorn app.main:app --reload
```

Documentação da API disponível em `http://localhost:8000/docs`

## Frontend

[tatame-frontend](https://github.com/RenanGonzales/tatame-frontend)