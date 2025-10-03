"""
Pydantic schemas for Cita entity.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChequeBase(BaseModel):
    """Base schema for Cheque with common fields."""

    idCliente: UUID
    fechaEmision: date
    monto: float
    motivo: str


class ChequeCreate(ChequeBase):
    """Schema for creating a new Cheque."""

    pass


class ChequeResponse(ChequeBase):
    """Schema for Cheque response."""

    idCheque: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
