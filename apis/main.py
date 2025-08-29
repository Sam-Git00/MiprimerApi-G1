
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import json
import os
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="API Bancaria G1 - Versión Simplificada",
    description="API para sistema bancario con funcionalidades básicas",
    version="1.0.0"
)

# Modelos Pydantic simplificados
class ClienteSimple(BaseModel):
    idCliente: int
    nombreCompleto: str
    correoElectronico: str
    numeroTelefono: str
    numeroDocumento: str
    tipoDocumento: str

class CuentaSimple(BaseModel):
    numeroCuenta: str
    idCliente: int
    tipoCuenta: str
    saldoActual: float
    estadoCuenta: str

class TransaccionSimple(BaseModel):
    idTransaccion: int
    numeroCuentaOrigen: str
    tipoTransaccion: str
    montoTransaccion: float
    descripcionTransaccion: str

# Modelos para endpoints especiales
class OperacionConsignacion(BaseModel):
    numeroCuenta: str
    monto: float
    descripcion: str = "Consignación"

class OperacionRetiro(BaseModel):
    numeroCuenta: str
    monto: float
    descripcion: str = "Retiro"

class OperacionTransferencia(BaseModel):
    numeroCuentaOrigen: str
    numeroCuentaDestino: str
    monto: float
    descripcion: str = "Transferencia"

# Datos en memoria (simulando base de datos)
clientes_db = []
cuentas_db = []
transacciones_db = []

def cargar_datos():
    """Carga datos desde archivos JSON"""
    try:
        # Cargar clientes
        if os.path.exists("datos/clientes.json"):
            with open("datos/clientes.json", 'r', encoding='utf-8') as f:
                clientes_db.extend(json.load(f))
        
        # Cargar cuentas
        if os.path.exists("datos/cuentas.json"):
            with open("datos/cuentas.json", 'r', encoding='utf-8') as f:
                cuentas_db.extend(json.load(f))
        
        # Cargar transacciones
        if os.path.exists("datos/transacciones.json"):
            with open("datos/transacciones.json", 'r', encoding='utf-8') as f:
                transacciones_db.extend(json.load(f))
                
        print(f"✅ Datos cargados: {len(clientes_db)} clientes, {len(cuentas_db)} cuentas, {len(transacciones_db)} transacciones")
    except Exception as e:
        print(f"⚠️ Error cargando datos: {e}")

# Cargar datos al iniciar
cargar_datos()

# Ruta raíz
@app.get("/", tags=["Información"],
         summary="Información general de la API",
         description="Endpoint principal que proporciona información general sobre la API bancaria, incluyendo versión y endpoints disponibles.",
         response_description="Información general de la API bancaria")
def read_root():
    """
    ## Información General de la API Bancaria
    
    Este endpoint proporciona información básica sobre la API bancaria G1.
    
    ### Información incluida:
    - **message**: Nombre y descripción de la API
    - **version**: Versión actual del servicio
    - **endpoints**: Lista de endpoints principales disponibles
    - **documentación**: Enlace a la documentación interactiva
    
    ### Endpoints disponibles:
    - **/clientes**: Gestión de clientes bancarios
    - **/cuentas**: Gestión de cuentas bancarias
    - **/transacciones**: Gestión de transacciones bancarias
    - **/health**: Verificación de estado de la API
    - **/docs**: Documentación interactiva (Swagger UI)
    
    ### Ejemplo de respuesta: (Intentar mejorar)
    ```json
    {
        "message": "API Bancaria G1 - Versión Simplificada",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "cuentas": "/cuentas",
            "transacciones": "/transacciones"
        },
        "documentación": "/docs"
    }
    ```
    """
    return {
        "message": "API Bancaria G1 - Versión Simplificada",
        "version": "1.0.0",
        "endpoints": {
            "clientes": "/clientes",
            "cuentas": "/cuentas", 
            "transacciones": "/transacciones"
        },
        "documentación": "/docs"
    }

@app.get("/health", tags=["Salud"], 
         summary="Verificar estado de la API",
         description="Endpoint para verificar que la API esté funcionando correctamente. Retorna información detallada sobre el estado del servicio, incluyendo métricas y timestamp.",
         response_description="Información detallada del estado de salud de la API",
         responses={
             200: {
                 "description": "API funcionando correctamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "status": "healthy",
                             "message": "API funcionando correctamente",
                             "timestamp": "2024-01-15T10:30:00",
                             "version": "1.0.0",
                             "uptime": "2h 15m 30s",
                             "databases": {
                                 "clientes": 4,
                                 "cuentas": 3,
                                 "transacciones": 2
                             }
                         }
                     }
                 }
             }
         })
