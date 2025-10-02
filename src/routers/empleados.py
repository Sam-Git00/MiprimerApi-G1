# src/routers/empleado.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
import src.controller.empleados as empleado_controller
from database.connection import get_db
from src.schemas.empleado import EmpleadoCreate, EmpleadoResponse

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=EmpleadoResponse)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_empleado = empleado_controller.create_empleado(db, empleado, current_user_id)
    if not db_empleado:
        raise HTTPException(status_code=400, detail="Error al crear empleado")
    return JSONResponse(status_code=201, content={"detail": "Empleado creado", "data": db_empleado.__dict__})

@router.get("/", response_model=list[EmpleadoResponse])
def read_empleados(db: Session = Depends(get_db)):
    empleados = empleado_controller.get_empleados(db)
    if not empleados:
        raise HTTPException(status_code=404, detail="No hay empleados registrados")
    return empleados

@router.get("/{empleado_id}", response_model=EmpleadoResponse)
def read_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    db_empleado = empleado_controller.get_empleado(db, empleado_id)
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return db_empleado

@router.put("/{empleado_id}", response_model=EmpleadoResponse)
def update_empleado(empleado_id: UUID, empleado: EmpleadoCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    db_empleado = empleado_controller.update_empleado(db, empleado_id, empleado, current_user_id)
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Empleado actualizado", "data": db_empleado.__dict__})

@router.delete("/{empleado_id}", response_model=EmpleadoResponse)
def delete_empleado(empleado_id: UUID, db: Session = Depends(get_db)):
    db_empleado = empleado_controller.delete_empleado(db, empleado_id)
    if not db_empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Empleado eliminado", "data": db_empleado.__dict__})
