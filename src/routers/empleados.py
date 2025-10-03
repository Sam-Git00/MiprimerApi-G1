from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.controller.empleados as empleado_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.empleados import EmpleadoCreate, EmpleadoResponse

"""Creamos el router para los empleados
Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/empleados", tags=["Empleados"])


@router.post("/empleados/", response_model=EmpleadoResponse, tags=["Empleados"])
def create_empleado(
    empleado: EmpleadoCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Busca en la base de datos si ya existe un empleado con la misma cédula (idEmpleado)"""

    db_empleado = empleado_controller.get_empleado(db, empleado_id=empleado.idEmpleado)

    """Si el empleado ya está registrado, lanza una excepción HTTP con código 400 (Bad Request)"""

    if db_empleado:

        raise HTTPException(status_code=400, detail="Empleado ya registrado")
    else:
        empleado_creado = empleado_controller.create_empleado(db=db, empleado=empleado)

        return JSONResponse(
            status_code=201,
            content={
                "detail": "Empleado creado correctamente",   
                "data": {
                    "Id empleado": empleado.idEmpleado,
                    "nombre": empleado.nombreEmpleado,
                    "documento": empleado.documentoEmpleado,
                    "cargo": empleado.cargo,
                    "telefono": empleado.telefonoEmpleado,
                    "email": empleado.correoEmpleado,
                },
            },
        )


@router.get("/empleados/", response_model=list[EmpleadoResponse], tags=["Empleados"])
def read_all_empleados(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    empleados_db = empleado_controller.get_empleados(db)
    if not empleados_db:
        raise HTTPException(status_code=404, detail="No hay empleados registrados")
    return empleados_db     


"""
    Obtiene todos los empleados registrados en la base de datos.

    Args:
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        list[schemas.Empleado]: Lista de empleados registrados.

    Raises:
        HTTPException: Si no hay empleados registrados, retorna un error 404 con el detalle "No hay empleados registrados".
"""


@router.get(
    "/empleados/{empleado_id}", response_model=EmpleadoResponse, tags=["Empleados"]
)
def read_one_empleado(empleado_id: str, db: Session = Depends(get_db)):
    db_empleado = empleado_controller.get_empleado(db, empleado_id=empleado_id)
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Empleado encontrado correctamente", 
                "data": {
                    "Id empleado": db_empleado.idEmpleado,
                    "nombre": db_empleado.nombre,
                    "apellido": db_empleado.apellido,
                    "documento": db_empleado.documento,
                    "direccion": db_empleado.direccion,
                    "telefono": db_empleado.telefono,
                    "email": db_empleado.email,
                    "fechaNacimiento": db_empleado.fechaNacimiento,
                },
            },
        )


@router.delete(
    "/empleados/{empleado_id}", response_model=EmpleadoResponse, tags=["Empleados"]
)
def delete_empleado(empleado_id: str, db: Session = Depends(get_db)):
    db_empleado = empleado_controller.delete_empleado(db, empleado_id=empleado_id)
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Empleado eliminado correctamente",
                "data": {
                    "Id empleado": db_empleado.idEmpleado,
                    "nombre": db_empleado.nombre,
                    "apellido": db_empleado.apellido,
                    "documento": db_empleado.documento,
                    "direccion": db_empleado.direccion,
                    "telefono": db_empleado.telefono,
                    "email": db_empleado.email,
                    "fechaNacimiento": db_empleado.fechaNacimiento,
                },
            },
        )


@router.put(
    "/empleados/{empleado_id}", response_model=EmpleadoResponse, tags=["Empleados"]
)
def update_empleado(    
    empleado_id: str, empleado: EmpleadoCreate, db: Session = Depends(get_db)
):
    db_empleado = empleado_controller.update_empleado(
        db, empleado_id=empleado_id, empleado=empleado
    )
    if db_empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Empleado actualizado correctamente",
                "data": {
                    "Id empleado": db_empleado.idEmpleado,
                    "nombre": db_empleado.nombre,
                    "apellido": db_empleado.apellido,
                    "documento": db_empleado.documento,
                    "direccion": db_empleado.direccion,
                    "telefono": db_empleado.telefono,
                    "email": db_empleado.email,
                    "fechaNacimiento": db_empleado.fechaNacimiento,
                },
            },
        )
