"""
Pydantic schemas for Paciente entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TarjetaBase(BaseModel):
    """Base schema for Tarjeta with common fields."""

    idCuenta: UUID
    numeroTarjeta: str
    tipo: str
    limiteCredito: float
    saldoDisponible: float
    fechaExpiracion: datetime
    estado: str


class TarjetaCreate(TarjetaBase):
    """Schema for creating a new Tarjeta."""

    pass


class TarjetaResponse(TarjetaBase):
    """Schema for Tarjeta response."""

    idTarjeta: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
