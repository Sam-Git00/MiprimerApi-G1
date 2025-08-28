from typing import List, Optional
from fastapi import HTTPException
from entidades.cuenta import Cuenta, CuentaCrear, TipoCuenta, EstadoCuenta
from negocio.cliente_negocio import ClienteNegocio
import json
import os
import random

class CuentaNegocio:
    def __init__(self):
        self.archivo_datos = "datos/cuentas.json"
        self.cliente_negocio = ClienteNegocio()
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.cuentas_db = [Cuenta(**cuenta) for cuenta in datos]
        else:
            self.cuentas_db = []
    
    def _guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo_datos), exist_ok=True)
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            datos = [cuenta.dict() for cuenta in self.cuentas_db]
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def _generar_numero_cuenta(self) -> str:
        """Genera un número de cuenta único"""
        while True:
            numero = f"100{random.randint(1000000, 9999999)}"
            if not any(cuenta.numeroCuenta == numero for cuenta in self.cuentas_db):
                return numero
    
    def obtener_todas_cuentas(self) -> List[Cuenta]:
        """Obtiene todas las cuentas"""
        return self.cuentas_db
    
    def obtener_cuenta_por_numero(self, numero_cuenta: str) -> Cuenta:
        """Obtiene una cuenta por su número"""
        for cuenta in self.cuentas_db:
            if cuenta.numeroCuenta == numero_cuenta:
                return cuenta
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    def crear_cuenta(self, datos_cuenta: CuentaCrear) -> Cuenta:
        """Crea una nueva cuenta"""
        # Validar que el cliente existe
        self.cliente_negocio.obtener_cliente_por_id(datos_cuenta.idCliente)
        
        # Generar número de cuenta único
        numero_cuenta = self._generar_numero_cuenta()
        
        # Configurar límite según tipo de cuenta
        limite = None
        if datos_cuenta.tipoCuenta == TipoCuenta.CREDITO:
            limite = datos_cuenta.limiteCuenta or 1000000.0
        
        nueva_cuenta = Cuenta(
            numeroCuenta=numero_cuenta,
            idCliente=datos_cuenta.idCliente,
            tipoCuenta=datos_cuenta.tipoCuenta,
            saldoActual=datos_cuenta.saldoInicial,
            limiteCuenta=limite,
            estadoCuenta=EstadoCuenta.ACTIVA
        )
        
        self.cuentas_db.append(nueva_cuenta)
        self._guardar_datos()
        return nueva_cuenta
    
    def actualizar_cuenta(self, numero_cuenta: str, estado_cuenta: EstadoCuenta) -> Cuenta:
        """Actualiza el estado de una cuenta"""
        for index, cuenta in enumerate(self.cuentas_db):
            if cuenta.numeroCuenta == numero_cuenta:
                cuenta_actualizada = cuenta.copy(update={"estadoCuenta": estado_cuenta})
                self.cuentas_db[index] = cuenta_actualizada
                self._guardar_datos()
                return cuenta_actualizada
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    def eliminar_cuenta(self, numero_cuenta: str) -> dict:
        """Elimina una cuenta"""
        for index, cuenta in enumerate(self.cuentas_db):
            if cuenta.numeroCuenta == numero_cuenta:
                if cuenta.saldoActual != 0:
                    raise HTTPException(status_code=400, detail="No se puede eliminar una cuenta con saldo diferente a cero")
                self.cuentas_db.pop(index)
                self._guardar_datos()
                return {"mensaje": "Cuenta eliminada exitosamente"}
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    def obtener_cuentas_por_cliente(self, id_cliente: int) -> List[Cuenta]:
        """Obtiene todas las cuentas de un cliente"""
        cuentas_cliente = [cuenta for cuenta in self.cuentas_db if cuenta.idCliente == id_cliente]
        return cuentas_cliente
    
    def obtener_cuentas_por_tipo(self, tipo_cuenta: str) -> List[Cuenta]:
        """Obtiene cuentas filtradas por tipo"""
        cuentas_filtradas = [
            cuenta for cuenta in self.cuentas_db 
            if cuenta.tipoCuenta.value.lower() == tipo_cuenta.lower()
        ]
        return cuentas_filtradas
    
    def actualizar_saldo(self, numero_cuenta: str, nuevo_saldo: float):
        """Actualiza el saldo de una cuenta"""
        for index, cuenta in enumerate(self.cuentas_db):
            if cuenta.numeroCuenta == numero_cuenta:
                cuenta_actualizada = cuenta.copy(update={"saldoActual": nuevo_saldo})
                self.cuentas_db[index] = cuenta_actualizada
                self._guardar_datos()
                return cuenta_actualizada
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
