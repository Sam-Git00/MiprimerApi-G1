from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from apis.models.schemas import ClienteSimple, ClienteCreate, ClienteUpdate
from apis.models.models import Cliente
from apis.database.connection import get_db


router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("", summary="Obtener lista de clientes", response_model=List[ClienteSimple])
def obtener_clientes(
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento (CC, CE, NIT, etc.)"),
    incluir_inactivos: bool = Query(False, description="Incluir clientes inactivos (eliminados)"),
    db: Session = Depends(get_db)
):
    """Obtener lista de clientes"""
    query = db.query(Cliente)
    
    if not incluir_inactivos:
        query = query.filter(Cliente.activo == True)
    
    if tipo_documento:
        query = query.filter(Cliente.tipo_documento.ilike(f"%{tipo_documento}%"))
        clientes = query.all()
        if not clientes:
            raise HTTPException(status_code=404, detail=f"No se encontraron clientes con tipo de documento: {tipo_documento}")
        return clientes
    
    return query.all()


@router.get("/{id_cliente}", summary="Obtener cliente por ID", response_model=ClienteSimple)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Obtener cliente por ID"""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente, Cliente.activo == True).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("", summary="Crear nuevo cliente", status_code=201, response_model=ClienteSimple)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crear nuevo cliente"""
    # Verificar si el ID ya existe
    cliente_existente = db.query(Cliente).filter(Cliente.id_cliente == cliente.id_cliente).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    
    # Crear nuevo cliente
    nuevo_cliente = Cliente(
        id_cliente=cliente.id_cliente,
        nombre_completo=cliente.nombre_completo,
        correo_electronico=cliente.correo_electronico,
        numero_telefono=cliente.numero_telefono,
        numero_documento=cliente.numero_documento,
        tipo_documento=cliente.tipo_documento,
        activo=True,
        fecha_creacion=datetime.now(),
        fecha_edicion=datetime.now(),
        id_usuario_creacion=1,  # Usuario por defecto
        id_usuario_edicion=1    # Usuario por defecto
    )
    
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.put("/{id_cliente}", summary="Actualizar cliente", response_model=ClienteSimple)
def actualizar_cliente(id_cliente: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    """Actualizar cliente"""
    cliente_existente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente, Cliente.activo == True).first()
    if not cliente_existente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizar campos
    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(cliente_existente, key, value)
    
    cliente_existente.fecha_edicion = datetime.now()
    cliente_existente.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    db.refresh(cliente_existente)
    return cliente_existente


@router.delete("/{id_cliente}", summary="Eliminar cliente (soft delete)")
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    """Eliminar cliente usando soft delete"""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente, Cliente.activo == True).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    cliente.activo = False
    cliente.fecha_edicion = datetime.now()
    cliente.id_usuario_edicion = 1  # Usuario por defecto
    
    db.commit()
    return {"mensaje": f"Cliente {id_cliente} eliminado (soft delete)"}
