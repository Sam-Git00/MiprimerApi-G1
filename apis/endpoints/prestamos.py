from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import PrestamoSimple, OperacionPagoPrestamo
from typing import List, Optional
import json

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])

def save_prestamos_to_file(prestamos_data):
    """Guarda los datos de préstamos en el archivo JSON"""
    with open("apis/datos/prestamos.json", "w", encoding="utf-8") as file:
        json.dump(prestamos_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[PrestamoSimple])
async def listar_prestamos(
    request: Request,
    estado_prestamo: Optional[str] = None,
    id_cliente: Optional[int] = None
):
    """Listar todos los préstamos con filtros opcionales"""
    prestamos = request.app.state.prestamos_db
    
    # Aplicar filtros
    if estado_prestamo:
        prestamos = [p for p in prestamos if p["estadoPrestamo"].lower() == estado_prestamo.lower()]
    if id_cliente:
        prestamos = [p for p in prestamos if p["idCliente"] == id_cliente]
    
    return prestamos

@router.get("/{id_prestamo}", response_model=PrestamoSimple)
async def obtener_prestamo(id_prestamo: int, request: Request):
    """Obtener préstamo por ID"""
    prestamos = request.app.state.prestamos_db
    prestamo = next((p for p in prestamos if p["idPrestamo"] == id_prestamo), None)
    
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    return prestamo

@router.post("/", response_model=PrestamoSimple)
async def crear_prestamo(prestamo: PrestamoSimple, request: Request):
    """Crear nuevo préstamo"""
    prestamos = request.app.state.prestamos_db
    
    # Verificar que no exista un préstamo con el mismo número
    if any(p["numeroPrestamo"] == prestamo.numeroPrestamo for p in prestamos):
        raise HTTPException(status_code=400, detail="Ya existe un préstamo con este número")
    
    # Convertir a diccionario y agregar
    nuevo_prestamo = prestamo.model_dump()
    prestamos.append(nuevo_prestamo)
    
    # Guardar en archivo
    save_prestamos_to_file(prestamos)
    
    return nuevo_prestamo

@router.put("/{id_prestamo}", response_model=PrestamoSimple)
async def actualizar_prestamo(id_prestamo: int, prestamo_actualizado: PrestamoSimple, request: Request):
    """Actualizar préstamo existente"""
    prestamos = request.app.state.prestamos_db
    
    # Buscar el préstamo
    for i, prestamo in enumerate(prestamos):
        if prestamo["idPrestamo"] == id_prestamo:
            # Actualizar datos
            prestamos[i] = prestamo_actualizado.model_dump()
            
            # Guardar en archivo
            save_prestamos_to_file(prestamos)
            
            return prestamos[i]
    
    raise HTTPException(status_code=404, detail="Préstamo no encontrado")

@router.delete("/{id_prestamo}")
async def eliminar_prestamo(id_prestamo: int, request: Request):
    """Eliminar préstamo"""
    prestamos = request.app.state.prestamos_db
    
    # Buscar y eliminar el préstamo
    for i, prestamo in enumerate(prestamos):
        if prestamo["idPrestamo"] == id_prestamo:
            prestamo_eliminado = prestamos.pop(i)
            
            # Guardar en archivo
            save_prestamos_to_file(prestamos)
            
            return {"mensaje": "Préstamo eliminado exitosamente", "prestamo": prestamo_eliminado}
    
    raise HTTPException(status_code=404, detail="Préstamo no encontrado")

@router.post("/pagar")
async def pagar_prestamo(operacion: OperacionPagoPrestamo, request: Request):
    """Realizar pago parcial o total de un préstamo"""
    prestamos = request.app.state.prestamos_db
    
    # Buscar el préstamo
    for i, prestamo in enumerate(prestamos):
        if prestamo["idPrestamo"] == operacion.idPrestamo:
            if prestamo["estadoPrestamo"] == "Pagado":
                raise HTTPException(status_code=400, detail="El préstamo ya está completamente pagado")
            
            if prestamo["estadoPrestamo"] == "Vencido":
                raise HTTPException(status_code=400, detail="No se pueden realizar pagos a préstamos vencidos")
            
            if operacion.montoPago <= 0:
                raise HTTPException(status_code=400, detail="El monto del pago debe ser mayor a cero")
            
            if operacion.montoPago > prestamo["saldoPendiente"]:
                raise HTTPException(status_code=400, detail="El monto del pago no puede ser mayor al saldo pendiente")
            
            # Realizar el pago
            nuevo_saldo = prestamo["saldoPendiente"] - operacion.montoPago
            prestamos[i]["saldoPendiente"] = nuevo_saldo
            
            # Si el saldo queda en cero, marcar como pagado
            if nuevo_saldo == 0:
                prestamos[i]["estadoPrestamo"] = "Pagado"
            
            # Guardar en archivo
            save_prestamos_to_file(prestamos)
            
            return {
                "mensaje": "Pago realizado exitosamente",
                "idPrestamo": operacion.idPrestamo,
                "montoPagado": operacion.montoPago,
                "saldoPendiente": nuevo_saldo,
                "estadoPrestamo": prestamos[i]["estadoPrestamo"]
            }
    
    raise HTTPException(status_code=404, detail="Préstamo no encontrado")
