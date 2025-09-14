"""Modelos SQLAlchemy para la base de datos"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from apis.database.connection import Base
import uuid

class Cliente(Base):
    """Modelo de cliente para la base de datos"""
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, unique=True, nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), nullable=False)
    numero_telefono = Column(String(20), nullable=False)
    numero_documento = Column(String(20), nullable=False)
    tipo_documento = Column(String(10), nullable=False)
    
    # Campos de auditoría
    id_usuario_creacion = Column(String(36), nullable=False)
    id_usuario_edicion = Column(String(36), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cuentas = relationship("Cuenta", back_populates="cliente")

class Cuenta(Base):
    """Modelo de cuenta para la base de datos"""
    __tablename__ = "cuentas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_cuenta = Column(String(20), unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    tipo_cuenta = Column(String(20), nullable=False)
    saldo_actual = Column(Float, nullable=False, default=0.0)
    estado_cuenta = Column(String(20), nullable=False, default="activa")
    
    # Campos de auditoría
    id_usuario_creacion = Column(String(36), nullable=False)
    id_usuario_edicion = Column(String(36), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="cuentas")
    transacciones_origen = relationship("Transaccion", foreign_keys="[Transaccion.numero_cuenta_origen]", back_populates="cuenta_origen")
    transacciones_destino = relationship("Transaccion", foreign_keys="[Transaccion.numero_cuenta_destino]", back_populates="cuenta_destino")

class Transaccion(Base):
    """Modelo de transacción para la base de datos"""
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_transaccion = Column(Integer, unique=True, nullable=False)
    numero_cuenta_origen = Column(String(20), ForeignKey("cuentas.numero_cuenta"), nullable=False)
    numero_cuenta_destino = Column(String(20), ForeignKey("cuentas.numero_cuenta"), nullable=True)
    tipo_transaccion = Column(String(20), nullable=False)
    monto_transaccion = Column(Float, nullable=False)
    descripcion_transaccion = Column(String(200), nullable=True)
    estado_transaccion = Column(String(20), default="exitosa")
    fecha_transaccion = Column(DateTime, default=func.now())
    
    # Campos de auditoría
    id_usuario_creacion = Column(String(36), nullable=False)
    id_usuario_edicion = Column(String(36), nullable=True)
    fecha_creacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_edicion = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    cuenta_origen = relationship("Cuenta", foreign_keys=[numero_cuenta_origen], back_populates="transacciones_origen")
    cuenta_destino = relationship("Cuenta", foreign_keys=[numero_cuenta_destino], back_populates="transacciones_destino")