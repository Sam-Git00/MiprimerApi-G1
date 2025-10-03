"""
Pydantic schemas for Enfermera entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CuentaBase(BaseModel):
    """Base schema for Cuenta with common fields."""

    idCliente: UUID
    numeroCuenta: str
    tipoCuenta: str
    saldo: float
    estado: str


class CuentaCreate(CuentaBase):
    """Schema for creating a new Cuenta."""

    pass


class CuentaResponse(CuentaBase):
    """Schema for Cuenta response."""   

    idCuenta: UUID
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
