from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class AuditableModel(BaseModel):
    id_usuario_creacion: UUID
    id_usuario_edicion: Optional[UUID] = None
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    fecha_edicion: Optional[datetime] = None
    activo: bool = True


class ClienteBase(BaseModel):
    id_cliente: int
    nombre_completo: str
    correo_electronico: str
    numero_telefono: str
    numero_documento: str
    tipo_documento: str


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(ClienteBase):
    id_cliente: Optional[int] = None
    nombre_completo: Optional[str] = None
    correo_electronico: Optional[str] = None
    numero_telefono: Optional[str] = None
    numero_documento: Optional[str] = None
    tipo_documento: Optional[str] = None


class ClienteSimple(ClienteBase, AuditableModel):
    pass


class CuentaBase(BaseModel):
    numero_cuenta: str
    id_cliente: int
    tipo_cuenta: str
    saldo_actual: float
    estado_cuenta: str


class CuentaCreate(CuentaBase):
    pass


class CuentaUpdate(CuentaBase):
    id_cliente: Optional[int] = None
    tipo_cuenta: Optional[str] = None
    saldo_actual: Optional[float] = None
    estado_cuenta: Optional[str] = None


class CuentaSimple(CuentaBase, AuditableModel):
    pass


class TransaccionBase(BaseModel):
    id_transaccion: int
    numero_cuenta_origen: str
    tipo_transaccion: str
    monto_transaccion: float
    descripcion_transaccion: str


class TransaccionCreate(TransaccionBase):
    pass


class TransaccionUpdate(TransaccionBase):
    id_transaccion: Optional[int] = None
    numero_cuenta_origen: Optional[str] = None
    tipo_transaccion: Optional[str] = None
    monto_transaccion: Optional[float] = None
    descripcion_transaccion: Optional[str] = None


class TransaccionSimple(TransaccionBase, AuditableModel):
    pass


class OperacionConsignacion(BaseModel):
    numero_cuenta: str
    monto: float
    descripcion: str = "Consignación"


class OperacionRetiro(BaseModel):
    numero_cuenta: str
    monto: float
    descripcion: str = "Retiro"


class OperacionTransferencia(BaseModel):
    numero_cuenta_origen: str
    numero_cuenta_destino: str
    monto: float
    descripcion: str = "Transferencia"


class TarjetaSimple(AuditableModel):
    id_tarjeta: int
    numero_tarjeta: str
    tipo_tarjeta: str  # "Débito", "Crédito"
    id_cuenta: int
    id_cliente: int
    fecha_vencimiento: date
    cvv: str
    estado_tarjeta: str  # "Activa", "Bloqueada"
    limite_credito: Optional[float] = None


class PrestamoSimple(AuditableModel):
    id_prestamo: int
    id_cliente: int
    numero_prestamo: str
    monto_prestado: float
    tasa_interes: float
    plazo_meses: int
    fecha_desembolso: date
    saldo_pendiente: float
    estado_prestamo: str  # "Aprobado", "Pagado", "Vencido"
    id_cuenta: int


class SucursalSimple(BaseModel):
    id_sucursal: int
    nombre_sucursal: str
    direccion: str
    ciudad: str
    codigo_postal: str
    telefono: str
    gerente_id: Optional[int] = None
    estado_sucursal: str  # "Abierta", "Cerrada"
    activo: bool = True


class EmpleadoSimple(BaseModel):
    id_empleado: int
    nombre_completo: str
    cargo: str  # "Cajero", "Gerente"
    id_sucursal: int
    numero_documento: str
    tipo_documento: str  # "CC"
    correo_electronico: str
    telefono: str
    estado_empleado: str  # "Activo", "Inactivo"
    activo: bool = True


class ChequeSimple(BaseModel):
    id_cheque: int
    numero_cheque: str
    id_cuenta: int
    monto: float
    beneficiario: str
    fecha_emision: date
    fecha_vencimiento: date
    estado_cheque: str  # "Emitido", "Cobrado", "Rechazado"
    activo: bool = True


class InversionSimple(AuditableModel):
    id_inversion: int
    id_cliente: int
    tipo_inversion: str  # "Acciones", "Fondos Mutuos"
    monto_invertido: float
    fecha_inicio: date
    plazo: int  # en meses
    rendimiento_esperado: float
    estado_inversion: str  # "Activa", "Vencida"
    id_cuenta: int


class OperacionBloqueoTarjeta(BaseModel):
    numero_tarjeta: str
    motivo: str = "Bloqueo por seguridad"


class OperacionPagoPrestamo(BaseModel):
    id_prestamo: int
    monto_pago: float
    descripcion: str = "Pago de préstamo"


class OperacionCobroCheque(BaseModel):
    numero_cheque: str
    descripcion: str = "Cobro de cheque"


class OperacionRetiroInversion(BaseModel):
    id_inversion: int
    monto_retiro: float
    descripcion: str = "Retiro de inversión"
