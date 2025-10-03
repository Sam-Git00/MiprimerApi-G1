import uuid
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base

class Cuentas(Base):
    """
    Modelo de Cuenta Bancaria
    """
    __tablename__ = "cuentas"

    idCuenta = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    idCliente = Column(UUID(as_uuid=True), ForeignKey("clientes.idCliente"), nullable=False)

    numeroCuenta = Column(String, unique=True, nullable=False, index=True)
    tipoCuenta = Column(String, nullable=False)  # Ahorros / Corriente
    estado = Column(String, default="Activa")
    saldo = Column(Numeric(14, 2), default=0.00)

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones
    cliente = relationship("Clientes", back_populates="cuentas")
    transacciones = relationship("Transacciones", back_populates="cuenta")
    tarjeta = relationship("Tarjetas", back_populates="cuenta")