def health_check():
    """
    ## Verificación de Estado de la API
    
    Este endpoint permite verificar que la API bancaria esté funcionando correctamente.
    
    ### Respuesta
    - **status**: Estado actual de la API ("healthy", "degraded", "unhealthy")
    - **message**: Mensaje descriptivo del estado
    - **timestamp**: Fecha y hora exacta de la verificación
    - **version**: Versión actual de la API
    - **uptime**: Tiempo de actividad del servicio (simulado)
    - **databases**: Métricas de los datos cargados en memoria
    
    ### Uso
    Útil para:
    - Monitoreo de disponibilidad
    - Health checks automáticos
    - Verificación rápida de conectividad
    - Análisis de métricas de datos
    
    ### Ejemplo de respuesta:
    ```json
    {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "timestamp": "2024-01-15T10:30:00",
        "version": "1.0.0",
        "uptime": "2h 15m 30s",
        "databases": {
            "clientes": 4,
            "cuentas": 3,
            "transacciones": 2
        }
    }
    ```
    """
    # Verificar archivos de datos
    archivos_ok = all([
        os.path.exists("datos/clientes.json"),
        os.path.exists("datos/cuentas.json"),
        os.path.exists("datos/transacciones.json")
    ])
    
    # Determinar estado basado en verificaciones
    if archivos_ok and len(clientes_db) > 0:
        status = "healthy"
        message = "API funcionando correctamente"
    elif archivos_ok:
        status = "degraded"
        message = "API funcionando pero sin datos cargados"
    else:
        status = "unhealthy"
        message = "Problemas con archivos de datos"
    
    # Simular uptime (en un caso real se calcularía desde el inicio)
    uptime = "2h 15m 30s"  # Simulado
    
    return {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": uptime,
        "databases": {
            "clientes": len(clientes_db),
            "cuentas": len(cuentas_db),
            "transacciones": len(transacciones_db)
        }
    }

# ===== ENDPOINTS DE CLIENTES =====
@app.get("/clientes", tags=["Clientes"], 
         summary="Obtener lista de clientes",
         description="Retorna la lista completa de clientes bancarios. Permite filtrar por tipo de documento (CC, CE, NIT, etc.).",
         response_description="Lista de clientes bancarios",
         response_model=List[ClienteSimple],
         responses={
             200: {
                 "description": "Lista de clientes obtenida exitosamente",
                 "content": {
                     "application/json": {
                         "example": [
                             {
                                 "idCliente": 1,
                                 "nombreCompleto": "Juan Pérez",
                                 "correoElectronico": "juan.perez@email.com",
                                 "numeroTelefono": "3001234567",
                                 "numeroDocumento": "12345678",
                                 "tipoDocumento": "CC"
                             },
                             {
                                 "idCliente": 2,
                                 "nombreCompleto": "María García",
                                 "correoElectronico": "maria.garcia@email.com",
                                 "numeroTelefono": "3109876543",
                                 "numeroDocumento": "87654321",
                                 "tipoDocumento": "CC"
                             }
                         ]
                     }
                 }
             }
         })
def obtener_clientes(tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento (CC, CE, NIT, etc.)")):
    """
    ## Obtener Lista de Clientes
    
    Este endpoint retorna la lista completa de clientes bancarios registrados en el sistema.
    
    ### Parámetros de consulta:
    - **tipo_documento** (opcional): Filtra clientes por tipo de documento
      - Valores válidos: CC, CE, NIT, TI, PP
    
    ### Respuesta:
    - **200**: Lista de clientes obtenida exitosamente
    - **404**: No se encontraron clientes (si se aplica filtro)
    
    ### Ejemplo de uso:
    ```
    GET /clientes                    # Obtener todos los clientes
    GET /clientes?tipo_documento=CC  # Obtener solo clientes con cédula
    ```
    """
    if tipo_documento:
        clientes_filtrados = [c for c in clientes_db if c["tipoDocumento"].lower() == tipo_documento.lower()]
        if not clientes_filtrados:
            raise HTTPException(status_code=404, detail=f"No se encontraron clientes con tipo de documento: {tipo_documento}")
        return clientes_filtrados
    return clientes_db

@app.get("/clientes/{id_cliente}", tags=["Clientes"], 
         summary="Obtener cliente por ID",
         description="Retorna la información detallada de un cliente específico basado en su ID único.",
         response_description="Información del cliente solicitado",
         response_model=ClienteSimple,
         responses={
             200: {
                 "description": "Cliente encontrado exitosamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "idCliente": 1,
                             "nombreCompleto": "Juan Pérez",
                             "correoElectronico": "juan.perez@email.com",
                             "numeroTelefono": "3001234567",
                             "numeroDocumento": "12345678",
                             "tipoDocumento": "CC"
                         }
                     }
                 }
             },
             404: {
                 "description": "Cliente no encontrado",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": "Cliente no encontrado"
                         }
                     }
                 }
             }
         })
def obtener_cliente(id_cliente: int):
    """
    ## Obtener Cliente por ID
    
    Este endpoint retorna la información completa de un cliente específico.
    
    ### Parámetros de ruta:
    - **id_cliente** (int): ID único del cliente a consultar
    
    ### Respuesta:
    - **200**: Cliente encontrado exitosamente
    - **404**: Cliente no encontrado
    
    ### Ejemplo de uso:
    ```
    GET /clientes/1  # Obtener cliente con ID 1
    ```
    """
    for cliente in clientes_db:
        if cliente["idCliente"] == id_cliente:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.post("/clientes", tags=["Clientes"], 
          summary="Crear nuevo cliente",
          description="Crea un nuevo cliente bancario en el sistema. Valida que el ID del cliente no exista previamente.",
          response_description="Cliente creado exitosamente",
          status_code=201, 
          response_model=ClienteSimple,
          responses={
              201: {
                  "description": "Cliente creado exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "idCliente": 3,
                              "nombreCompleto": "Ana López",
                              "correoElectronico": "ana.lopez@email.com",
                              "numeroTelefono": "315789456",
                              "numeroDocumento": "98765432",
                              "tipoDocumento": "CC"
                          }
                      }
                  }
              },
              400: {
                  "description": "ID de cliente ya existe",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "El ID del cliente ya existe"
                          }
                      }
                  }
              }
          })
