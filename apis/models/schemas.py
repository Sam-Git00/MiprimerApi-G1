from pydantic import BaseModel


class ClienteSimple(BaseModel):
    idCliente: int
    nombreCompleto: str
    correoElectronico: str
    numeroTelefono: str
    numeroDocumento: str
    tipoDocumento: str


class CuentaSimple(BaseModel):
    numeroCuenta: str
    idCliente: int
    tipoCuenta: str
    saldoActual: float
    estadoCuenta: str


class TransaccionSimple(BaseModel):
    idTransaccion: int
    numeroCuentaOrigen: str
    tipoTransaccion: str
    montoTransaccion: float
    descripcionTransaccion: str


class OperacionConsignacion(BaseModel):
    numeroCuenta: str
    monto: float
    descripcion: str = "Consignación"


class OperacionRetiro(BaseModel):
    numeroCuenta: str
    monto: float
    descripcion: str = "Retiro"


class OperacionTransferencia(BaseModel):
    numeroCuentaOrigen: str
    numeroCuentaDestino: str
    monto: float
    descripcion: str = "Transferencia"


