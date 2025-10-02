# src/routers/cliente.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.clientes as cliente_controller
from database.connection import get_db
from src.schemas.cliente import ClienteCreate, ClienteResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cliente = cliente_controller.create_cliente(db, cliente, current_user_id)
    if not db_cliente:
        raise HTTPException(status_code=400, detail="Error al crear cliente")
    return JSONResponse(status_code=201, content={"detail": "Cliente creado correctamente", "data": db_cliente.__dict__})

@router.get("/", response_model=list[ClienteResponse])
def read_clientes(db: Session = Depends(get_db)):
    clientes = cliente_controller.get_clientes(db)
    if not clientes:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return clientes

@router.get("/{cliente_id}", response_model=ClienteResponse)
def read_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    db_cliente = cliente_controller.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(cliente_id: UUID, cliente: ClienteCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_cliente = cliente_controller.update_cliente(db, cliente_id, cliente, current_user_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Cliente actualizado", "data": db_cliente.__dict__})

@router.delete("/{cliente_id}", response_model=ClienteResponse)
def delete_cliente(cliente_id: UUID, db: Session = Depends(get_db)):
    db_cliente = cliente_controller.delete_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Cliente eliminado", "data": db_cliente.__dict__})
