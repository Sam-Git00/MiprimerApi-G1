import uuid
from sqlalchemy import Column, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class Clientes(Base):
    """
    Modelo de Cliente Bancario
    """
    __tablename__ = "clientes"

    idCliente = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Datos personales del cliente
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False, index=True)  # cédula/NIT
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String, unique=True)
    fechaNacimiento = Column(Date)

    # Auditoría (si quieres que solo empleados puedan crear/modificar clientes)
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones con las entidades financieras
    cuentas = relationship("Cuentas", back_populates="cliente")
    prestamos = relationship("Prestamos", back_populates="cliente")
    tarjetas = relationship("Tarjetas", back_populates="cliente")
    inversiones = relationship("Inversiones", back_populates="cliente")
    cheques = relationship("Cheques", back_populates="cliente")
