# src/routers/prestamo.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.prestamos as prestamo_controller
from database.connection import get_db
from src.schemas.prestamo import PrestamoCreate, PrestamoResponse

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])

@router.post("/", response_model=PrestamoResponse)
def create_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_prestamo = prestamo_controller.create_prestamo(db, prestamo, current_user_id)
    if not db_prestamo:
        raise HTTPException(status_code=400, detail="Error al crear préstamo")
    return JSONResponse(status_code=201, content={"detail": "Préstamo creado correctamente", "data": db_prestamo.__dict__})

@router.get("/", response_model=list[PrestamoResponse])
def read_prestamos(db: Session = Depends(get_db)):
    prestamos = prestamo_controller.get_prestamos(db)
    if not prestamos:
        raise HTTPException(status_code=404, detail="No hay préstamos registrados")
    return prestamos

@router.get("/{prestamo_id}", response_model=PrestamoResponse)
def read_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    db_prestamo = prestamo_controller.get_prestamo(db, prestamo_id)
    if not db_prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return db_prestamo

@router.put("/{prestamo_id}", response_model=PrestamoResponse)
def update_prestamo(prestamo_id: UUID, prestamo: PrestamoCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_prestamo = prestamo_controller.update_prestamo(db, prestamo_id, prestamo, current_user_id)
    if not db_prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Préstamo actualizado", "data": db_prestamo.__dict__})

@router.delete("/{prestamo_id}", response_model=PrestamoResponse)
def delete_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    db_prestamo = prestamo_controller.delete_prestamo(db, prestamo_id)
    if not db_prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Préstamo eliminado", "data": db_prestamo.__dict__})
