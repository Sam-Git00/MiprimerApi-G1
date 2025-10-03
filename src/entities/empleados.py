import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class Empleados(Base):
    """
    Modelo de Empleados del Banco
    """
    __tablename__ = "empleados"

    idEmpleado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False, index=True)
    cargo = Column(String, nullable=False)  # Cajero, Asesor, Gerente
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String)
    activo = Column(Boolean, default=True)

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)
