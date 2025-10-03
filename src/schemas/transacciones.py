"""
Pydantic schemas for Paciente entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TransaccionBase(BaseModel):
    """Base schema for Transaccion with common fields."""

    idCuenta: UUID
    tipo: str
    monto: float
    fecha: datetime
    descripcion: str


class TransaccionCreate(TransaccionBase):
    """Schema for creating a new Transaccion."""

    pass


class TransaccionResponse(TransaccionBase):
    """Schema for Transaccion response."""

    idTransaccion: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
