# src/routers/cheque.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID

import src.controller.empleados as empleado_controller
import src.controller.clientes as cliente_controller
import src.controller.prestamos as prestamo_controller
from database.connection import get_db
from src.schemas.prestamos import PrestamoCreate, PrestamoResponse

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])

# Crear Cheque
@router.post("/", response_model=PrestamoResponse)
def create_prestamo(prestamo: PrestamoCreate, db: Session = Depends(get_db), current_user_id: UUID = None):
    # Validar Cliente
    cliente = cliente_controller.get_cliente(db, prestamo.idCliente)
    if not cliente:
        raise HTTPException(status_code=400, detail="El cliente no existe")

    # Validar Empleado
    empleado = empleado_controller.get_empleado(db, prestamo.idEmpleado)
    if not empleado:
        raise HTTPException(status_code=400, detail="El empleado no existe")

    # Crear Cheque
    db_prestamo = prestamo_controller.create_prestamo(db, prestamo, current_user_id)
    if not db_prestamo:
        raise HTTPException(status_code=400, detail="Error al crear préstamo")

    return JSONResponse(
        status_code=201,
        content={
            "detail": "Préstamo creado correctamente",
            "data": {
                "idPrestamo": db_prestamo.idPrestamo,
                "idCliente":prestamo.idCliente,
                "idEmpleado":prestamo.idEmpleado,
                "monto":prestamo.montoPrestamo,
                "interes":prestamo.interes,
                "plazo":prestamo.plazoMeses,
                "estado":prestamo.estado,
            },
        },
    )

# Listar todos los Préstamos
@router.get("/", response_model=list[PrestamoResponse])
def read_prestamos(db: Session = Depends(get_db)):
    prestamos_db = prestamo_controller.get_prestamos(db)
    if not prestamos_db:
        raise HTTPException(status_code=404, detail="No hay préstamos registrados")   
    return prestamos_db         


# Listar todos los Préstamos
@router.get("/", response_model=list[PrestamoResponse])
def read_prestamos(db: Session = Depends(get_db)):
    prestamos_db = prestamo_controller.get_prestamos(db)
    if not prestamos_db:
        raise HTTPException(status_code=404, detail="No hay préstamos registrados")   
    return prestamos_db         

# Obtener un préstamo
@router.get("/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos"])
def read_one_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    db_prestamo = prestamo_controller.get_prestamo(db, prestamo_id=prestamo_id)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Préstamo encontrado",
                "data": {
                    "idPrestamo": db_prestamo.idPrestamo,
                    "idCliente":db_prestamo.idCliente,
                    "idEmpleado":db_prestamo.idEmpleado,
                    "monto":db_prestamo.monto,
                    "interes":db_prestamo.interes,
                    "plazo":db_prestamo.plazoMeses,
                    "estado":db_prestamo.estado,
                },
            },
        )   
        
# Actualizar Préstamo
@router.put("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos"])
def update_prestamo(prestamo_id: UUID, prestamo: PrestamoCreate, db: Session = Depends(get_db)):
    db_prestamo = prestamo_controller.update_prestamo(db, prestamo_id=prestamo_id, prestamo=prestamo)
    if db_prestamo is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    else:
        return JSONResponse(
            status_code=201,
            content={
                "detail": "Préstamo actualizado correctamente",
                "data": {
                    "idPrestamo": db_prestamo.idPrestamo,
                    "idCliente":db_prestamo.idCliente,
                    "idEmpleado":db_prestamo.idEmpleado,
                    "monto":db_prestamo.monto,
                    "interes":db_prestamo.interes,
                    "plazo":db_prestamo.plazoMeses,
                    "estado":db_prestamo.estado,
                },
            },
        )

# Eliminar Préstamo
@router.delete("/prestamos/{prestamo_id}", response_model=PrestamoResponse, tags=["Préstamos"])
def delete_prestamo(prestamo_id: UUID, db: Session = Depends(get_db)):
    db_prestamo = prestamo_controller.delete_prestamo(db, prestamo_id)
    if not db_prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return JSONResponse(status_code=200, content={"detail": "Préstamo eliminado", "data": db_prestamo.__dict__})
