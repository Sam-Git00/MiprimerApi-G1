from typing import List, Optional
from fastapi import HTTPException
from entidades.cliente import Cliente, ClienteActualizar
import json
import os

class ClienteNegocio:
    def __init__(self):
        self.archivo_datos = "datos/clientes.json"
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.clientes_db = [Cliente(**cliente) for cliente in datos]
        else:
            self.clientes_db = []
    
    def _guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo_datos), exist_ok=True)
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            datos = [cliente.dict() for cliente in self.clientes_db]
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def obtener_todos_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        return self.clientes_db
    
    def obtener_cliente_por_id(self, id_cliente: int) -> Cliente:
        """Obtiene un cliente por su ID"""
        for cliente in self.clientes_db:
            if cliente.idCliente == id_cliente:
                return cliente
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    def crear_cliente(self, cliente: Cliente) -> Cliente:
        """Crea un nuevo cliente"""
        # Validar que no exista el ID
        for cliente_existente in self.clientes_db:
            if cliente_existente.idCliente == cliente.idCliente:
                raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
        
        # Validar que no exista el documento
        for cliente_existente in self.clientes_db:
            if cliente_existente.numeroDocumento == cliente.numeroDocumento:
                raise HTTPException(status_code=400, detail="El número de documento ya está registrado")
        
        self.clientes_db.append(cliente)
        self._guardar_datos()
        return cliente
    
    def actualizar_cliente(self, id_cliente: int, datos_actualizacion: ClienteActualizar) -> Cliente:
        """Actualiza un cliente existente"""
        for index, cliente in enumerate(self.clientes_db):
            if cliente.idCliente == id_cliente:
                datos_actualizados = datos_actualizacion.dict(exclude_unset=True)
                cliente_actualizado = cliente.copy(update=datos_actualizados)
                self.clientes_db[index] = cliente_actualizado
                self._guardar_datos()
                return cliente_actualizado
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    def eliminar_cliente(self, id_cliente: int) -> dict:
        """Elimina un cliente"""
        for index, cliente in enumerate(self.clientes_db):
            if cliente.idCliente == id_cliente:
                self.clientes_db.pop(index)
                self._guardar_datos()
                return {"mensaje": "Cliente eliminado exitosamente"}
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    def buscar_clientes_por_tipo_documento(self, tipo_documento: str) -> List[Cliente]:
        """Busca clientes por tipo de documento"""
        clientes_filtrados = [
            cliente for cliente in self.clientes_db 
            if cliente.tipoDocumento.lower() == tipo_documento.lower()
        ]
        return clientes_filtrados
