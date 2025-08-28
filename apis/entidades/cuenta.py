from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TipoCuenta(str, Enum):
    AHORRO = "ahorro"
    CORRIENTE = "corriente"
    CREDITO = "credito"

class EstadoCuenta(str, Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"
    BLOQUEADA = "bloqueada"

class Cuenta(BaseModel):
    numeroCuenta: str = Field(..., examples=["1001234567"], description="Número único de cuenta")
    idCliente: int = Field(..., examples=[1], description="ID del cliente propietario")
    tipoCuenta: TipoCuenta = Field(..., examples=["ahorro"], description="Tipo de cuenta")
    saldoActual: float = Field(default=0.0, examples=[1500000.50], description="Saldo actual de la cuenta")
    limiteCuenta: Optional[float] = Field(None, examples=[5000000.0], description="Límite de la cuenta (para crédito)")
    estadoCuenta: EstadoCuenta = Field(default=EstadoCuenta.ACTIVA, examples=["activa"], description="Estado de la cuenta")

class CuentaCrear(BaseModel):
    idCliente: int = Field(..., examples=[1])
    tipoCuenta: TipoCuenta = Field(..., examples=["ahorro"])
    saldoInicial: float = Field(default=0.0, examples=[100000.0])
    limiteCuenta: Optional[float] = Field(None, examples=[5000000.0])
