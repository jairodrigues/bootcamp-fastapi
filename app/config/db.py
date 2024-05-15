
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from ..schemas.assistant import Base

# método singleton
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

            #Esta variável contém a URL de conexão com o banco de dados SQLite.
            SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

            # O `engine` é responsável por criar a conexão com o banco de dados SQLite.
            cls._instance.engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

            # `SessionLocal` é uma fábrica de sessões que será utilizada para interagir com o banco de dados.
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)

            # # Este comando cria as tabelas no banco de dados com base nos modelos definidos.
            Base.metadata.create_all(bind=cls._instance.engine)

            return cls._instance
    