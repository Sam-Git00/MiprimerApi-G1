"""Modelos SQLAlchemy para la base de datos"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from apis.database.connection import Base
import uuid
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER

# Modelo de Usuario para la base de datos
class Usuario(Base):
    """Modelo de usuario para la base de datos (para auditoría)"""
    __tablename__ = "usuarios"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    nombre_usuario = Column(String(100), nullable=False)
    correo_electronico = Column(String(150), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_ultimo_acceso = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones de auditoría inversa
    clientes_creados = relationship("Cliente", foreign_keys="[Cliente.id_usuario_creacion]", back_populates="usuario_creacion")
    clientes_editados = relationship("Cliente", foreign_keys="[Cliente.id_usuario_edicion]", back_populates="usuario_edicion")
    cuentas_creadas = relationship("Cuenta", foreign_keys="[Cuenta.id_usuario_creacion]", back_populates="usuario_creacion")
    cuentas_editadas = relationship("Cuenta", foreign_keys="[Cuenta.id_usuario_edicion]", back_populates="usuario_edicion")
    transacciones_creadas = relationship("Transaccion", foreign_keys="[Transaccion.id_usuario_creacion]", back_populates="usuario_creacion")
    transacciones_editadas = relationship("Transaccion", foreign_keys="[Transaccion.id_usuario_edicion]", back_populates="usuario_edicion")
    tarjetas_creadas = relationship("Tarjeta", foreign_keys="[Tarjeta.id_usuario_creacion]", back_populates="usuario_creacion")
    tarjetas_editadas = relationship("Tarjeta", foreign_keys="[Tarjeta.id_usuario_edicion]", back_populates="usuario_edicion")
    prestamos_creados = relationship("Prestamo", foreign_keys="[Prestamo.id_usuario_creacion]", back_populates="usuario_creacion")
    prestamos_editados = relationship("Prestamo", foreign_keys="[Prestamo.id_usuario_edicion]", back_populates="usuario_edicion")
    inversiones_creadas = relationship("Inversion", foreign_keys="[Inversion.id_usuario_creacion]", back_populates="usuario_creacion")
    inversiones_editadas = relationship("Inversion", foreign_keys="[Inversion.id_usuario_edicion]", back_populates="usuario_edicion")
    empleados_creados = relationship("Empleado", foreign_keys="[Empleado.id_usuario_creacion]", back_populates="usuario_creacion")
    empleados_editados = relationship("Empleado", foreign_keys="[Empleado.id_usuario_edicion]", back_populates="usuario_edicion")
    sucursales_gerente = relationship("Sucursal", foreign_keys="[Sucursal.gerente_id]", back_populates="gerente")
    cheques_creados = relationship("Cheque", foreign_keys="[Cheque.id_usuario_creacion]", back_populates="usuario_creacion")
    cheques_editados = relationship("Cheque", foreign_keys="[Cheque.id_usuario_edicion]", back_populates="usuario_edicion")

class Cliente(Base):
    """Modelo de cliente para la base de datos"""
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, unique=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    correo_electronico = Column(String(150), unique=True, nullable=False)
    numero_telefono = Column(String(20), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    tipo_documento = Column(String(10), nullable=False)
    
    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cuentas = relationship("Cuenta", back_populates="cliente")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="clientes_creados")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="clientes_editados")

class Cuenta(Base):
    """Modelo de cuenta para la base de datos"""
    __tablename__ = "cuentas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_cuenta = Column(String(20), unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    tipo_cuenta = Column(String(20), nullable=False)
    saldo_actual = Column(Numeric(15,2), nullable=False, default=0.00)
    estado_cuenta = Column(String(20), nullable=False, default="activa")
    
    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="cuentas")
    transacciones_origen = relationship("Transaccion", foreign_keys="[Transaccion.numero_cuenta_origen]", back_populates="cuenta_origen")
    transacciones_destino = relationship("Transaccion", foreign_keys="[Transaccion.numero_cuenta_destino]", back_populates="cuenta_destino")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="cuentas_creadas")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="cuentas_editadas")

class Transaccion(Base):
    """Modelo de transacción para la base de datos"""
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_transaccion = Column(Integer, unique=True, nullable=False)
    numero_cuenta_origen = Column(String(20), ForeignKey("cuentas.numero_cuenta"), nullable=False)
    numero_cuenta_destino = Column(String(20), ForeignKey("cuentas.numero_cuenta"), nullable=True)
    tipo_transaccion = Column(String(20), nullable=False)
    monto_transaccion = Column(Numeric(15,2), nullable=False)
    descripcion_transaccion = Column(String(200), nullable=True)
    estado_transaccion = Column(String(20), default="exitosa")
    fecha_transaccion = Column(DateTime, default=func.now())
    
    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cuenta_origen = relationship("Cuenta", foreign_keys=[numero_cuenta_origen], back_populates="transacciones_origen")
    cuenta_destino = relationship("Cuenta", foreign_keys=[numero_cuenta_destino], back_populates="transacciones_destino")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="transacciones_creadas")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="transacciones_editadas")


class Tarjeta(Base):
    """Modelo de Tarjeta para la base de datos"""
    __tablename__ = "tarjetas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_tarjeta = Column(Integer, unique=True, nullable=False)
    numero_tarjeta = Column(String(20), unique=True, nullable=False)
    tipo_tarjeta = Column(String(20), nullable=False)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)  # Referencia al id_cliente de la tabla clientes
    fecha_vencimiento = Column(DateTime, nullable=False)
    cvv = Column(String(5), nullable=False)
    estado_tarjeta = Column(String(20), default="activa")
    limite_credito = Column(Numeric(15,2), nullable=True)

    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    cuenta = relationship("Cuenta", foreign_keys=[id_cuenta])
    cliente = relationship("Cliente", foreign_keys=[id_cliente])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="tarjetas_creadas")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="tarjetas_editadas")


class Prestamo(Base):
    """Modelo de Préstamo para la base de datos"""
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_prestamo = Column(Integer, unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    numero_prestamo = Column(String(20), unique=True, nullable=False)
    monto_prestado = Column(Numeric(15,2), nullable=False)
    tas_interes = Column(Numeric(5,2), nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    fecha_desembolso = Column(DateTime, nullable=False)
    saldo_pendiente = Column(Numeric(15,2), nullable=False)
    estado_prestamo = Column(String(20), default="aprobado")
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)

    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    cliente = relationship("Cliente", foreign_keys=[id_cliente])
    cuenta = relationship("Cuenta", foreign_keys=[id_cuenta])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="prestamos_creados")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="prestamos_editados")


class Empleado(Base):
    """Modelo de Empleado para la base de datos"""
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, unique=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    cargo = Column(String(50), nullable=False)
    id_sucursal = Column(Integer, ForeignKey("sucursales.id_sucursal"), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    tipo_documento = Column(String(10), nullable=False)
    correo_electronico = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    estado_empleado = Column(String(20), default="activo")
    activo = Column(Boolean, default=True)

    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="empleados")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="empleados_creados")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="empleados_editados")


class Sucursal(Base):
    """Modelo de Sucursal para la base de datos"""
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_sucursal = Column(Integer, unique=True, nullable=False)
    nombre_sucursal = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    ciudad = Column(String(50), nullable=False)
    codigo_postal = Column(String(10), nullable=False)
    telefono = Column(String(20), nullable=False)
    gerente_id = Column(Integer, ForeignKey("empleados.id_empleado"), nullable=True)
    estado_sucursal = Column(String(20), default="abierta")
    activo = Column(Boolean, default=True)

    # Relaciones
    empleados = relationship("Empleado", back_populates="sucursal")
    gerente = relationship("Empleado", foreign_keys=[gerente_id], back_populates="sucursales_gerente")


class Cheque(Base):
    """Modelo de Cheque para la base de datos"""
    __tablename__ = "cheques"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cheque = Column(Integer, unique=True, nullable=False)
    numero_cheque = Column(String(20), unique=True, nullable=False)
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    monto = Column(Numeric(15,2), nullable=False)
    beneficiario = Column(String(100), nullable=False)
    fecha_emision = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    estado_cheque = Column(String(20), default="emitido")
    activo = Column(Boolean, default=True)

    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)

    # Relaciones
    cuenta = relationship("Cuenta", foreign_keys=[id_cuenta])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="cheques_creados")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="cheques_editados")


class Inversion(Base):
    """Modelo de Inversión para la base de datos"""
    __tablename__ = "inversiones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_inversion = Column(Integer, unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    tipo_inversion = Column(String(50), nullable=False)
    monto_invertido = Column(Numeric(15,2), nullable=False)
    fech_inicio = Column(DateTime, nullable=False)
    plazo = Column(Integer, nullable=False)
    rendimiento_esperado = Column(Numeric(5,2), nullable=False)
    estado_inversion = Column(String(20), default="activa")
    id_cuenta = Column(Integer, ForeignKey("cuentas.id"), nullable=False)

    # Campos de auditoría
    id_usuario_creacion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=False)
    id_usuario_edicion = Column(UNIQUEIDENTIFIER, ForeignKey('usuarios.id'), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, onupdate=func.now(), nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    cliente = relationship("Cliente", foreign_keys=[id_cliente])
    cuenta = relationship("Cuenta", foreign_keys=[id_cuenta])
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion], back_populates="inversiones_creadas")
    usuario_edicion = relationship("Usuario", foreign_keys=[id_usuario_edicion], back_populates="inversiones_editadas")