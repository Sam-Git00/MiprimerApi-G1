from fastapi import APIRouter, HTTPException, Request
from apis.models.schemas import ChequeSimple, OperacionCobroCheque
from typing import List, Optional
import json

router = APIRouter(prefix="/cheques", tags=["Cheques"])

def save_cheques_to_file(cheques_data):
    """Guarda los datos de cheques en el archivo JSON"""
    with open("apis/datos/cheques.json", "w", encoding="utf-8") as file:
        json.dump(cheques_data, file, indent=2, ensure_ascii=False, default=str)

@router.get("/", response_model=List[ChequeSimple])
async def listar_cheques(
    request: Request,
    estado_cheque: Optional[str] = None,
    id_cuenta: Optional[int] = None,
    beneficiario: Optional[str] = None
):
    """Listar todos los cheques con filtros opcionales"""
    cheques = request.app.state.cheques_db
    
    # Aplicar filtros
    if estado_cheque:
        cheques = [c for c in cheques if c["estadoCheque"].lower() == estado_cheque.lower()]
    if id_cuenta:
        cheques = [c for c in cheques if c["idCuenta"] == id_cuenta]
    if beneficiario:
        cheques = [c for c in cheques if beneficiario.lower() in c["beneficiario"].lower()]
    
    return cheques

@router.get("/{numero_cheque}", response_model=ChequeSimple)
async def obtener_cheque(numero_cheque: str, request: Request):
    """Obtener cheque por número"""
    cheques = request.app.state.cheques_db
    cheque = next((c for c in cheques if c["numeroCheque"] == numero_cheque), None)
    
    if not cheque:
        raise HTTPException(status_code=404, detail="Cheque no encontrado")
    
    return cheque

@router.post("/", response_model=ChequeSimple)
async def crear_cheque(cheque: ChequeSimple, request: Request):
    """Crear nuevo cheque"""
    cheques = request.app.state.cheques_db
    
    # Verificar que no exista un cheque con el mismo número
    if any(c["numeroCheque"] == cheque.numeroCheque for c in cheques):
        raise HTTPException(status_code=400, detail="Ya existe un cheque con este número")
    
    # Convertir a diccionario y agregar
    nuevo_cheque = cheque.model_dump()
    cheques.append(nuevo_cheque)
    
    # Guardar en archivo
    save_cheques_to_file(cheques)
    
    return nuevo_cheque

@router.put("/{numero_cheque}", response_model=ChequeSimple)
async def actualizar_cheque(numero_cheque: str, cheque_actualizado: ChequeSimple, request: Request):
    """Actualizar cheque existente"""
    cheques = request.app.state.cheques_db
    
    # Buscar el cheque
    for i, cheque in enumerate(cheques):
        if cheque["numeroCheque"] == numero_cheque:
            # Actualizar datos
            cheques[i] = cheque_actualizado.model_dump()
            
            # Guardar en archivo
            save_cheques_to_file(cheques)
            
            return cheques[i]
    
    raise HTTPException(status_code=404, detail="Cheque no encontrado")

@router.delete("/{numero_cheque}")
async def eliminar_cheque(numero_cheque: str, request: Request):
    """Eliminar cheque"""
    cheques = request.app.state.cheques_db
    
    # Buscar y eliminar el cheque
    for i, cheque in enumerate(cheques):
        if cheque["numeroCheque"] == numero_cheque:
            cheque_eliminado = cheques.pop(i)
            
            # Guardar en archivo
            save_cheques_to_file(cheques)
            
            return {"mensaje": "Cheque eliminado exitosamente", "cheque": cheque_eliminado}
    
    raise HTTPException(status_code=404, detail="Cheque no encontrado")

@router.post("/cobrar")
async def cobrar_cheque(operacion: OperacionCobroCheque, request: Request):
    """Cobrar un cheque (genera transacción)"""
    cheques = request.app.state.cheques_db
    
    # Buscar el cheque
    for i, cheque in enumerate(cheques):
        if cheque["numeroCheque"] == operacion.numeroCheque:
            if cheque["estadoCheque"] == "Cobrado":
                raise HTTPException(status_code=400, detail="El cheque ya ha sido cobrado")
            
            if cheque["estadoCheque"] == "Rechazado":
                raise HTTPException(status_code=400, detail="No se puede cobrar un cheque rechazado")
            
            # Marcar cheque como cobrado
            cheques[i]["estadoCheque"] = "Cobrado"
            
            # Guardar en archivo
            save_cheques_to_file(cheques)
            
            # Aquí se podría generar una transacción automáticamente
            # Por ahora solo retornamos la confirmación del cobro
            
            return {
                "mensaje": "Cheque cobrado exitosamente",
                "numeroCheque": operacion.numeroCheque,
                "monto": cheque["monto"],
                "beneficiario": cheque["beneficiario"],
                "descripcion": operacion.descripcion
            }
    
    raise HTTPException(status_code=404, detail="Cheque no encontrado")
