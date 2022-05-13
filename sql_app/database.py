from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv  import load_dotenv, find_dotenv
import os

# Carregando variaveis de usuario e senha
load_dotenv(find_dotenv())
USER_DB  = os.environ.get("USER")
PASSW_DB = os.environ.get("PASSW")

#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "mysql://{USER_DB}:{PASSW_DB}@localhost/db_api"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()