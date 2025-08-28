from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoTransaccion(str, Enum):
    CONSIGNACION = "consignacion"
    RETIRO = "retiro"
    TRANSFERENCIA = "transferencia"

class EstadoTransaccion(str, Enum):
    EXITOSA = "exitosa"
    FALLIDA = "fallida"
    PENDIENTE = "pendiente"

class Transaccion(BaseModel):
    idTransaccion: int = Field(..., examples=[1], description="ID único de la transacción")
    numeroCuentaOrigen: str = Field(..., examples=["1001234567"], description="Número de cuenta origen")
    numeroCuentaDestino: Optional[str] = Field(None, examples=["1001234568"], description="Número de cuenta destino (para transferencias)")
    tipoTransaccion: TipoTransaccion = Field(..., examples=["consignacion"], description="Tipo de transacción")
    montoTransaccion: float = Field(..., examples=[50000.0], description="Monto de la transacción")
    fechaTransaccion: datetime = Field(default_factory=datetime.now, description="Fecha y hora de la transacción")
    descripcionTransaccion: str = Field(..., examples=["Consignación por nómina"], description="Descripción de la transacción")
    estadoTransaccion: EstadoTransaccion = Field(default=EstadoTransaccion.EXITOSA, description="Estado de la transacción")

class TransaccionCrear(BaseModel):
    numeroCuentaOrigen: str = Field(..., examples=["1001234567"])
    numeroCuentaDestino: Optional[str] = Field(None, examples=["1001234568"])
    tipoTransaccion: TipoTransaccion = Field(..., examples=["consignacion"])
    montoTransaccion: float = Field(..., examples=[50000.0])
    descripcionTransaccion: str = Field(..., examples=["Consignación por nómina"])

class OperacionBancaria(BaseModel):
    numeroCuenta: str = Field(..., examples=["1001234567"])
    monto: float = Field(..., examples=[50000.0])
    descripcion: str = Field(..., examples=["Consignación por nómina"])

class TransferenciaBancaria(BaseModel):
    numeroCuentaOrigen: str = Field(..., examples=["1001234567"])
    numeroCuentaDestino: str = Field(..., examples=["1001234568"])
    monto: float = Field(..., examples=[50000.0])
    descripcion: str = Field(..., examples=["Transferencia entre cuentas"])
