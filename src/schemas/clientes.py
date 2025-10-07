"""
Pydantic schemas for Diagnostico entity.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ClienteBase(BaseModel):
    """Base schema for Cliente with common fields."""

    idCliente:str
    nombre: str
    apellido: str
    documento: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    fechaNacimiento: Optional[date] = None


class ClienteCreate(ClienteBase):
    """Schema for creating a new Cliente."""

    pass


class ClienteResponse(ClienteBase):
    """Schema for Cliente response."""

    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
