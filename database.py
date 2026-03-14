"""
database.py
-----------
Configura a conexão com o PostgreSQL via SQLAlchemy.
Lê as credenciais do arquivo .env para manter segurança.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Carrega variáveis do arquivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "gerenciador_cursos")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# String de conexão com o PostgreSQL
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine principal — responsável pela comunicação com o banco
engine = create_engine(DATABASE_URL, echo=False)

# Fábrica de sessões — cada sessão representa uma transação
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM do projeto."""
    pass


def get_session():
    """Retorna uma sessão ativa com o banco de dados."""
    return SessionLocal()
