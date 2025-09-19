from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import EmpleadoSimple
from typing import List, Optional
import json

router = APIRouter(prefix="/empleados", tags=["Empleados"])

def save_empleados_to_file(empleados_data):
    """Guarda los datos de empleados en el archivo JSON"""
    with open("apis/datos/empleados.json", "w", encoding="utf-8") as file:
        json.dump(empleados_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[EmpleadoSimple])
async def listar_empleados(
    request: Request,
    cargo: Optional[str] = None,
    id_sucursal: Optional[int] = None,
    estado_empleado: Optional[str] = None
):
    """Listar todos los empleados con filtros opcionales"""
    empleados = request.app.state.empleados_db
    
    # Aplicar filtros
    if cargo:
        empleados = [e for e in empleados if e["cargo"].lower() == cargo.lower()]
    if id_sucursal:
        empleados = [e for e in empleados if e["idSucursal"] == id_sucursal]
    if estado_empleado:
        empleados = [e for e in empleados if e["estadoEmpleado"].lower() == estado_empleado.lower()]
    
    return empleados

@router.get("/{id_empleado}", response_model=EmpleadoSimple)
async def obtener_empleado(id_empleado: int, request: Request):
    """Obtener empleado por ID"""
    empleados = request.app.state.empleados_db
    empleado = next((e for e in empleados if e["idEmpleado"] == id_empleado), None)
    
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    return empleado

@router.post("/", response_model=EmpleadoSimple)
async def crear_empleado(empleado: EmpleadoSimple, request: Request):
    """Crear nuevo empleado"""
    empleados = request.app.state.empleados_db
    
    # Verificar que no exista un empleado con el mismo ID
    if any(e["idEmpleado"] == empleado.idEmpleado for e in empleados):
        raise HTTPException(status_code=400, detail="Ya existe un empleado con este ID")
    
    # Verificar que no exista un empleado con el mismo número de documento
    if any(e["numeroDocumento"] == empleado.numeroDocumento for e in empleados):
        raise HTTPException(status_code=400, detail="Ya existe un empleado con este número de documento")
    
    # Convertir a diccionario y agregar
    nuevo_empleado = empleado.model_dump()
    empleados.append(nuevo_empleado)
    
    # Guardar en archivo
    save_empleados_to_file(empleados)
    
    return nuevo_empleado

@router.put("/{id_empleado}", response_model=EmpleadoSimple)
async def actualizar_empleado(id_empleado: int, empleado_actualizado: EmpleadoSimple, request: Request):
    """Actualizar empleado existente"""
    empleados = request.app.state.empleados_db
    
    # Buscar el empleado
    for i, empleado in enumerate(empleados):
        if empleado["idEmpleado"] == id_empleado:
            # Actualizar datos
            empleados[i] = empleado_actualizado.model_dump()
            
            # Guardar en archivo
            save_empleados_to_file(empleados)
            
            return empleados[i]
    
    raise HTTPException(status_code=404, detail="Empleado no encontrado")

@router.delete("/{id_empleado}")
async def eliminar_empleado(id_empleado: int, request: Request):
    """Eliminar empleado"""
    empleados = request.app.state.empleados_db
    
    # Buscar y eliminar el empleado
    for i, empleado in enumerate(empleados):
        if empleado["idEmpleado"] == id_empleado:
            empleado_eliminado = empleados.pop(i)
            
            # Guardar en archivo
            save_empleados_to_file(empleados)
            
            return {"mensaje": "Empleado eliminado exitosamente", "empleado": empleado_eliminado}
    
    raise HTTPException(status_code=404, detail="Empleado no encontrado")
