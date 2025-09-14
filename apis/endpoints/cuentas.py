from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from apis.models.schemas import CuentaSimple, CuentaCreate, CuentaUpdate
from apis.models.models import Cuenta
from apis.database.connection import get_db


router = APIRouter(prefix="/cuentas", tags=["Cuentas"])


@router.get("", summary="Obtener lista de cuentas", response_model=List[CuentaSimple])
def obtener_cuentas(
    tipo_cuenta: Optional[str] = Query(None, description="Filtrar por tipo de cuenta (Ahorros, Corriente, etc.)"),
    incluir_inactivos: bool = Query(False, description="Incluir cuentas inactivas (eliminadas)"),
    db: Session = Depends(get_db)
):
    """Obtener lista de cuentas"""
    query = db.query(Cuenta)
    
    if not incluir_inactivos:
        query = query.filter(Cuenta.activo == True)
    
    if tipo_cuenta:
        query = query.filter(Cuenta.tipo_cuenta.ilike(f"%{tipo_cuenta}%"))
        cuentas = query.all()
        if not cuentas:
            raise HTTPException(status_code=404, detail=f"No se encontraron cuentas con tipo: {tipo_cuenta}")
        return cuentas
    
    return query.all()


@router.get("/{numero_cuenta}", summary="Obtener cuenta por número", response_model=CuentaSimple)
def obtener_cuenta(numero_cuenta: str, db: Session = Depends(get_db)):
    """Obtener cuenta por número"""
    cuenta = db.query(Cuenta).filter(Cuenta.numero_cuenta == numero_cuenta, Cuenta.activo == True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return cuenta


@router.post("", summary="Crear nueva cuenta", status_code=201, response_model=CuentaSimple)
def crear_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db)):
    """Crear nueva cuenta"""
    # Verificar si el número de cuenta ya existe
    cuenta_existente = db.query(Cuenta).filter(Cuenta.numero_cuenta == cuenta.numero_cuenta).first()
    if cuenta_existente:
        raise HTTPException(status_code=400, detail="El número de cuenta ya existe")
    
    # Crear nueva cuenta
    nueva_cuenta = Cuenta(
        numero_cuenta=cuenta.numero_cuenta,
        id_cliente=cuenta.id_cliente,
        tipo_cuenta=cuenta.tipo_cuenta,
        saldo_actual=cuenta.saldo_actual,
        estado_cuenta=cuenta.estado_cuenta,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nueva_cuenta)
    db.commit()
    db.refresh(nueva_cuenta)
    return nueva_cuenta


@router.put("/{numero_cuenta}", summary="Actualizar cuenta", response_model=CuentaSimple)
def actualizar_cuenta(numero_cuenta: str, cuenta: CuentaUpdate, db: Session = Depends(get_db)):
    """Actualizar cuenta"""
    cuenta_existente = db.query(Cuenta).filter(Cuenta.numero_cuenta == numero_cuenta, Cuenta.activo == True).first()
    if not cuenta_existente:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    # Actualizar campos
    for key, value in cuenta.model_dump(exclude_unset=True).items():
        setattr(cuenta_existente, key, value)
    
    cuenta_existente.fecha_edicion = datetime.now()
    cuenta_existente.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    db.refresh(cuenta_existente)
    return cuenta_existente


@router.delete("/{numero_cuenta}", summary="Eliminar cuenta (soft delete)")
def eliminar_cuenta(numero_cuenta: str, db: Session = Depends(get_db)):
    """Eliminar cuenta usando soft delete"""
    cuenta = db.query(Cuenta).filter(Cuenta.numero_cuenta == numero_cuenta, Cuenta.activo == True).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    cuenta.activo = False
    cuenta.fecha_edicion = datetime.now()
    cuenta.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    return {"mensaje": f"Cuenta {numero_cuenta} eliminada (soft delete)"}
