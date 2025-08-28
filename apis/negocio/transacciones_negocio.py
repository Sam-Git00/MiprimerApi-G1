from typing import List
from fastapi import HTTPException
from entidades.transaccion import Transaccion, TransaccionCrear, OperacionBancaria, TransferenciaBancaria, TipoTransaccion, EstadoTransaccion
from negocio.cuenta_negocio import CuentaNegocio
from datetime import datetime
import json
import os

class TransaccionNegocio:
    def __init__(self):
        self.archivo_datos = "datos/transacciones.json"
        self.cuenta_negocio = CuentaNegocio()
        self._cargar_datos()
        self.contador_id = self._obtener_siguiente_id()
    
    def _cargar_datos(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.transacciones_db = []
                for transaccion_data in datos:
                    # Convertir string de fecha a datetime
                    if isinstance(transaccion_data['fechaTransaccion'], str):
                        transaccion_data['fechaTransaccion'] = datetime.fromisoformat(transaccion_data['fechaTransaccion'])
                    self.transacciones_db.append(Transaccion(**transaccion_data))
        else:
            self.transacciones_db = []
    
    def _guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo_datos), exist_ok=True)
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            datos = []
            for transaccion in self.transacciones_db:
                transaccion_dict = transaccion.dict()
                # Convertir datetime a string para JSON
                transaccion_dict['fechaTransaccion'] = transaccion.fechaTransaccion.isoformat()
                datos.append(transaccion_dict)
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def _obtener_siguiente_id(self) -> int:
        """Obtiene el siguiente ID disponible"""
        if not self.transacciones_db:
            return 1
        return max(transaccion.idTransaccion for transaccion in self.transacciones_db) + 1
    
    def obtener_todas_transacciones(self) -> List[Transaccion]:
        """Obtiene todas las transacciones"""
        return self.transacciones_db
    
    def obtener_transaccion_por_id(self, id_transaccion: int) -> Transaccion:
        """Obtiene una transacción por su ID"""
        for transaccion in self.transacciones_db:
            if transaccion.idTransaccion == id_transaccion:
                return transaccion
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    def consignar(self, operacion: OperacionBancaria) -> dict:
        """Realiza una consignación"""
        # Validar que la cuenta existe
        cuenta = self.cuenta_negocio.obtener_cuenta_por_numero(operacion.numeroCuenta)
        
        # Validar monto positivo
        if operacion.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
        
        # Actualizar saldo
        nuevo_saldo = cuenta.saldoActual + operacion.monto
        self.cuenta_negocio.actualizar_saldo(operacion.numeroCuenta, nuevo_saldo)
        
        # Crear transacción
        transaccion = Transaccion(
            idTransaccion=self.contador_id,
            numeroCuentaOrigen=operacion.numeroCuenta,
            tipoTransaccion=TipoTransaccion.CONSIGNACION,
            montoTransaccion=operacion.monto,
            descripcionTransaccion=operacion.descripcion,
            estadoTransaccion=EstadoTransaccion.EXITOSA
        )
        
        self.transacciones_db.append(transaccion)
        self.contador_id += 1
        self._guardar_datos()
        
        return {
            "mensaje": "Consignación exitosa",
            "transaccion": transaccion,
            "saldoAnterior": cuenta.saldoActual,
            "saldoNuevo": nuevo_saldo
        }
    
    def retirar(self, operacion: OperacionBancaria) -> dict:
        """Realiza un retiro"""
        # Validar que la cuenta existe
        cuenta = self.cuenta_negocio.obtener_cuenta_por_numero(operacion.numeroCuenta)
        
        # Validar monto positivo
        if operacion.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
        
        # Validar saldo suficiente
        if cuenta.saldoActual < operacion.monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        
        # Actualizar saldo
        nuevo_saldo = cuenta.saldoActual - operacion.monto
        self.cuenta_negocio.actualizar_saldo(operacion.numeroCuenta, nuevo_saldo)
        
        # Crear transacción
        transaccion = Transaccion(
            idTransaccion=self.contador_id,
            numeroCuentaOrigen=operacion.numeroCuenta,
            tipoTransaccion=TipoTransaccion.RETIRO,
            montoTransaccion=operacion.monto,
            descripcionTransaccion=operacion.descripcion,
            estadoTransaccion=EstadoTransaccion.EXITOSA
        )
        
        self.transacciones_db.append(transaccion)
        self.contador_id += 1
        self._guardar_datos()
        
        return {
            "mensaje": "Retiro exitoso",
            "transaccion": transaccion,
            "saldoAnterior": cuenta.saldoActual + operacion.monto,
            "saldoNuevo": nuevo_saldo
        }
    
    def transferir(self, transferencia: TransferenciaBancaria) -> dict:
        """Realiza una transferencia entre cuentas"""
        # Validar que ambas cuentas existen
        cuenta_origen = self.cuenta_negocio.obtener_cuenta_por_numero(transferencia.numeroCuentaOrigen)
        cuenta_destino = self.cuenta_negocio.obtener_cuenta_por_numero(transferencia.numeroCuentaDestino)
        
        # Validar monto positivo
        if transferencia.monto <= 0:
            raise HTTPException(status_code=400, detail="El monto debe ser mayor a cero")
        
        # Validar saldo suficiente
        if cuenta_origen.saldoActual < transferencia.monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente en cuenta origen")
        
        # Actualizar saldos
        nuevo_saldo_origen = cuenta_origen.saldoActual - transferencia.monto
        nuevo_saldo_destino = cuenta_destino.saldoActual + transferencia.monto
        
        self.cuenta_negocio.actualizar_saldo(transferencia.numeroCuentaOrigen, nuevo_saldo_origen)
        self.cuenta_negocio.actualizar_saldo(transferencia.numeroCuentaDestino, nuevo_saldo_destino)
        
        # Crear transacción
        transaccion = Transaccion(
            idTransaccion=self.contador_id,
            numeroCuentaOrigen=transferencia.numeroCuentaOrigen,
            numeroCuentaDestino=transferencia.numeroCuentaDestino,
            tipoTransaccion=TipoTransaccion.TRANSFERENCIA,
            montoTransaccion=transferencia.monto,
            descripcionTransaccion=transferencia.descripcion,
            estadoTransaccion=EstadoTransaccion.EXITOSA
        )
        
        self.transacciones_db.append(transaccion)
        self.contador_id += 1
        self._guardar_datos()
        
        return {
            "mensaje": "Transferencia exitosa",
            "transaccion": transaccion,
            "saldoOrigenAnterior": cuenta_origen.saldoActual,
            "saldoOrigenNuevo": nuevo_saldo_origen,
            "saldoDestinoAnterior": cuenta_destino.saldoActual - transferencia.monto,
            "saldoDestinoNuevo": nuevo_saldo_destino
        }
    
    def obtener_transacciones_por_cuenta(self, numero_cuenta: str) -> List[Transaccion]:
        """Obtiene todas las transacciones de una cuenta"""
        transacciones_cuenta = [
            transaccion for transaccion in self.transacciones_db 
            if transaccion.numeroCuentaOrigen == numero_cuenta or 
               transaccion.numeroCuentaDestino == numero_cuenta
        ]
        return transacciones_cuenta
    
    def obtener_transacciones_por_tipo(self, tipo_transaccion: str) -> List[Transaccion]:
        """Obtiene transacciones filtradas por tipo"""
        transacciones_filtradas = [
            transaccion for transaccion in self.transacciones_db 
            if transaccion.tipoTransaccion.value.lower() == tipo_transaccion.lower()
        ]
        return transacciones_filtradas
