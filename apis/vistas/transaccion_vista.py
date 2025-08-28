from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from entidades.transaccion import Transaccion, OperacionBancaria, TransferenciaBancaria
from negocio.transaccion_negocio import TransaccionNegocio

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])
transaccion_negocio = TransaccionNegocio()

@router.get(
    "",
    response_model=List[Transaccion],
    summary="Obtener todas las transacciones",
    description="Retorna una lista con todas las transacciones realizadas",
    responses={
        200: {"description": "Lista de transacciones obtenida exitosamente"}
    }
)
def obtener_transacciones(
    numeroCuenta: Optional[str] = Query(None, description="Filtrar por número de cuenta"),
    tipoTransaccion: Optional[str] = Query(None, description="Filtrar por tipo (consignacion, retiro, transferencia)")
) -> List[Transaccion]:
    if numeroCuenta:
        return transaccion_negocio.obtener_transacciones_por_cuenta(numeroCuenta)
    elif tipoTransaccion:
        return transaccion_negocio.obtener_transacciones_por_tipo(tipoTransaccion)
    return transaccion_negocio.obtener_todas_transacciones()

@router.get(
    "/{idTransaccion}",
    response_model=Transaccion,
    summary="Obtener transacción por ID",
    description="Retorna una transacción específica basada en su ID",
    responses={
        200: {"description": "Transacción encontrada exitosamente"},
        404: {"description": "Transacción no encontrada"}
    }
)
def obtener_transaccion(idTransaccion: int) -> Transaccion:
    return transaccion_negocio.obtener_transaccion_por_id(idTransaccion)

@router.post(
    "/consignar",
    status_code=201,
    summary="Realizar consignación",
    description="Realiza una consignación a una cuenta bancaria",
    responses={
        201: {"description": "Consignación realizada exitosamente"},
        400: {"description": "Error en los datos de la operación"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def consignar(operacion: OperacionBancaria) -> dict:
    return transaccion_negocio.consignar(operacion)

@router.post(
    "/retirar",
    status_code=201,
    summary="Realizar retiro",
    description="Realiza un retiro de una cuenta bancaria",
    responses={
        201: {"description": "Retiro realizado exitosamente"},
        400: {"description": "Saldo insuficiente o error en los datos"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def retirar(operacion: OperacionBancaria) -> dict:
    return transaccion_negocio.retirar(operacion)

@router.post(
    "/transferir",
    status_code=201,
    summary="Realizar transferencia",
    description="Realiza una transferencia entre cuentas bancarias",
    responses={
        201: {"description": "Transferencia realizada exitosamente"},
        400: {"description": "Saldo insuficiente o error en los datos"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def transferir(transferencia: TransferenciaBancaria) -> dict:
    return transaccion_negocio.transferir(transferencia)

@router.put(
    "/{idTransaccion}",
    response_model=Transaccion,
    summary="Actualizar transacción",
    description="Actualiza una transacción existente (funcionalidad limitada)",
    responses={
        200: {"description": "Transacción actualizada exitosamente"},
        404: {"description": "Transacción no encontrada"}
    }
)
def actualizar_transaccion(idTransaccion: int) -> Transaccion:
    # En un sistema real, las transacciones no se modifican, solo se consultan
    return transaccion_negocio.obtener_transaccion_por_id(idTransaccion)

@router.delete(
    "/{idTransaccion}",
    summary="Eliminar transacción",
    description="Elimina una transacción del sistema (solo para casos especiales)",
    responses={
        200: {"description": "Transacción eliminada exitosamente"},
        404: {"description": "Transacción no encontrada"}
    }
)
def eliminar_transaccion(idTransaccion: int) -> dict:
    # En un sistema real, las transacciones no se eliminan
    transaccion = transaccion_negocio.obtener_transaccion_por_id(idTransaccion)
    return {"mensaje": f"Transacción {idTransaccion} marcada para eliminación (funcionalidad simulada)"}
