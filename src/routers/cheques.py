# src/routers/cheque.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.cheques as cheque_controller
from database.connection import get_db
from src.schemas.cheque import ChequeCreate, ChequeResponse

router = APIRouter(prefix="/cheques", tags=["Cheques"])

@router.post("/", response_model=ChequeResponse)
def create_cheque(cheque: ChequeCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cheque = cheque_controller.create_cheque(db, cheque, current_user_id)
    if not db_cheque:
        raise HTTPException(status_code=400, detail="Error al crear cheque")
    return JSONResponse(status_code=201, content={"detail": "Cheque creado correctamente", "data": db_cheque.__dict__})

@router.get("/", response_model=list[ChequeResponse])
def read_cheques(db: Session = Depends(get_db)):
    cheques = cheque_controller.get_cheques(db)
    if not cheques:
        raise HTTPException(status_code=404, detail="No hay cheques registrados")
    return cheques

@router.get("/{cheque_id}", response_model=ChequeResponse)
def read_cheque(cheque_id: UUID, db: Session = Depends(get_db)):
    db_cheque = cheque_controller.get_cheque(db, cheque_id)
    if not db_cheque:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    return db_cheque

@router.put("/{cheque_id}", response_model=ChequeResponse)
def update_cheque(cheque_id: UUID, cheque: ChequeCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cheque = cheque_controller.update_cheque(db, cheque_id, cheque, current_user_id)
    if not db_cheque:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Cheque actualizado", "data": db_cheque.__dict__})

@router.delete("/{cheque_id}", response_model=ChequeResponse)
def delete_cheque(cheque_id: UUID, db: Session = Depends(get_db)):
    db_cheque = cheque_controller.delete_cheque(db, cheque_id)
    if not db_cheque:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Cheque eliminado", "data": db_cheque.__dict__})
