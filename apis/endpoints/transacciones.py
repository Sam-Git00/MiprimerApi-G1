from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from apis.models.schemas import (
    TransaccionSimple,
    TransaccionCreate,
    TransaccionUpdate,
    OperacionConsignacion,
    OperacionRetiro,
    OperacionTransferencia,
)
from apis.models.models import Transaccion, Cuenta
from apis.database.connection import get_db


router = APIRouter(prefix="/transacciones", tags=["Transacciones"])


@router.get("", summary="Obtener lista de transacciones", response_model=List[TransaccionSimple])
def obtener_transacciones(
    tipo_transaccion: Optional[str] = Query(None, description="Filtrar por tipo de transacción (Consignación, Retiro, Transferencia, etc.)"),
    incluir_inactivos: bool = Query(False, description="Incluir transacciones inactivas (eliminadas)"),
    db: Session = Depends(get_db)
):
    """Obtener lista de transacciones"""
    query = db.query(Transaccion)
    
    if not incluir_inactivos:
        query = query.filter(Transaccion.activo == True)
    
    if tipo_transaccion:
        query = query.filter(Transaccion.tipo_transaccion.ilike(f"%{tipo_transaccion}%"))
        transacciones = query.all()
        if not transacciones:
            raise HTTPException(status_code=404, detail=f"No se encontraron transacciones con tipo: {tipo_transaccion}")
        return transacciones
    
    return query.all()


@router.get("/{id_transaccion}", summary="Obtener transacción por ID", response_model=TransaccionSimple)
def obtener_transaccion(id_transaccion: int, db: Session = Depends(get_db)):
    """Obtener transacción por ID"""
    transaccion = db.query(Transaccion).filter(Transaccion.id_transaccion == id_transaccion, Transaccion.activo == True).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@router.post("", summary="Crear nueva transacción", status_code=201, response_model=TransaccionSimple)
