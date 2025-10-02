import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class Prestamos(Base):
    """
    Modelo de Préstamo Bancario
    """
    __tablename__ = "prestamos"

    idPrestamo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    idCliente = Column(UUID(as_uuid=True), ForeignKey("clientes.idCliente"), nullable=False)

    monto = Column(Float, nullable=False)
    interes = Column(Float, nullable=False)
    plazoMeses = Column(String, nullable=False)
    estado = Column(String, default="pendiente")  # pendiente, pagado, vencido

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones
    cliente = relationship("Clientes", back_populates="prestamos")
