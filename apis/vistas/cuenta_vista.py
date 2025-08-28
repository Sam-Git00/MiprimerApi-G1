from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from entidades.cuenta import Cuenta, CuentaCrear, EstadoCuenta
from negocio.cuenta_negocio import CuentaNegocio

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])
cuenta_negocio = CuentaNegocio()

@router.get(
    "",
    response_model=List[Cuenta],
    summary="Obtener todas las cuentas",
    description="Retorna una lista con todas las cuentas bancarias registradas",
    responses={
        200: {"description": "Lista de cuentas obtenida exitosamente"}
    }
)
def obtener_cuentas(
    tipoCuenta: Optional[str] = Query(None, description="Filtrar por tipo de cuenta (ahorro, corriente, credito)"),
    idCliente: Optional[int] = Query(None, description="Filtrar por ID del cliente")
) -> List[Cuenta]:
    if tipoCuenta:
        return cuenta_negocio.obtener_cuentas_por_tipo(tipoCuenta)
    elif idCliente:
        return cuenta_negocio.obtener_cuentas_por_cliente(idCliente)
    return cuenta_negocio.obtener_todas_cuentas()

@router.get(
    "/{numeroCuenta}",
    response_model=Cuenta,
    summary="Obtener cuenta por número",
    description="Retorna una cuenta específica basada en su número",
    responses={
        200: {"description": "Cuenta encontrada exitosamente"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def obtener_cuenta(numeroCuenta: str) -> Cuenta:
    return cuenta_negocio.obtener_cuenta_por_numero(numeroCuenta)

@router.post(
    "",
    response_model=Cuenta,
    status_code=201,
    summary="Crear nueva cuenta",
    description="Crea una nueva cuenta bancaria para un cliente",
    responses={
        201: {"description": "Cuenta creada exitosamente"},
        400: {"description": "Error en los datos de la cuenta"},
        404: {"description": "Cliente no encontrado"}
    }
)
def crear_cuenta(datosCuenta: CuentaCrear) -> Cuenta:
    return cuenta_negocio.crear_cuenta(datosCuenta)

@router.put(
    "/{numeroCuenta}",
    response_model=Cuenta,
    summary="Actualizar estado de cuenta",
    description="Actualiza el estado de una cuenta bancaria",
    responses={
        200: {"description": "Cuenta actualizada exitosamente"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def actualizar_cuenta(numeroCuenta: str, estadoCuenta: EstadoCuenta) -> Cuenta:
    return cuenta_negocio.actualizar_cuenta(numeroCuenta, estadoCuenta)

@router.delete(
    "/{numeroCuenta}",
    summary="Eliminar cuenta",
    description="Elimina una cuenta bancaria del sistema",
    responses={
        200: {"description": "Cuenta eliminada exitosamente"},
        400: {"description": "No se puede eliminar cuenta con saldo"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def eliminar_cuenta(numeroCuenta: str) -> dict:
    return cuenta_negocio.eliminar_cuenta(numeroCuenta)
