from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import InversionSimple, OperacionRetiroInversion
from typing import List, Optional
import json

router = APIRouter(prefix="/inversiones", tags=["Inversiones"])

def save_inversiones_to_file(inversiones_data):
    """Guarda los datos de inversiones en el archivo JSON"""
    with open("apis/datos/inversiones.json", "w", encoding="utf-8") as file:
        json.dump(inversiones_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[InversionSimple])
async def listar_inversiones(
    request: Request,
    tipo_inversion: Optional[str] = None,
    estado_inversion: Optional[str] = None,
    id_cliente: Optional[int] = None
):
    """Listar todas las inversiones con filtros opcionales"""
    inversiones = request.app.state.inversiones_db
    
    # Aplicar filtros
    if tipo_inversion:
        inversiones = [i for i in inversiones if i["tipoInversion"].lower() == tipo_inversion.lower()]
    if estado_inversion:
        inversiones = [i for i in inversiones if i["estadoInversion"].lower() == estado_inversion.lower()]
    if id_cliente:
        inversiones = [i for i in inversiones if i["idCliente"] == id_cliente]
    
    return inversiones

@router.get("/{id_inversion}", response_model=InversionSimple)
async def obtener_inversion(id_inversion: int, request: Request):
    """Obtener inversión por ID"""
    inversiones = request.app.state.inversiones_db
    inversion = next((i for i in inversiones if i["idInversion"] == id_inversion), None)
    
    if not inversion:
        raise HTTPException(status_code=404, detail="Inversión no encontrada")
    
    return inversion

@router.post("/", response_model=InversionSimple)
async def crear_inversion(inversion: InversionSimple, request: Request):
    """Crear nueva inversión"""
    inversiones = request.app.state.inversiones_db
    
    # Verificar que no exista una inversión con el mismo ID
    if any(i["idInversion"] == inversion.idInversion for i in inversiones):
        raise HTTPException(status_code=400, detail="Ya existe una inversión con este ID")
    
    # Convertir a diccionario y agregar
    nueva_inversion = inversion.model_dump()
    inversiones.append(nueva_inversion)
    
    # Guardar en archivo
    save_inversiones_to_file(inversiones)
    
    return nueva_inversion

@router.put("/{id_inversion}", response_model=InversionSimple)
async def actualizar_inversion(id_inversion: int, inversion_actualizada: InversionSimple, request: Request):
    """Actualizar inversión existente"""
    inversiones = request.app.state.inversiones_db
    
    # Buscar la inversión
    for i, inversion in enumerate(inversiones):
        if inversion["idInversion"] == id_inversion:
            # Actualizar datos
            inversiones[i] = inversion_actualizada.model_dump()
            
            # Guardar en archivo
            save_inversiones_to_file(inversiones)
            
            return inversiones[i]
    
    raise HTTPException(status_code=404, detail="Inversión no encontrada")

@router.delete("/{id_inversion}")
async def eliminar_inversion(id_inversion: int, request: Request):
    """Eliminar inversión"""
    inversiones = request.app.state.inversiones_db
    
    # Buscar y eliminar la inversión
    for i, inversion in enumerate(inversiones):
        if inversion["idInversion"] == id_inversion:
            inversion_eliminada = inversiones.pop(i)
            
            # Guardar en archivo
            save_inversiones_to_file(inversiones)
            
            return {"mensaje": "Inversión eliminada exitosamente", "inversion": inversion_eliminada}
    
    raise HTTPException(status_code=404, detail="Inversión no encontrada")

@router.post("/retirar")
async def retirar_inversion(operacion: OperacionRetiroInversion, request: Request):
    """Retirar fondos de inversión"""
    inversiones = request.app.state.inversiones_db
    
    # Buscar la inversión
    for i, inversion in enumerate(inversiones):
        if inversion["idInversion"] == operacion.idInversion:
            if inversion["estadoInversion"] == "Vencida":
                raise HTTPException(status_code=400, detail="No se pueden retirar fondos de una inversión vencida")
            
            if operacion.montoRetiro <= 0:
                raise HTTPException(status_code=400, detail="El monto de retiro debe ser mayor a cero")
            
            if operacion.montoRetiro > inversion["montoInvertido"]:
                raise HTTPException(status_code=400, detail="El monto de retiro no puede ser mayor al monto invertido")
            
            # Realizar el retiro
            nuevo_monto = inversion["montoInvertido"] - operacion.montoRetiro
            inversiones[i]["montoInvertido"] = nuevo_monto
            
            # Si el monto queda en cero, marcar como vencida
            if nuevo_monto == 0:
                inversiones[i]["estadoInversion"] = "Vencida"
            
            # Guardar en archivo
            save_inversiones_to_file(inversiones)
            
            return {
                "mensaje": "Retiro realizado exitosamente",
                "idInversion": operacion.idInversion,
                "montoRetirado": operacion.montoRetiro,
                "montoRestante": nuevo_monto,
                "estadoInversion": inversiones[i]["estadoInversion"]
            }
    
    raise HTTPException(status_code=404, detail="Inversión no encontrada")