def crear_cliente(cliente: ClienteSimple):
    """
    ## Crear Nuevo Cliente
    
    Este endpoint permite crear un nuevo cliente bancario en el sistema.
    
    ### Cuerpo de la petición:
    - **idCliente** (int): ID único del cliente
    - **nombreCompleto** (str): Nombre completo del cliente
    - **correoElectronico** (str): Correo electrónico válido
    - **numeroTelefono** (str): Número de teléfono
    - **numeroDocumento** (str): Número del documento de identidad
    - **tipoDocumento** (str): Tipo de documento (CC, CE, NIT, etc.)
    
    ### Respuesta:
    - **201**: Cliente creado exitosamente
    - **400**: ID de cliente ya existe
    
    ### Ejemplo de request body:
    ```json
    {
        "idCliente": 3,
        "nombreCompleto": "Ana López",
        "correoElectronico": "ana.lopez@email.com",
        "numeroTelefono": "315789456",
        "numeroDocumento": "98765432",
        "tipoDocumento": "CC"
    }
    ```
    """
    # Validar que no exista el ID
    for c in clientes_db:
        if c["idCliente"] == cliente.idCliente:
            raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    
    cliente_dict = cliente.model_dump()
    clientes_db.append(cliente_dict)
    return cliente_dict

@app.put("/clientes/{id_cliente}", tags=["Clientes"], 
         summary="Actualizar cliente",
         description="Actualiza la información de un cliente existente basado en su ID.",
         response_description="Cliente actualizado exitosamente",
         response_model=ClienteSimple,
         responses={
             200: {
                  "description": "Cliente actualizado exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "idCliente": 1,
                              "nombreCompleto": "Juan Pérez Actualizado",
                              "correoElectronico": "juan.nuevo@email.com",
                              "numeroTelefono": "3001234567",
                              "numeroDocumento": "12345678",
                              "tipoDocumento": "CC"
                          }
                      }
                  }
              },
             404: {
                  "description": "Cliente no encontrado",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Cliente no encontrado"
                          }
                      }
                  }
              }
         })
def actualizar_cliente(id_cliente: int, cliente: ClienteSimple):
    """
    ## Actualizar Cliente
    
    Este endpoint permite actualizar la información de un cliente existente.
    
    ### Parámetros de ruta:
    - **id_cliente** (int): ID del cliente a actualizar
    
    ### Cuerpo de la petición:
    - **idCliente** (int): ID único del cliente
    - **nombreCompleto** (str): Nombre completo del cliente
    - **correoElectronico** (str): Correo electrónico válido
    - **numeroTelefono** (str): Número de teléfono
    - **numeroDocumento** (str): Número del documento de identidad
    - **tipoDocumento** (str): Tipo de documento (CC, CE, NIT, etc.)
    
    ### Respuesta:
    - **200**: Cliente actualizado exitosamente
    - **404**: Cliente no encontrado
    
    ### Ejemplo de request body:
    ```json
    {
        "idCliente": 1,
        "nombreCompleto": "Juan Pérez Actualizado",
        "correoElectronico": "juan.nuevo@email.com",
        "numeroTelefono": "3001234567",
        "numeroDocumento": "12345678",
        "tipoDocumento": "CC"
    }
    ```
    """
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            cliente_dict = cliente.model_dump()
            clientes_db[i] = cliente_dict
            return cliente_dict
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/{id_cliente}", tags=["Clientes"],
           summary="Eliminar cliente",
           description="Elimina un cliente del sistema basado en su ID único.",
           response_description="Cliente eliminado exitosamente",
           responses={
               200: {
                   "description": "Cliente eliminado exitosamente",
                   "content": {
                       "application/json": {
                           "example": {
                               "mensaje": "Cliente 1 eliminado"
                           }
                       }
                   }
               },
               404: {
                   "description": "Cliente no encontrado",
                   "content": {
                       "application/json": {
                           "example": {
                               "detail": "Cliente no encontrado"
                           }
                       }
                   }
               }
           })
