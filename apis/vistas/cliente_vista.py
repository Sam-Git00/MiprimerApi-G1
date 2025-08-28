from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from entidades.cliente import Cliente, ClienteActualizar
from negocio.cliente_negocio import ClienteNegocio

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_negocio = ClienteNegocio()

@router.get(
    "",
    response_model=List[Cliente],
    summary="Obtener todos los clientes",
    description="Retorna una lista con todos los clientes registrados en el sistema",
    responses={
        200: {"description": "Lista de clientes obtenida exitosamente"}
    }
)
def obtener_clientes(
    tipoDocumento: Optional[str] = Query(None, description="Filtrar por tipo de documento (CC, CE, TI)")
) -> List[Cliente]:
    if tipoDocumento:
        return cliente_negocio.buscar_clientes_por_tipo_documento(tipoDocumento)
    return cliente_negocio.obtener_todos_clientes()

@router.get(
    "/{idCliente}",
    response_model=Cliente,
    summary="Obtener cliente por ID",
    description="Retorna un cliente específico basado en su ID",
    responses={
        200: {"description": "Cliente encontrado exitosamente"},
        404: {"description": "Cliente no encontrado"}
    }
)
def obtener_cliente(idCliente: int) -> Cliente:
    return cliente_negocio.obtener_cliente_por_id(idCliente)

@router.post(
    "",
    response_model=Cliente,
    status_code=201,
    summary="Crear nuevo cliente",
    description="Crea un nuevo cliente en el sistema bancario",
    responses={
        201: {"description": "Cliente creado exitosamente"},
        400: {"description": "Error en los datos del cliente"}
    }
)
def crear_cliente(cliente: Cliente) -> Cliente:
    return cliente_negocio.crear_cliente(cliente)

@router.put(
    "/{idCliente}",
    response_model=Cliente,
    summary="Actualizar cliente",
    description="Actualiza la información de un cliente existente",
    responses={
        200: {"description": "Cliente actualizado exitosamente"},
        404: {"description": "Cliente no encontrado"}
    }
)
def actualizar_cliente(idCliente: int, datosActualizacion: ClienteActualizar) -> Cliente:
    return cliente_negocio.actualizar_cliente(idCliente, datosActualizacion)

@router.delete(
    "/{idCliente}",
    summary="Eliminar cliente",
    description="Elimina un cliente del sistema",
    responses={
        200: {"description": "Cliente eliminado exitosamente"},
        404: {"description": "Cliente no encontrado"}
    }
)
def eliminar_cliente(idCliente: int) -> dict:
    return cliente_negocio.eliminar_cliente(idCliente)
