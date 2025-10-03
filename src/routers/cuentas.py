# src/routers/cheque.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.cuentas as cuenta_controller
import src.controller.clientes as cliente_controller
from database.connection import get_db
from src.schemas.cuentas import CuentaCreate, CuentaResponse

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

# Crear Cheque
@router.post("/", response_model=CuentaResponse)
def create_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    # Validar Cliente
    cliente = cliente_controller.get_cliente(db, cuenta.idCliente)
    if not cliente:
        raise HTTPException(status_code=400, detail="El cliente no existe")

    # Crear Cheque
    db_cuenta = cuenta_controller.create_cuenta(db, cuenta, current_user_id)
    if not db_cuenta:
        raise HTTPException(status_code=400, detail="Error al crear cuenta")

    return JSONResponse(
        status_code=201,
        content={
            "detail": "Cuenta creada correctamente",
            "data": {
                "idCuenta": cuenta.idCuenta,
                "idCliente":cuenta.idCliente,
                "numeroCuenta":cuenta.numeroCuenta,
                "tipoCuenta":cuenta.tipoCuenta,
                "saldo":cuenta.saldo,
                "estado":cuenta.estado,
            },
        },
    )

# Listar todos los Cheques
@router.get("/", response_model=list[CuentaResponse])
def read_cuentas(db: Session = Depends(get_db)):
    cuentas = cuenta_controller.get_cuentas(db)
    if not cuentas:
        raise HTTPException(status_code=404, detail="No hay cuentas registradas")   
    return cuentas

# Obtener un cheque
@router.get("/{cuenta_id}", response_model=CuentaResponse, tags=["Cuentas"])
def read_one_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    db_cuenta = cuenta_controller.get_cuenta(db, cuenta_id=cuenta_id)
    if db_cuenta is None:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cuenta encontrada",
                "data": {
                    "idCuenta": db_cuenta.idCuenta,
                    "idCliente":db_cuenta.idCliente,
                    "numeroCuenta":db_cuenta.numeroCuenta,
                    "tipoCuenta":db_cuenta.tipoCuenta,
                    "saldo":db_cuenta.saldo,
                    "estado":db_cuenta.estado,
                },
            },
        )
# Actualizar Cheque
@router.put("/cuentas/{cuenta_id}", response_model=CuentaResponse, tags=["Cuentas"])
def update_cuenta(cuenta_id: UUID, cuenta: CuentaCreate, db: Session = Depends(get_db)):
    db_cuenta = cuenta_controller.update_cuenta(db, cuenta_id=cuenta_id, cuenta=cuenta)
    if db_cuenta is None:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Cuenta actualizada correctamente",
                "data": {
                    "idCuenta": db_cuenta.idCuenta,
                    "idCliente":db_cuenta.idCliente,
                    "numeroCuenta":db_cuenta.numeroCuenta,
                    "tipoCuenta":db_cuenta.tipoCuenta,
                    "saldo":db_cuenta.saldo,
                    "estado":db_cuenta.estado,
                },
            },
        )

# Eliminar Cheque
@router.delete("/cuentas/{cuenta_id}", response_model=CuentaResponse, tags=["Cuentas"])
def delete_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    db_cuenta = cuenta_controller.delete_cuenta(db, cuenta_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Cuenta eliminada", "data": db_cuenta.__dict__})
