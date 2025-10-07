from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.controller.clientes as cliente_controller
from database.connection import get_db
from src.auth.middleware import get_current_active_user
from src.schemas.auth import UserResponse
from src.schemas.clientes import ClienteCreate, ClienteResponse

"""Creamos el router para los clientes
Define un prefijo para las rutas y etiquetas para la documentación
En todas las rutas usamos router en lugar de app ya que aqui se abre otra instancia de APIRouter"""

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/clientes/", response_model=ClienteResponse, tags=["Clientes"])
def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    """Busca en la base de datos si ya existe un cliente con la misma cédula (idCliente)"""

    db_cliente = cliente_controller.get_cliente(db, cliente_id=cliente.idCliente)

    """Si el cliente ya está registrado, lanza una excepción HTTP con código 400 (Bad Request)"""

    if db_cliente:

        raise HTTPException(status_code=400, detail="Cliente ya registrado")
    else:
        cliente_creado = cliente_controller.create_cliente(db=db, cliente=cliente)

        return JSONResponse(
            status_code=201,
            content={
                "detail": "Cliente creado correctamente",   
                "data": {
                    "Id cliente": cliente.idCliente,
                    "nombre": cliente.nombre,
                    "apellido": cliente.apellido,
                    "documento": cliente.documento,
                    "direccion": cliente.direccion,
                    "telefono": cliente.telefono,
                    "email": cliente.email,
                    "fechaNacimiento": cliente.fechaNacimiento,
                },
            },
        )


@router.get("/clientes/", response_model=list[ClienteResponse], tags=["Clientes"])
def read_all_clientes(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_active_user),
):
    clientes_db = cliente_controller.get_clientes(db)
    if not clientes_db:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return clientes_db  


"""
    Obtiene todos los clientes registrados en la base de datos.

    Args:
        db (Session): Sesión de base de datos proporcionada por la dependencia `get_db`.

    Returns:
        list[schemas.Cliente]: Lista de clientes registrados.

    Raises:
        HTTPException: Si no hay clientes registrados, retorna un error 404 con el detalle "No hay clientes registrados".
"""


@router.get(
    "/clientes/{cliente_id}", response_model=ClienteResponse, tags=["Clientes"]
)
def read_one_cliente(cliente_id: str, db: Session = Depends(get_db)):
    db_cliente = cliente_controller.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cliente encontrado correctamente", 
                "data": {
                    "Id cliente": db_cliente.idCliente,
                    "nombre": db_cliente.nombre,
                    "apellido": db_cliente.apellido,
                    "documento": db_cliente.documento,
                    "direccion": db_cliente.direccion,
                    "telefono": db_cliente.telefono,
                    "email": db_cliente.email,
                    "fechaNacimiento": db_cliente.fechaNacimiento,
                },
            },
        )


@router.delete(
    "/clientes/{cliente_id}", response_model=ClienteResponse, tags=["Clientes"]
)
def delete_cliente(cliente_id: str, db: Session = Depends(get_db)):
    db_cliente = cliente_controller.delete_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cliente eliminado correctamente",
                "data": {
                    "Id cliente": db_cliente.idCliente,
                    "nombre": db_cliente.nombre,
                    "apellido": db_cliente.apellido,
                    "documento": db_cliente.documento,
                    "direccion": db_cliente.direccion,
                    "telefono": db_cliente.telefono,
                    "email": db_cliente.email,
                    "fechaNacimiento": db_cliente.fechaNacimiento,
                },
            },
        )


@router.put(
    "/clientes/{cliente_id}", response_model=ClienteResponse, tags=["Clientes"]
)
def update_cliente(
    cliente_id: str, cliente: ClienteCreate, db: Session = Depends(get_db)
):
    db_cliente = cliente_controller.update_cliente(
        db, cliente_id=cliente_id, cliente=cliente
    )
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    else:
        return JSONResponse(
            status_code=200,
            content={
                "detail": "Cliente actualizado correctamente",
                "data": {
                    "Id cliente": db_cliente.idCliente,
                    "nombre": db_cliente.nombre,
                    "apellido": db_cliente.apellido,
                    "documento": db_cliente.documento,
                    "direccion": db_cliente.direccion,
                    "telefono": db_cliente.telefono,
                    "email": db_cliente.email,
                    "fechaNacimiento": db_cliente.fechaNacimiento,
                },
            },
        )
