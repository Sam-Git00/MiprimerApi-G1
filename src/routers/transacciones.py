# src/routers/transaccion.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.transacciones as transaccion_controller
from database.connection import get_db
from src.schemas.transaccion import TransaccionCreate, TransaccionResponse

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/", response_model=TransaccionResponse)
def create_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_transaccion = transaccion_controller.create_transaccion(db, transaccion, current_user_id)
    if not db_transaccion:
        raise HTTPException(status_code=400, detail="Error al crear transacción")
    return JSONResponse(status_code=201, content={"detail": "Transacción creada correctamente", "data": db_transaccion.__dict__})

@router.get("/", response_model=list[TransaccionResponse])
def read_transacciones(db: Session = Depends(get_db)):
    transacciones = transaccion_controller.get_transacciones(db)
    if not transacciones:
        raise HTTPException(status_code=404, detail="No hay transacciones registradas")
    return transacciones

@router.get("/{transaccion_id}", response_model=TransaccionResponse)
def read_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    db_transaccion = transaccion_controller.get_transaccion(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_transaccion

@router.put("/{transaccion_id}", response_model=TransaccionResponse)
def update_transaccion(transaccion_id: UUID, transaccion: TransaccionCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_transaccion = transaccion_controller.update_transaccion(db, transaccion_id, transaccion, current_user_id)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Transacción actualizada", "data": db_transaccion.__dict__})

@router.delete("/{transaccion_id}", response_model=TransaccionResponse)
def delete_transaccion(transaccion_id: UUID, db: Session = Depends(get_db)):
    db_transaccion = transaccion_controller.delete_transaccion(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return JSONResponse(status_code=200, content={"detail": "Transacción eliminada", "data": db_transaccion.__dict__})