def eliminar_cliente(id_cliente: int):
    """
    ## Eliminar Cliente
    
    Este endpoint permite eliminar un cliente del sistema.
    
    ### Parámetros de ruta:
    - **id_cliente** (int): ID del cliente a eliminar
    
    ### Respuesta:
    - **200**: Cliente eliminado exitosamente
    - **404**: Cliente no encontrado
    
    ### Ejemplo de uso:
    ```
    DELETE /clientes/1  # Eliminar cliente con ID 1
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Cliente 1 eliminado"
    }
    ```
    """
    for i, c in enumerate(clientes_db):
        if c["idCliente"] == id_cliente:
            clientes_db.pop(i)
            return {"mensaje": f"Cliente {id_cliente} eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# ===== ENDPOINTS DE CUENTAS =====
@app.get("/cuentas", tags=["Cuentas"], 
         summary="Obtener lista de cuentas",
         description="Retorna la lista completa de cuentas bancarias. Permite filtrar por tipo de cuenta (Ahorros, Corriente, etc.).",
         response_description="Lista de cuentas bancarias",
         response_model=List[CuentaSimple],
         responses={
             200: {
                 "description": "Lista de cuentas obtenida exitosamente",
                 "content": {
                     "application/json": {
                         "example": [
                             {
                                 "numeroCuenta": "1234567890",
                                 "idCliente": 1,
                                 "tipoCuenta": "Ahorros",
                                 "saldoActual": 1500000.50,
                                 "estadoCuenta": "Activa"
                             },
                             {
                                 "numeroCuenta": "0987654321",
                                 "idCliente": 2,
                                 "tipoCuenta": "Corriente",
                                 "saldoActual": 2500000.00,
                                 "estadoCuenta": "Activa"
                             }
                         ]
                     }
                 }
             }
         })
def obtener_cuentas(tipo_cuenta: Optional[str] = Query(None, description="Filtrar por tipo de cuenta (Ahorros, Corriente, etc.)")):
    """
    ## Obtener Lista de Cuentas
    
    Este endpoint retorna la lista completa de cuentas bancarias registradas en el sistema.
    
    ### Parámetros de consulta:
    - **tipo_cuenta** (opcional): Filtra cuentas por tipo
      - Valores válidos: Ahorros, Corriente, CDT, etc.
    
    ### Respuesta:
    - **200**: Lista de cuentas obtenida exitosamente
    - **404**: No se encontraron cuentas (si se aplica filtro)
    
    ### Ejemplo de uso:
    ```
    GET /cuentas                    # Obtener todas las cuentas
    GET /cuentas?tipo_cuenta=Ahorros  # Obtener solo cuentas de ahorros
    ```
    """
    if tipo_cuenta:
        cuentas_filtradas = [c for c in cuentas_db if c["tipoCuenta"].lower() == tipo_cuenta.lower()]
        if not cuentas_filtradas:
            raise HTTPException(status_code=404, detail=f"No se encontraron cuentas con tipo: {tipo_cuenta}")
        return cuentas_filtradas
    return cuentas_db

@app.get("/cuentas/{numero_cuenta}", tags=["Cuentas"], 
         summary="Obtener cuenta por número",
         description="Retorna la información detallada de una cuenta específica basada en su número único.",
         response_description="Información de la cuenta solicitada",
         response_model=CuentaSimple,
         responses={
             200: {
                 "description": "Cuenta encontrada exitosamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "numeroCuenta": "1234567890",
                             "idCliente": 1,
                             "tipoCuenta": "Ahorros",
                             "saldoActual": 1500000.50,
                             "estadoCuenta": "Activa"
                         }
                     }
                 }
             },
             404: {
                 "description": "Cuenta no encontrada",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": "Cuenta no encontrada"
                         }
                     }
                 }
             }
         })
def obtener_cuenta(numero_cuenta: str):
    """
    ## Obtener Cuenta por Número
    
    Este endpoint retorna la información completa de una cuenta específica.
    
    ### Parámetros de ruta:
    - **numero_cuenta** (str): Número único de la cuenta a consultar
    
    ### Respuesta:
    - **200**: Cuenta encontrada exitosamente
    - **404**: Cuenta no encontrada
    
    ### Ejemplo de uso:
    ```
    GET /cuentas/1234567890  # Obtener cuenta con número 1234567890
    ```
    """
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == numero_cuenta:
            return cuenta
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")

@app.post("/cuentas", tags=["Cuentas"], 
          summary="Crear nueva cuenta",
          description="Crea una nueva cuenta bancaria en el sistema.",
          response_description="Cuenta creada exitosamente",
          status_code=201, 
          response_model=CuentaSimple,
          responses={
              201: {
                  "description": "Cuenta creada exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "numeroCuenta": "5555666677",
                              "idCliente": 3,
                              "tipoCuenta": "Ahorros",
                              "saldoActual": 0.00,
                              "estadoCuenta": "Activa"
                          }
                      }
                  }
              }
          })
def crear_cuenta(cuenta: CuentaSimple):
    """
    ## Crear Nueva Cuenta
    
    Este endpoint permite crear una nueva cuenta bancaria en el sistema.
    
    ### Cuerpo de la petición:
    - **numeroCuenta** (str): Número único de la cuenta
    - **idCliente** (int): ID del cliente propietario
    - **tipoCuenta** (str): Tipo de cuenta (Ahorros, Corriente, etc.)
    - **saldoActual** (float): Saldo inicial de la cuenta
    - **estadoCuenta** (str): Estado de la cuenta (Activa, Inactiva, Bloqueada)
    
    ### Respuesta:
    - **201**: Cuenta creada exitosamente
    
    ### Ejemplo de request body:
    ```json
    {
        "numeroCuenta": "5555666677",
        "idCliente": 3,
        "tipoCuenta": "Ahorros",
        "saldoActual": 0.00,
        "estadoCuenta": "Activa"
    }
    ```
    """
    cuenta_dict = cuenta.model_dump()
    cuentas_db.append(cuenta_dict)
    return cuenta_dict

@app.put("/cuentas/{numero_cuenta}", tags=["Cuentas"], 
         summary="Actualizar cuenta",
         description="Actualiza la información de una cuenta existente basada en su número único.",
         response_description="Cuenta actualizada exitosamente",
         response_model=CuentaSimple,
         responses={
             200: {
                 "description": "Cuenta actualizada exitosamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "numeroCuenta": "1234567890",
                             "idCliente": 1,
                             "tipoCuenta": "Ahorros",
                             "saldoActual": 2000000.00,
                             "estadoCuenta": "Activa"
                         }
                     }
                 }
             },
             404: {
                 "description": "Cuenta no encontrada",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": "Cuenta no encontrada"
                         }
                     }
                 }
             }
         })