def crear_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    """Crear nueva transacción"""
    # Verificar si el ID ya existe
    transaccion_existente = db.query(Transaccion).filter(Transaccion.id_transaccion == transaccion.id_transaccion).first()
    if transaccion_existente:
        raise HTTPException(status_code=400, detail="El ID de la transacción ya existe")
    
    # Crear nueva transacción
    nueva_transaccion = Transaccion(
        id_transaccion=transaccion.id_transaccion,
        numero_cuenta_origen=transaccion.numero_cuenta_origen,
        tipo_transaccion=transaccion.tipo_transaccion,
        monto_transaccion=transaccion.monto_transaccion,
        descripcion_transaccion=transaccion.descripcion_transaccion,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    return nueva_transaccion


@router.put("/{id_transaccion}", summary="Actualizar transacción", response_model=TransaccionSimple)
def actualizar_transaccion(id_transaccion: int, transaccion: TransaccionUpdate, db: Session = Depends(get_db)):
    """Actualizar transacción"""
    transaccion_existente = db.query(Transaccion).filter(Transaccion.id_transaccion == id_transaccion, Transaccion.activo == True).first()
    if not transaccion_existente:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Actualizar campos
    for key, value in transaccion.model_dump(exclude_unset=True).items():
        setattr(transaccion_existente, key, value)
    
    transaccion_existente.fecha_edicion = datetime.now()
    transaccion_existente.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    db.refresh(transaccion_existente)
    return transaccion_existente


@router.delete("/{id_transaccion}", summary="Eliminar transacción (soft delete)")
def eliminar_transaccion(id_transaccion: int, db: Session = Depends(get_db)):
    """Eliminar transacción usando soft delete"""
    transaccion = db.query(Transaccion).filter(Transaccion.id_transaccion == id_transaccion, Transaccion.activo == True).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    transaccion.activo = False
    transaccion.fecha_edicion = datetime.now()
    transaccion.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    return {"mensaje": f"Transacción {id_transaccion} eliminada (soft delete)"}


@router.post("/consignar", summary="Realizar consignación")
def consignar(operacion: OperacionConsignacion, db: Session = Depends(get_db)):
    """Realizar consignación"""
    cuenta = db.query(Cuenta).filter(Cuenta.numeroCuenta == operacion.numeroCuenta, Cuenta.activo == True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    saldo_anterior = cuenta.saldoActual
    saldo_nuevo = saldo_anterior + operacion.monto
    
    # Actualizar saldo de la cuenta
    cuenta.saldoActual = saldo_nuevo
    cuenta.fecha_edicion = datetime.now()
    cuenta.id_usuario_edicion = 1  # Usuario por defecto
    
    # Crear registro de transacción
    ultima_transaccion = db.query(Transaccion).order_by(Transaccion.idTransaccion.desc()).first()
    nuevo_id = 1 if not ultima_transaccion else ultima_transaccion.idTransaccion + 1
    
    nueva_transaccion = Transaccion(
        idTransaccion=nuevo_id,
        numeroCuentaOrigen=operacion.numeroCuenta,
        tipoTransaccion="Consignación",
        montoTransaccion=operacion.monto,
        descripcionTransaccion=operacion.descripcion,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nueva_transaccion)
    db.commit()
    
    return {
        "mensaje": "Consignación exitosa",
        "operacion": operacion.model_dump(),
        "tipo": "consignacion",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo,
    }


@router.post("/retirar", summary="Realizar retiro")
def retirar(operacion: OperacionRetiro, db: Session = Depends(get_db)):
    """Realizar retiro"""
    cuenta = db.query(Cuenta).filter(Cuenta.numeroCuenta == operacion.numeroCuenta, Cuenta.activo == True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    saldo_anterior = cuenta.saldoActual
    if saldo_anterior < operacion.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el retiro")
    
    saldo_nuevo = saldo_anterior - operacion.monto
    
    # Actualizar saldo de la cuenta
    cuenta.saldoActual = saldo_nuevo
    cuenta.fecha_edicion = datetime.now()
    cuenta.id_usuario_edicion = 1  # Usuario por defecto
    
    # Crear registro de transacción
    ultima_transaccion = db.query(Transaccion).order_by(Transaccion.idTransaccion.desc()).first()
    nuevo_id = 1 if not ultima_transaccion else ultima_transaccion.idTransaccion + 1
    
    nueva_transaccion = Transaccion(
        idTransaccion=nuevo_id,
        numeroCuentaOrigen=operacion.numeroCuenta,
        tipoTransaccion="Retiro",
        montoTransaccion=operacion.monto,
        descripcionTransaccion=operacion.descripcion,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nueva_transaccion)
    db.commit()
    
    return {
        "mensaje": "Retiro exitoso",
        "operacion": operacion.model_dump(),
        "tipo": "retiro",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo,
    }


@router.post("/transferir", summary="Realizar transferencia")
def transferir(transferencia: OperacionTransferencia, db: Session = Depends(get_db)):
    """Realizar transferencia"""
    if transferencia.numeroCuentaOrigen == transferencia.numeroCuentaDestino:
        raise HTTPException(status_code=400, detail="No se puede transferir a la misma cuenta")
    
    cuenta_origen = db.query(Cuenta).filter(Cuenta.numeroCuenta == transferencia.numeroCuentaOrigen, Cuenta.activo == True).first()
    cuenta_destino = db.query(Cuenta).filter(Cuenta.numeroCuenta == transferencia.numeroCuentaDestino, Cuenta.activo == True).first()
    
    if not cuenta_origen or not cuenta_destino:
        raise HTTPException(status_code=404, detail="Cuenta origen o destino no encontrada")
    
    saldo_origen_anterior = cuenta_origen.saldoActual
    saldo_destino_anterior = cuenta_destino.saldoActual
    
    if saldo_origen_anterior < transferencia.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar la transferencia")
    
    saldo_origen_nuevo = saldo_origen_anterior - transferencia.monto
    saldo_destino_nuevo = saldo_destino_anterior + transferencia.monto
    
    # Actualizar saldos
    cuenta_origen.saldoActual = saldo_origen_nuevo
    cuenta_origen.fecha_edicion = datetime.now()
    cuenta_origen.id_usuario_edicion = 1  # Usuario por defecto
    
    cuenta_destino.saldoActual = saldo_destino_nuevo
    cuenta_destino.fecha_edicion = datetime.now()
    cuenta_destino.id_usuario_edicion = 1  # Usuario por defecto
    
    # Crear registro de transacción
    ultima_transaccion = db.query(Transaccion).order_by(Transaccion.idTransaccion.desc()).first()
    nuevo_id = 1 if not ultima_transaccion else ultima_transaccion.idTransaccion + 1
    
    nueva_transaccion = Transaccion(
        idTransaccion=nuevo_id,
        numeroCuentaOrigen=transferencia.numeroCuentaOrigen,
        tipoTransaccion="Transferencia",
        montoTransaccion=transferencia.monto,
        descripcionTransaccion=transferencia.descripcion,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nueva_transaccion)
    db.commit()
    
    return {
        "mensaje": "Transferencia exitosa",
        "transferencia": transferencia.model_dump(),
        "tipo": "transferencia",
        "saldoOrigenAnterior": saldo_origen_anterior,
        "saldoOrigenNuevo": saldo_origen_nuevo,
        "saldoDestinoAnterior": saldo_destino_anterior,
        "saldoDestinoNuevo": saldo_destino_nuevo,
    }
