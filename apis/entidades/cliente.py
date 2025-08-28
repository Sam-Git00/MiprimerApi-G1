from pydantic import BaseModel, Field
from typing import Optional

class Cliente(BaseModel):
    idCliente: int = Field(..., examples=[1], description="ID único del cliente")
    nombreCompleto: str = Field(..., examples=["Juan Pérez García"], description="Nombre completo del cliente")
    correoElectronico: str = Field(..., examples=["juan.perez@email.com"], description="Correo electrónico del cliente")
    numeroTelefono: str = Field(..., examples=["+57 300 123 4567"], description="Número de teléfono")
    numeroDocumento: str = Field(..., examples=["12345678"], description="Número de documento de identidad")
    tipoDocumento: str = Field(..., examples=["CC"], description="Tipo de documento (CC, CE, TI)")

class ClienteActualizar(BaseModel):
    nombreCompleto: Optional[str] = Field(None, examples=["Juan Pérez García"])
    correoElectronico: Optional[str] = Field(None, examples=["juan.perez@email.com"])
    numeroTelefono: Optional[str] = Field(None, examples=["+57 300 123 4567"])
