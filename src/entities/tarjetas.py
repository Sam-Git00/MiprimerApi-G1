import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class Tarjetas(Base):
    """
    Modelo de Tarjeta Bancaria
    """
    __tablename__ = "tarjetas"

    idTarjeta = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    idCuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.idCuenta"), nullable=False)

    numeroTarjeta = Column(String, unique=True, nullable=False, index=True)
    tipo = Column(String, nullable=False)  # Débito, Crédito
    limiteCredito = Column(Float, nullable=True)
    saldoDisponible = Column(Float, default=0.0)
    estado = Column(String, default="Activa")
    fechaExpiracion = Column(DateTime)

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones
    cuenta = relationship("Cuentas", back_populates="tarjeta")
