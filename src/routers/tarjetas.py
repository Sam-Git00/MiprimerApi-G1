# src/routers/cheque.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.cuentas as cuenta_controller
import src.controller.tarjetas as tarjeta_controller
from database.connection import get_db
from src.schemas.tarjetas import TarjetaCreate, TarjetaResponse

router = APIRouter(prefix="/tarjetas", tags=["Tarjetas"])

# Crear Cheque
@router.post("/", response_model=TarjetaResponse)
def create_tarjeta(tarjeta: TarjetaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    # Validar Cliente
    cuentas = cuenta_controller.get_cuentas(db, tarjeta.idCuenta)
    if not cuentas:
        raise HTTPException(status_code=400, detail="La cuenta no existe")
    # Crear Cheque
    db_tarjeta = tarjeta_controller.create_tarjeta(db, tarjeta, current_user_id)
    if not db_tarjeta:
        raise HTTPException(status_code=400, detail="Error al crear tarjeta")

    return JSONResponse(
        status_code=201,
        content={
            "detail": "Tarjeta creada correctamente",
            "data": {
                "idTarjeta": db_tarjeta.idTarjeta,
                "idCuenta":tarjeta.idCuenta,
                "numeroTarjeta":tarjeta.numeroTarjeta,
                "fechaExpiracion":tarjeta.fechaExpiracion,
                "cvv":tarjeta.cvv,
                "estado":tarjeta.estado,
            },
        },
    )

# Listar todos los Tarjetas
@router.get("/", response_model=list[TarjetaResponse])
def read_tarjetas(db: Session = Depends(get_db)):
    tarjetas_db = tarjeta_controller.get_tarjetas(db)
    if not tarjetas_db:
        raise HTTPException(status_code=404, detail="No hay tarjetas registradas")   
    return tarjetas_db        

# Obtener un préstamo
@router.get("/{tarjeta_id}", response_model=TarjetaResponse, tags=["Tarjetas"])
def read_one_tarjeta(tarjeta_id: UUID, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.get_tarjeta(db, tarjeta_id=tarjeta_id)
    if db_tarjeta is None:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Tarjeta encontrada",
                "data": {
                    "idTarjeta": db_tarjeta.idTarjeta,
                    "idCuenta":db_tarjeta.idCuenta,
                    "numeroTarjeta":db_tarjeta.numeroTarjeta,
                    "fechaExpiracion":db_tarjeta.fechaExpiracion,
                    "cvv":db_tarjeta.cvv,
                    "estado":db_tarjeta.estado,
                },
            },
        )   

        
# Actualizar Tarjeta
@router.put("/tarjetas/{tarjeta_id}", response_model=TarjetaResponse, tags=["Tarjetas"])
def update_tarjeta(tarjeta_id: UUID, tarjeta: TarjetaCreate, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.update_tarjeta(db, tarjeta_id=tarjeta_id, tarjeta=tarjeta)
    if db_tarjeta is None:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Tarjeta actualizada correctamente",
                "data": {
                    "idTarjeta": db_tarjeta.idTarjeta,
                    "idCuenta":db_tarjeta.idCuenta,
                    "numeroTarjeta":db_tarjeta.numeroTarjeta,
                    "fechaExpiracion":db_tarjeta.fechaExpiracion,
                    "cvv":db_tarjeta.cvv,
                    "estado":db_tarjeta.estado,
                },
            },
        )



# Eliminar Tarjeta
@router.delete("/tarjetas/{tarjeta_id}", response_model=TarjetaResponse, tags=["Tarjetas"])
def delete_tarjeta(tarjeta_id: UUID, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.delete_tarjeta(db, tarjeta_id)
    if db_tarjeta is None:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Tarjeta eliminada",
                "data": {
                    "idTarjeta": db_tarjeta.idTarjeta,
                    "idCuenta":db_tarjeta.idCuenta,
                    "numeroTarjeta":db_tarjeta.numeroTarjeta,
                    "fechaExpiracion":db_tarjeta.fechaExpiracion,
                    "cvv":db_tarjeta.cvv,
                    "estado":db_tarjeta.estado,
                },
            },
        )

# Eliminar tarjeta
@router.delete("/tarjetas/{tarjeta_id}", response_model=TarjetaResponse, tags=["Tarjetas"])
def delete_tarjeta(tarjeta_id: UUID, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.delete_tarjeta(db, tarjeta_id)
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Tarjeta eliminada", "data": db_tarjeta.__dict__})
