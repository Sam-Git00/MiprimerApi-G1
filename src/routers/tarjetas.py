# src/routers/tarjeta.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.tarjetas as tarjeta_controller
from database.connection import get_db
from src.schemas.tarjeta import TarjetaCreate, TarjetaResponse

router = APIRouter(prefix="/tarjetas", tags=["Tarjetas"])

@router.post("/", response_model=TarjetaResponse)
def create_tarjeta(tarjeta: TarjetaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_tarjeta = tarjeta_controller.create_tarjeta(db, tarjeta, current_user_id)
    if not db_tarjeta:
        raise HTTPException(status_code=400, detail="Error al crear tarjeta")
    return JSONResponse(status_code=201, content={"detail": "Tarjeta creada correctamente", "data": db_tarjeta.__dict__})

@router.get("/", response_model=list[TarjetaResponse])
def read_tarjetas(db: Session = Depends(get_db)):
    tarjetas = tarjeta_controller.get_tarjetas(db)
    if not tarjetas:
        raise HTTPException(status_code=404, detail="No hay tarjetas registradas")
    return tarjetas

@router.get("/{tarjeta_id}", response_model=TarjetaResponse)
def read_tarjeta(tarjeta_id: UUID, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.get_tarjeta(db, tarjeta_id)
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return db_tarjeta

@router.put("/{tarjeta_id}", response_model=TarjetaResponse)
def update_tarjeta(tarjeta_id: UUID, tarjeta: TarjetaCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_tarjeta = tarjeta_controller.update_tarjeta(db, tarjeta_id, tarjeta, current_user_id)
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Tarjeta actualizada", "data": db_tarjeta.__dict__})

@router.delete("/{tarjeta_id}", response_model=TarjetaResponse)
def delete_tarjeta(tarjeta_id: UUID, db: Session = Depends(get_db)):
    db_tarjeta = tarjeta_controller.delete_tarjeta(db, tarjeta_id)
    if not db_tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Tarjeta eliminada", "data": db_tarjeta.__dict__})
