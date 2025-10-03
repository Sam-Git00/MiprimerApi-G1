# src/routers/cheque.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.cheques as cheque_controller
import src.controller.clientes as cliente_controller
from database.connection import get_db
from src.schemas.cheques import ChequeCreate, ChequeResponse

router = APIRouter(prefix="/cheques", tags=["Cheques"])

# Crear Cheque
@router.post("/", response_model=ChequeResponse)
def create_cheque(cheque: ChequeCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    # Validar Cliente
    cliente = cliente_controller.get_cliente(db, cheque.idCliente)
    if not cliente:
        raise HTTPException(status_code=400, detail="El cliente no existe")

    # Crear Cheque
    db_cheque = cheque_controller.create_cheque(db, cheque, current_user_id)
    if not db_cheque:
        raise HTTPException(status_code=400, detail="Error al crear cheque")

    return JSONResponse(
        status_code=201,
        content={
            "detail": "Cheque creado correctamente",
            "data": {
                "idCheque": cheque.idCheque,
                "idCliente":cheque.idCliente,
                "fechaEmision":cheque.fechaEmision,
                "monto":cheque.monto,
                "motivo":cheque.motivo,
            },
        },
    )

# Listar todos los Cheques
@router.get("/", response_model=list[ChequeResponse])
def read_cheques(db: Session = Depends(get_db)):
    cheques = cheque_controller.get_cheques(db)
    if not cheques:
        raise HTTPException(status_code=404, detail="No hay cheques registrados")
    return cheques

# Obtener un cheque
@router.get("/{cheque_id}", response_model=ChequeResponse, tags=["Cheques"])
def read_one_cheque(cheque_id: UUID, db: Session = Depends(get_db)):
    db_cheque = cheque_controller.get_cheque(db, cheque_id=cheque_id)
    if db_cheque is None:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cheque encontrado",
                "data": {
                    "idCheque": db_cheque.idCheque,
                    "idCliente":db_cheque.idCliente,
                    "fechaEmision":db_cheque.fechaEmision,
                    "monto":db_cheque.monto,
                    "motivo":db_cheque.motivo,
                },
            },
        )
# Actualizar Cheque
@router.put("/cheques/{cheque_id}", response_model=ChequeResponse, tags=["Cheques"])
def update_cheque(cheque_id: UUID, cheque: ChequeCreate, db: Session = Depends(get_db)):
    db_cheque = cheque_controller.update_cheque(db, cheque_id=cheque_id, cheque=cheque)
    if db_cheque is None:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Cheque actualizado correctamente",
                "data": {
                    "idCheque": cheque.idCheque,
                    "idCliente":cheque.idCliente,
                    "fechaEmision":cheque.fechaEmision,
                    "monto":cheque.monto,
                    "motivo":cheque.motivo,
                },
            },
        )

# Eliminar Cheque
@router.delete("/cheques/{cheque_id}", response_model=ChequeResponse, tags=["Cheques"])
def delete_cheque(cheque_id: UUID, db: Session = Depends(get_db)):
    db_cheque = cheque_controller.delete_cheque(db, cheque_id)
    if not db_cheque:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Cheque eliminado", "data": db_cheque.__dict__})
