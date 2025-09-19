from fastapi import APIRouter, HTTPException, Request, Query
from apis.models.schemas import TarjetaSimple, OperacionBloqueoTarjeta
from typing import List, Optional
from datetime import datetime
import json

router = APIRouter(prefix="/tarjetas", tags=["Tarjetas"])

def save_tarjetas_to_file(tarjetas_data):
    """Guarda los datos de tarjetas en el archivo JSON"""
    with open("apis/datos/tarjetas.json", "w", encoding="utf-8") as file:
        json.dump(tarjetas_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[TarjetaSimple])
async def listar_tarjetas(
    request: Request,
    tipo_tarjeta: Optional[str] = None,
    estado_tarjeta: Optional[str] = None,
    id_cliente: Optional[int] = None,
    incluir_inactivos: bool = Query(False, description="Incluir tarjetas inactivas (eliminadas)")
):
    """Listar todas las tarjetas con filtros opcionales"""
    tarjetas = request.app.state.tarjetas_db
    
    if not incluir_inactivos:
        tarjetas = [t for t in tarjetas if t.get("activo", True)]
    
    # Aplicar filtros
    if tipo_tarjeta:
        tarjetas = [t for t in tarjetas if t["tipoTarjeta"].lower() == tipo_tarjeta.lower()]
    if estado_tarjeta:
        tarjetas = [t for t in tarjetas if t["estadoTarjeta"].lower() == estado_tarjeta.lower()]
    if id_cliente:
        tarjetas = [t for t in tarjetas if t["idCliente"] == id_cliente]
    
    return tarjetas

@router.get("/{numero_tarjeta}", response_model=TarjetaSimple)
async def obtener_tarjeta(numero_tarjeta: str, request: Request):
    """Obtener tarjeta por número"""
    tarjetas = request.app.state.tarjetas_db
    tarjeta = next((t for t in tarjetas if t["numeroTarjeta"] == numero_tarjeta and t.get("activo", True)), None)
    
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    return tarjeta

@router.post("/", response_model=TarjetaSimple)
async def crear_tarjeta(tarjeta: TarjetaSimple, request: Request):
    """Crear nueva tarjeta"""
    tarjetas = request.app.state.tarjetas_db
    
    # Verificar que no exista una tarjeta con el mismo número
    if any(t["numeroTarjeta"] == tarjeta.numeroTarjeta for t in tarjetas):
        raise HTTPException(status_code=400, detail="Ya existe una tarjeta con este número")
    
    # Convertir a diccionario y agregar
    nueva_tarjeta = tarjeta.model_dump()
    tarjetas.append(nueva_tarjeta)
    
    # Guardar en archivo
    save_tarjetas_to_file(tarjetas)
    
    return nueva_tarjeta

@router.put("/{numero_tarjeta}", response_model=TarjetaSimple)
async def actualizar_tarjeta(numero_tarjeta: str, tarjeta_actualizada: TarjetaSimple, request: Request):
    """Actualizar tarjeta existente"""
    tarjetas = request.app.state.tarjetas_db
    
    # Buscar la tarjeta
    for i, tarjeta in enumerate(tarjetas):
        if tarjeta["numeroTarjeta"] == numero_tarjeta and tarjeta.get("activo", True):
            # Actualizar datos
            tarjetas[i] = tarjeta_actualizada.model_dump()
            
            # Guardar en archivo
            save_tarjetas_to_file(tarjetas)
            
            return tarjetas[i]
    
    raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

@router.delete("/{numero_tarjeta}")
async def eliminar_tarjeta(numero_tarjeta: str, request: Request):
    """Eliminar tarjeta usando soft delete"""
    tarjetas = request.app.state.tarjetas_db
    
    for i, tarjeta in enumerate(tarjetas):
        if tarjeta["numeroTarjeta"] == numero_tarjeta and tarjeta.get("activo", True):
            tarjetas[i]["activo"] = False
            tarjetas[i]["fecha_edicion"] = datetime.now().isoformat()
            
            # Guardar en archivo
            save_tarjetas_to_file(tarjetas)
            
            return {"mensaje": f"Tarjeta {numero_tarjeta} eliminada (soft delete)"}
    
    raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

@router.post("/bloquear")
async def bloquear_tarjeta(operacion: OperacionBloqueoTarjeta, request: Request):
    """Bloquear una tarjeta por seguridad"""
    tarjetas = request.app.state.tarjetas_db
    
    # Buscar la tarjeta
    for i, tarjeta in enumerate(tarjetas):
        if tarjeta["numeroTarjeta"] == operacion.numeroTarjeta:
            if tarjeta["estadoTarjeta"] == "Bloqueada":
                raise HTTPException(status_code=400, detail="La tarjeta ya está bloqueada")
            
            # Bloquear tarjeta
            tarjetas[i]["estadoTarjeta"] = "Bloqueada"
            
            # Guardar en archivo
            save_tarjetas_to_file(tarjetas)
            
            return {
                "mensaje": "Tarjeta bloqueada exitosamente",
                "numeroTarjeta": operacion.numeroTarjeta,
                "motivo": operacion.motivo
            }
    
    raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