def actualizar_cuenta(numero_cuenta: str, cuenta: CuentaSimple):
    """
    ## Actualizar Cuenta
    
    Este endpoint permite actualizar la información de una cuenta existente.
    
    ### Parámetros de ruta:
    - **numero_cuenta** (str): Número de la cuenta a actualizar
    
    ### Cuerpo de la petición:
    - **numeroCuenta** (str): Número único de la cuenta
    - **idCliente** (int): ID del cliente propietario
    - **tipoCuenta** (str): Tipo de cuenta (Ahorros, Corriente, etc.)
    - **saldoActual** (float): Saldo actual de la cuenta
    - **estadoCuenta** (str): Estado de la cuenta (Activa, Inactiva, Bloqueada)
    
    ### Respuesta:
    - **200**: Cuenta actualizada exitosamente
    - **404**: Cuenta no encontrada
    
    ### Ejemplo de request body:
    ```json
    {
        "numeroCuenta": "1234567890",
        "idCliente": 1,
        "tipoCuenta": "Ahorros",
        "saldoActual": 2000000.00,
        "estadoCuenta": "Activa"
    }
    ```
    """
    for i, c in enumerate(cuentas_db):
        if c["numeroCuenta"] == numero_cuenta:
            cuenta_dict = cuenta.model_dump()
            cuentas_db[i] = cuenta_dict
            return cuenta_dict
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")

@app.delete("/cuentas/{numero_cuenta}", tags=["Cuentas"],
           summary="Eliminar cuenta",
           description="Elimina una cuenta del sistema basada en su número único.",
           response_description="Cuenta eliminada exitosamente",
           responses={
               200: {
                   "description": "Cuenta eliminada exitosamente",
                   "content": {
                       "application/json": {
                           "example": {
                               "mensaje": "Cuenta 1234567890 eliminada"
                           }
                       }
                   }
               },
               404: {
                   "description": "Cuenta no encontrada",
                   "content": {
                       "application/json": {
                           "example": {
                               "detail": "Cuenta no encontrada"
                           }
                       }
                   }
               }
           })
def eliminar_cuenta(numero_cuenta: str):
    """
    ## Eliminar Cuenta
    
    Este endpoint permite eliminar una cuenta del sistema.
    
    ### Parámetros de ruta:
    - **numero_cuenta** (str): Número de la cuenta a eliminar
    
    ### Respuesta:
    - **200**: Cuenta eliminada exitosamente
    - **404**: Cuenta no encontrada
    
    ### Ejemplo de uso:
    ```
    DELETE /cuentas/1234567890  # Eliminar cuenta con número 1234567890
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Cuenta 1234567890 eliminada"
    }
    ```
    """
    for i, c in enumerate(cuentas_db):
        if c["numeroCuenta"] == numero_cuenta:
            cuentas_db.pop(i)
            return {"mensaje": f"Cuenta {numero_cuenta} eliminada"}
    raise HTTPException(status_code=404, detail="Cuenta no encontrada")

# ===== ENDPOINTS DE TRANSACCIONES =====
@app.get("/transacciones", tags=["Transacciones"], 
         summary="Obtener lista de transacciones",
         description="Retorna la lista completa de transacciones bancarias. Permite filtrar por tipo de transacción (no usar tildes-Consignacion, Retiro, Transferencia, etc.).",
         response_description="Lista de transacciones bancarias",
         response_model=List[TransaccionSimple],
         responses={
             200: {
                 "description": "Lista de transacciones obtenida exitosamente",
                 "content": {
                     "application/json": {
                         "example": [
                             {
                                 "idTransaccion": 1,
                                 "numeroCuentaOrigen": "1234567890",
                                 "tipoTransaccion": "Consignación",
                                 "montoTransaccion": 500000.00,
                                 "descripcionTransaccion": "Consignación inicial"
                             },
                             {
                                 "idTransaccion": 2,
                                 "numeroCuentaOrigen": "1234567890",
                                 "tipoTransaccion": "Retiro",
                                 "montoTransaccion": 100000.00,
                                 "descripcionTransaccion": "Retiro en cajero"
                             }
                         ]
                     }
                 }
             }
         })
def obtener_transacciones(tipo_transaccion: Optional[str] = Query(None, description="Filtrar por tipo de transacción (Consignación, Retiro, Transferencia, etc.)")):
    """
    ## Obtener Lista de Transacciones
    
    Este endpoint retorna la lista completa de transacciones bancarias registradas en el sistema.
    
    ### Parámetros de consulta:
    - **tipo_transaccion** (opcional): Filtra transacciones por tipo
      - Valores válidos: Consignación, Retiro, Transferencia, etc.
    
    ### Respuesta:
    - **200**: Lista de transacciones obtenida exitosamente
    - **404**: No se encontraron transacciones (si se aplica filtro)
    
    ### Ejemplo de uso:
    ```
    GET /transacciones                    # Obtener todas las transacciones
    GET /transacciones?tipo_transaccion=Consignación  # Obtener solo consignaciones
    ```
    """
    if tipo_transaccion:
        transacciones_filtradas = [t for t in transacciones_db if t["tipoTransaccion"].lower() == tipo_transaccion.lower()]
        if not transacciones_filtradas:
            raise HTTPException(status_code=404, detail=f"No se encontraron transacciones con tipo: {tipo_transaccion}")
        return transacciones_filtradas
    return transacciones_db

