import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.connection import Base


class Cheques(Base):
    """
    Modelo de Cheque Bancario
    """
    __tablename__ = "cheques"

    idCheque = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    idCliente = Column(UUID(as_uuid=True), ForeignKey("clientes.idCliente"), index=True)

    fechaEmision = Column(DateTime, index=True)
    fechaCobro = Column(Date, index=True, nullable=True)
    monto = Column(String, nullable=False)
    motivo = Column(String)

    # Auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    id_usuario_actualizacion = Column(UUID(as_uuid=True), ForeignKey("empleados.idEmpleado"))
    fecha_creacion = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    # Relaciones
    cliente = relationship("Clientes", back_populates="cheques")
