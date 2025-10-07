import uuid
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base

class Transacciones(Base):
    """
    Modelo de Transacción Bancaria
    """
    __tablename__ = "transacciones"

    idTransaccion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    idCuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.idCuenta"), nullable=False)

    tipo = Column(String, nullable=False)  # depósito, retiro, transferencia
    monto = Column(Numeric(14, 2), nullable=False)
    descripcion = Column(String)
    fecha = Column(DateTime)

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones
    cuenta = relationship("Cuentas", back_populates="transacciones")
