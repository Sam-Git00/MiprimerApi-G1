from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import SucursalSimple
from typing import List, Optional
import json

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])

def save_sucursales_to_file(sucursales_data):
    """Guarda los datos de sucursales en el archivo JSON"""
    with open("apis/datos/sucursales.json", "w", encoding="utf-8") as file:
        json.dump(sucursales_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[SucursalSimple])
async def listar_sucursales(
    request: Request,
    ciudad: Optional[str] = None,
    estado_sucursal: Optional[str] = None
):
    """Listar todas las sucursales con filtros opcionales"""
    sucursales = request.app.state.sucursales_db
    
    # Aplicar filtros
    if ciudad:
        sucursales = [s for s in sucursales if s["ciudad"].lower() == ciudad.lower()]
    if estado_sucursal:
        sucursales = [s for s in sucursales if s["estadoSucursal"].lower() == estado_sucursal.lower()]
    
    return sucursales

@router.get("/{id_sucursal}", response_model=SucursalSimple)
async def obtener_sucursal(id_sucursal: int, request: Request):
    """Obtener sucursal por ID"""
    sucursales = request.app.state.sucursales_db
    sucursal = next((s for s in sucursales if s["idSucursal"] == id_sucursal), None)
    
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    return sucursal

@router.post("/", response_model=SucursalSimple)
async def crear_sucursal(sucursal: SucursalSimple, request: Request):
    """Crear nueva sucursal"""
    sucursales = request.app.state.sucursales_db
    
    # Verificar que no exista una sucursal con el mismo ID
    if any(s["idSucursal"] == sucursal.idSucursal for s in sucursales):
        raise HTTPException(status_code=400, detail="Ya existe una sucursal con este ID")
    
    # Convertir a diccionario y agregar
    nueva_sucursal = sucursal.model_dump()
    sucursales.append(nueva_sucursal)
    
    # Guardar en archivo
    save_sucursales_to_file(sucursales)
    
    return nueva_sucursal

@router.put("/{id_sucursal}", response_model=SucursalSimple)
async def actualizar_sucursal(id_sucursal: int, sucursal_actualizada: SucursalSimple, request: Request):
    """Actualizar sucursal existente"""
    sucursales = request.app.state.sucursales_db
    
    # Buscar la sucursal
    for i, sucursal in enumerate(sucursales):
        if sucursal["idSucursal"] == id_sucursal:
            # Actualizar datos
            sucursales[i] = sucursal_actualizada.model_dump()
            
            # Guardar en archivo
            save_sucursales_to_file(sucursales)
            
            return sucursales[i]
    
    raise HTTPException(status_code=404, detail="Sucursal no encontrada")

@router.delete("/{id_sucursal}")
async def eliminar_sucursal(id_sucursal: int, request: Request):
    """Eliminar sucursal"""
    sucursales = request.app.state.sucursales_db
    
    # Buscar y eliminar la sucursal
    for i, sucursal in enumerate(sucursales):
        if sucursal["idSucursal"] == id_sucursal:
            sucursal_eliminada = sucursales.pop(i)
            
            # Guardar en archivo
            save_sucursales_to_file(sucursales)
            
            return {"mensaje": "Sucursal eliminada exitosamente", "sucursal": sucursal_eliminada}
    
    raise HTTPException(status_code=404, detail="Sucursal no encontrada")
