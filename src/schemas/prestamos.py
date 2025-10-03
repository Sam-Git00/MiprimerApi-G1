"""
Pydantic schemas for Medico entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PrestamoBase(BaseModel):
    """Base schema for Prestamo with common fields."""
    idCliente: UUID
    idEmpleado: UUID
    montoPrestamo: float
    interes: float
    plazoMeses: int
    estado: str


class PrestamoCreate(PrestamoBase):
    """Schema for creating a new Prestamo."""

    pass


class PrestamoResponse(PrestamoBase):
    """Schema for Prestamo response."""
    idPrestamo: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