@app.get("/transacciones/{id_transaccion}", tags=["Transacciones"], 
         summary="Obtener transacción por ID",
         description="Retorna la información detallada de una transacción específica basada en su ID único.",
         response_description="Información de la transacción solicitada",
         response_model=TransaccionSimple,
         responses={
             200: {
                 "description": "Transacción encontrada exitosamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "idTransaccion": 1,
                             "numeroCuentaOrigen": "1234567890",
                             "tipoTransaccion": "Consignación",
                             "montoTransaccion": 500000.00,
                             "descripcionTransaccion": "Consignación inicial"
                         }
                     }
                 }
             },
             404: {
                 "description": "Transacción no encontrada",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": "Transacción no encontrada"
                         }
                     }
                 }
             }
         })
def obtener_transaccion(id_transaccion: int):
    """
    ## Obtener Transacción por ID
    
    Este endpoint retorna la información completa de una transacción específica.
    
    ### Parámetros de ruta:
    - **id_transaccion** (int): ID único de la transacción a consultar
    
    ### Respuesta:
    - **200**: Transacción encontrada exitosamente
    - **404**: Transacción no encontrada
    
    ### Ejemplo de uso:
    ```
    GET /transacciones/1  # Obtener transacción con ID 1
    ```
    """
    for transaccion in transacciones_db:
        if transaccion["idTransaccion"] == id_transaccion:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.post("/transacciones", tags=["Transacciones"], 
          summary="Crear nueva transacción",
          description="Crea una nueva transacción bancaria en el sistema. Valida que el ID de la transacción no exista previamente.",
          response_description="Transacción creada exitosamente",
          status_code=201, 
          response_model=TransaccionSimple,
          responses={
              201: {
                  "description": "Transacción creada exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "idTransaccion": 3,
                              "numeroCuentaOrigen": "1234567890",
                              "tipoTransaccion": "Transferencia",
                              "montoTransaccion": 250000.00,
                              "descripcionTransaccion": "Transferencia a cuenta destino"
                          }
                      }
                  }
              },
              400: {
                  "description": "ID de transacción ya existe",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "El ID de la transacción ya existe"
                          }
                      }
                  }
              }
          })
def crear_transaccion(transaccion: TransaccionSimple):
    """
    ## Crear Nueva Transacción
    
    Este endpoint permite crear una nueva transacción bancaria en el sistema.
    
    ### Cuerpo de la petición:
    - **idTransaccion** (int): ID único de la transacción
    - **numeroCuentaOrigen** (str): Número de la cuenta origen
    - **tipoTransaccion** (str): Tipo de transacción (Consignación, Retiro, Transferencia, etc.)
    - **montoTransaccion** (float): Monto de la transacción
    - **descripcionTransaccion** (str): Descripción de la transacción
    
    ### Respuesta:
    - **201**: Transacción creada exitosamente
    - **400**: ID de transacción ya existe
    
    ### Ejemplo de request body:
    ```json
    {
        "idTransaccion": 3,
        "numeroCuentaOrigen": "1234567890",
        "tipoTransaccion": "Transferencia",
        "montoTransaccion": 250000.00,
        "descripcionTransaccion": "Transferencia a cuenta destino"
    }
    ```
    """
    # Validar que no exista el ID
    for t in transacciones_db:
        if t["idTransaccion"] == transaccion.idTransaccion:
            raise HTTPException(status_code=400, detail="El ID de la transacción ya existe")
    
    transaccion_dict = transaccion.model_dump()
    transacciones_db.append(transaccion_dict)
    return transaccion_dict

@app.put("/transacciones/{id_transaccion}", tags=["Transacciones"], 
         summary="Actualizar transacción",
         description="Actualiza la información de una transacción existente basada en su ID único.",
         response_description="Transacción actualizada exitosamente",
         response_model=TransaccionSimple,
         responses={
             200: {
                 "description": "Transacción actualizada exitosamente",
                 "content": {
                     "application/json": {
                         "example": {
                             "idTransaccion": 1,
                             "numeroCuentaOrigen": "1234567890",
                             "tipoTransaccion": "Consignación",
                             "montoTransaccion": 750000.00,
                             "descripcionTransaccion": "Consignación actualizada"
                         }
                     }
                 }
             },
             404: {
                 "description": "Transacción no encontrada",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": "Transacción no encontrada"
                         }
                     }
                 }
             }
         })
def actualizar_transaccion(id_transaccion: int, transaccion: TransaccionSimple):
    """
    ## Actualizar Transacción
    
    Este endpoint permite actualizar la información de una transacción existente.
    
    ### Parámetros de ruta:
    - **id_transaccion** (int): ID de la transacción a actualizar
    
    ### Cuerpo de la petición:
    - **idTransaccion** (int): ID único de la transacción
    - **numeroCuentaOrigen** (str): Número de la cuenta origen
    - **tipoTransaccion** (str): Tipo de transacción (Consignación, Retiro, Transferencia, etc.)
    - **montoTransaccion** (float): Monto de la transacción
    - **descripcionTransaccion** (str): Descripción de la transacción
    
    ### Respuesta:
    - **200**: Transacción actualizada exitosamente
    - **404**: Transacción no encontrada
    
    ### Ejemplo de request body:
    ```json
    {
        "idTransaccion": 1,
        "numeroCuentaOrigen": "1234567890",
        "tipoTransaccion": "Consignación",
        "montoTransaccion": 750000.00,
        "descripcionTransaccion": "Consignación actualizada"
    }
    ```
    """
    for i, t in enumerate(transacciones_db):
        if t["idTransaccion"] == id_transaccion:
            transaccion_dict = transaccion.model_dump()
            transacciones_db[i] = transaccion_dict
            return transaccion_dict
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.delete("/transacciones/{id_transaccion}", tags=["Transacciones"],
           summary="Eliminar transacción",
           description="Elimina una transacción del sistema basada en su ID único.",
           response_description="Transacción eliminada exitosamente",
           responses={
               200: {
                   "description": "Transacción eliminada exitosamente",
                   "content": {
                       "application/json": {
                           "example": {
                               "mensaje": "Transacción 1 eliminada"
                           }
                       }
                   }
               },
               404: {
                   "description": "Transacción no encontrada",
                   "content": {
                       "application/json": {
                           "example": {
                               "detail": "Transacción no encontrada"
                           }
                       }
                   }
               }
           })
