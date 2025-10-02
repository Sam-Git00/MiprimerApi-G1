# src/routers/cuenta.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.cuentas as cuenta_controller
from database.connection import get_db
from src.schemas.cuentas import CuentaCreate, CuentaResponse

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

@router.post("/", response_model=CuentaResponse)
def create_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cuenta = cuenta_controller.create_cuenta(db, cuenta, current_user_id)
    if not db_cuenta:
        raise HTTPException(status_code=400, detail="Error al crear cuenta")
    return JSONResponse(status_code=201, content={"detail": "Cuenta creada correctamente", "data": db_cuenta.__dict__})

@router.get("/", response_model=list[CuentaResponse])
def read_cuentas(db: Session = Depends(get_db)):
    cuentas = cuenta_controller.get_cuentas(db)
    if not cuentas:
        raise HTTPException(status_code=404, detail="No hay cuentas registradas")
    return cuentas

@router.get("/{cuenta_id}", response_model=CuentaResponse)
def read_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    db_cuenta = cuenta_controller.get_cuenta(db, cuenta_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return db_cuenta

@router.put("/{cuenta_id}", response_model=CuentaResponse)
def update_cuenta(cuenta_id: UUID, cuenta: CuentaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cuenta = cuenta_controller.update_cuenta(db, cuenta_id, cuenta, current_user_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Cuenta actualizada", "data": db_cuenta.__dict__})

@router.delete("/{cuenta_id}", response_model=CuentaResponse)
def delete_cuenta(cuenta_id: UUID, db: Session = Depends(get_db)):
    db_cuenta = cuenta_controller.delete_cuenta(db, cuenta_id)
    if not db_cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Cuenta eliminada", "data": db_cuenta.__dict__})
