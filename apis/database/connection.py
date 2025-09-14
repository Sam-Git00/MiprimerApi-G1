"""
Módulo de conexión a base de datos
Configuración de SQLAlchemy para conectar a SQL Server
"""

import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv('SQL_SERVER_CONNECTION_STRING')
if not DATABASE_URL:
    # String de conexión por defecto para SQL Server con SQLAlchemy
    DATABASE_URL = (
        "mssql+pyodbc://localhost/BancoAPI?"
        "driver=ODBC+Driver+17+for+SQL+Server&"
        "TrustServerCertificate=yes&"
        "Encrypt=yes"
    )

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver las queries SQL en consola
    pool_pre_ping=True,
    pool_recycle=300
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

class DatabaseConfig:
    """Configuración de base de datos"""
    
    def __init__(self):
        self.database_url: Optional[str] = DATABASE_URL
        self.database_type: str = "sqlserver"
        
    def get_connection_string(self) -> str:
        """Obtener string de conexión"""
        if self.database_url:
            return self.database_url
        return "memory://localhost"
    
    def is_memory_db(self) -> bool:
        """Verificar si se está usando base de datos en memoria"""
        return self.database_type == "memory" or not self.database_url

# Instancia global de configuración
db_config = DatabaseConfig()

def get_database_status() -> dict:
    """Obtener estado de la base de datos"""
    return {
        "type": db_config.database_type,
        "connection": db_config.get_connection_string(),
        "is_memory": db_config.is_memory_db(),
        "status": "connected" if not db_config.is_memory_db() else "not_configured"
    }

def get_db():
    """Obtener una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