def eliminar_transaccion(id_transaccion: int):
    """
    ## Eliminar Transacción
    
    Este endpoint permite eliminar una transacción del sistema.
    
    ### Parámetros de ruta:
    - **id_transaccion** (int): ID de la transacción a eliminar
    
    ### Respuesta:
    - **200**: Transacción eliminada exitosamente
    - **404**: Transacción no encontrada
    
    ### Ejemplo de uso:
    ```
    DELETE /transacciones/1  # Eliminar transacción con ID 1
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Transacción 1 eliminada"
    }
    ```
    """
    for i, t in enumerate(transacciones_db):
        if t["idTransaccion"] == id_transaccion:
            transacciones_db.pop(i)
            return {"mensaje": f"Transacción {id_transaccion} eliminada"}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

# ===== ENDPOINTS ESPECIALES =====
@app.post("/transacciones/consignar", tags=["Transacciones"], 
          summary="Realizar consignación",
          description="Realiza una consignación a una cuenta bancaria específica. Incrementa el saldo de la cuenta destino.",
          response_description="Consignación realizada exitosamente",
          status_code=201,
          responses={
              201: {
                  "description": "Consignación realizada exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "mensaje": "Consignación exitosa",
                              "operacion": {
                                  "numeroCuenta": "1234567890",
                                  "monto": 500000.00,
                                  "descripcion": "Consignación"
                              },
                              "tipo": "consignacion",
                              "saldoAnterior": 1000000.00,
                              "saldoNuevo": 1500000.00
                          }
                      }
                  }
              },
              404: {
                  "description": "Cuenta no encontrada",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Cuenta no encontrada"
                          }
                      }
                  }
              }
          })
def consignar(operacion: OperacionConsignacion):
    """
    ## Realizar Consignación
    
    Este endpoint permite realizar una consignación a una cuenta bancaria específica.
    
    ### Cuerpo de la petición:
    - **numeroCuenta** (str): Número de la cuenta destino
    - **monto** (float): Monto a consignar
    - **descripcion** (str): Descripción de la consignación (opcional)
    
    ### Respuesta:
    - **201**: Consignación realizada exitosamente
    - **404**: Cuenta no encontrada
    
    ### Ejemplo de request body:
    ```json
    {
        "numeroCuenta": "1234567890",
        "monto": 500000.00,
        "descripcion": "Consignación de salario"
    }
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Consignación exitosa",
        "operacion": {
            "numeroCuenta": "1234567890",
            "monto": 500000.00,
            "descripcion": "Consignación"
        },
        "tipo": "consignacion",
        "saldoAnterior": 1000000.00,
        "saldoNuevo": 1500000.00
    }
    ```
    """
    # Buscar la cuenta
    cuenta_encontrada = None
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == operacion.numeroCuenta:
            cuenta_encontrada = cuenta
            break
    
    if not cuenta_encontrada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    saldo_anterior = cuenta_encontrada["saldoActual"]
    saldo_nuevo = saldo_anterior + operacion.monto
    
    return {
        "mensaje": "Consignación exitosa",
        "operacion": operacion.model_dump(),
        "tipo": "consignacion",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo
    }

@app.post("/transacciones/retirar", tags=["Transacciones"], 
          summary="Realizar retiro",
          description="Realiza un retiro de una cuenta bancaria específica. Disminuye el saldo de la cuenta origen.",
          response_description="Retiro realizado exitosamente",
          status_code=201,
          responses={
              201: {
                  "description": "Retiro realizado exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "mensaje": "Retiro exitoso",
                              "operacion": {
                                  "numeroCuenta": "1234567890",
                                  "monto": 100000.00,
                                  "descripcion": "Retiro"
                              },
                              "tipo": "retiro",
                              "saldoAnterior": 1500000.00,
                              "saldoNuevo": 1400000.00
                          }
                      }
                  }
              },
              404: {
                  "description": "Cuenta no encontrada",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Cuenta no encontrada"
                          }
                      }
                  }
              },
              400: {
                  "description": "Saldo insuficiente",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Saldo insuficiente para realizar el retiro"
                          }
                      }
                  }
              }
          })
