from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional

from apis.models.schemas import ClienteSimple


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", summary="Obtener lista de clientes", response_model=List[ClienteSimple])
def obtener_clientes(request: Request, tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento (CC, CE, NIT, etc.)")):
    """Obtener lista de clientes"""
    clientes_db = request.app.state.clientes_db
    if tipo_documento:
        clientes_filtrados = [c for c in clientes_db if c["tipoDocumento"].lower() == tipo_documento.lower()]
        if not clientes_filtrados:
            raise HTTPException(status_code=404, detail=f"No se encontraron clientes con tipo de documento: {tipo_documento}")
        return clientes_filtrados
    return clientes_db


@router.get("/{id_cliente}", summary="Obtener cliente por ID", response_model=ClienteSimple)
def obtener_cliente(request: Request, id_cliente: int):
    """Obtener cliente por ID"""
    clientes_db = request.app.state.clientes_db
    for cliente in clientes_db:
        if cliente["idCliente"] == id_cliente:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router.post("", summary="Crear nuevo cliente", status_code=201, response_model=ClienteSimple)
def crear_cliente(request: Request, cliente: ClienteSimple):
    """Crear nuevo cliente"""
    clientes_db = request.app.state.clientes_db
    for c in clientes_db:
        if c["idCliente"] == cliente.idCliente:
            raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    cliente_dict = cliente.model_dump()
    clientes_db.append(cliente_dict)
    return cliente_dict


@router.put("/{id_cliente}", summary="Actualizar cliente", response_model=ClienteSimple)
def actualizar_cliente(request: Request, id_cliente: int, cliente: ClienteSimple):
    """Actualizar cliente"""
    clientes_db = request.app.state.clientes_db
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            cliente_dict = cliente.model_dump()
            clientes_db[i] = cliente_dict
            return cliente_dict
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router.delete("/{id_cliente}", summary="Eliminar cliente")
def eliminar_cliente(request: Request, id_cliente: int):
    """Eliminar cliente"""
    clientes_db = request.app.state.clientes_db
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            clientes_db.pop(i)
            return {"mensaje": f"Cliente {id_cliente} eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


