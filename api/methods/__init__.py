from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Crear el motor de base de datos
engine = create_engine('sqlite:///./db/tfinal.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)