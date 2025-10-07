"""
Pydantic schemas for Factura entity.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class EmpleadoBase(BaseModel):
    """Base schema for Empleado with common fields."""

    idEmpleado: str
    nombreEmpleado: str
    documentoEmpleado: str
    correoEmpleado: EmailStr
    telefonoEmpleado: Optional[str] = None
    cargo: Optional[str] = None



class EmpleadoCreate(EmpleadoBase):
    """Schema for creating a new Empleado."""

    pass


class EmpleadoResponse(EmpleadoBase):
    """Schema for Empleado response."""
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_actualizacion: Optional[UUID] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