def retirar(operacion: OperacionRetiro):
    """
    ## Realizar Retiro
    
    Este endpoint permite realizar un retiro de una cuenta bancaria específica.
    
    ### Cuerpo de la petición:
    - **numeroCuenta** (str): Número de la cuenta origen
    - **monto** (float): Monto a retirar
    - **descripcion** (str): Descripción del retiro (opcional)
    
    ### Respuesta:
    - **201**: Retiro realizado exitosamente
    - **404**: Cuenta no encontrada
    - **400**: Saldo insuficiente
    
    ### Ejemplo de request body:
    ```json
    {
        "numeroCuenta": "1234567890",
        "monto": 100000.00,
        "descripcion": "Retiro en cajero"
    }
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Retiro exitoso",
        "operacion": {
            "numeroCuenta": "1234567890",
            "monto": 100000.00,
            "descripcion": "Retiro"
        },
        "tipo": "retiro",
        "saldoAnterior": 1500000.00,
        "saldoNuevo": 1400000.00
    }
    ```
    """
    # Buscar la cuenta
    cuenta_encontrada = None
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == operacion.numeroCuenta:
            cuenta_encontrada = cuenta
            break
    
    if not cuenta_encontrada:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    saldo_anterior = cuenta_encontrada["saldoActual"]
    
    # Validar saldo suficiente
    if saldo_anterior < operacion.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar el retiro")
    
    saldo_nuevo = saldo_anterior - operacion.monto
    
    return {
        "mensaje": "Retiro exitoso",
        "operacion": operacion.model_dump(),
        "tipo": "retiro",
        "saldoAnterior": saldo_anterior,
        "saldoNuevo": saldo_nuevo
    }

@app.post("/transacciones/transferir", tags=["Transacciones"], 
          summary="Realizar transferencia",
          description="Realiza una transferencia entre dos cuentas bancarias. Disminuye el saldo de la cuenta origen e incrementa el de la cuenta destino.",
          response_description="Transferencia realizada exitosamente",
          status_code=201,
          responses={
              201: {
                  "description": "Transferencia realizada exitosamente",
                  "content": {
                      "application/json": {
                          "example": {
                              "mensaje": "Transferencia exitosa",
                              "transferencia": {
                                  "numeroCuentaOrigen": "1234567890",
                                  "numeroCuentaDestino": "0987654321",
                                  "monto": 250000.00,
                                  "descripcion": "Transferencia"
                              },
                              "tipo": "transferencia",
                              "saldoOrigenAnterior": 1500000.00,
                              "saldoOrigenNuevo": 1250000.00,
                              "saldoDestinoAnterior": 500000.00,
                              "saldoDestinoNuevo": 750000.00
                          }
                      }
                  }
              },
              404: {
                  "description": "Cuenta no encontrada",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Cuenta origen o destino no encontrada"
                          }
                      }
                  }
              },
              400: {
                  "description": "Saldo insuficiente o cuentas iguales",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": "Saldo insuficiente para realizar la transferencia"
                          }
                      }
                  }
              }
          })
def transferir(transferencia: OperacionTransferencia):
    """
    ## Realizar Transferencia
    
    Este endpoint permite realizar una transferencia entre dos cuentas bancarias.
    
    ### Cuerpo de la petición:
    - **numeroCuentaOrigen** (str): Número de la cuenta origen
    - **numeroCuentaDestino** (str): Número de la cuenta destino
    - **monto** (float): Monto a transferir
    - **descripcion** (str): Descripción de la transferencia (opcional)
    
    ### Respuesta:
    - **201**: Transferencia realizada exitosamente
    - **404**: Cuenta origen o destino no encontrada
    - **400**: Saldo insuficiente o cuentas iguales
    
    ### Ejemplo de request body:
    ```json
    {
        "numeroCuentaOrigen": "1234567890",
        "numeroCuentaDestino": "0987654321",
        "monto": 250000.00,
        "descripcion": "Transferencia de pago"
    }
    ```
    
    ### Respuesta exitosa:
    ```json
    {
        "mensaje": "Transferencia exitosa",
        "transferencia": {
            "numeroCuentaOrigen": "1234567890",
            "numeroCuentaDestino": "0987654321",
            "monto": 250000.00,
            "descripcion": "Transferencia"
        },
        "tipo": "transferencia",
        "saldoOrigenAnterior": 1500000.00,
        "saldoOrigenNuevo": 1250000.00,
        "saldoDestinoAnterior": 500000.00,
        "saldoDestinoNuevo": 750000.00
    }
    ```
    """
    # Validar que las cuentas no sean iguales
    if transferencia.numeroCuentaOrigen == transferencia.numeroCuentaDestino:
        raise HTTPException(status_code=400, detail="No se puede transferir a la misma cuenta")
    
    # Buscar cuenta origen
    cuenta_origen = None
    cuenta_destino = None
    
    for cuenta in cuentas_db:
        if cuenta["numeroCuenta"] == transferencia.numeroCuentaOrigen:
            cuenta_origen = cuenta
        if cuenta["numeroCuenta"] == transferencia.numeroCuentaDestino:
            cuenta_destino = cuenta
    
    if not cuenta_origen or not cuenta_destino:
        raise HTTPException(status_code=404, detail="Cuenta origen o destino no encontrada")
    
    saldo_origen_anterior = cuenta_origen["saldoActual"]
    saldo_destino_anterior = cuenta_destino["saldoActual"]
    
    # Validar saldo suficiente
    if saldo_origen_anterior < transferencia.monto:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar la transferencia")
    
    saldo_origen_nuevo = saldo_origen_anterior - transferencia.monto
    saldo_destino_nuevo = saldo_destino_anterior + transferencia.monto
    
    return {
        "mensaje": "Transferencia exitosa",
        "transferencia": transferencia.model_dump(),
        "tipo": "transferencia",
        "saldoOrigenAnterior": saldo_origen_anterior,
        "saldoOrigenNuevo": saldo_origen_nuevo,
        "saldoDestinoAnterior": saldo_destino_anterior,
        "saldoDestinoNuevo": saldo_destino_nuevo
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API Bancaria G1 - Versión Simplificada...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
