# API Bancaria G1 - Versión Simplificada sin Arquitectura

# AUTORES
Samuel Oliveros Granada
Julian Morales Saavedra
## Descripción

API REST desarrollada con FastAPI para la gestión integral de un sistema bancario. Proporciona funcionalidades completas para la administración de clientes, cuentas bancarias y transacciones financieras. Utiliza archivos JSON como base de datos simulada para facilitar el desarrollo y pruebas.

## Características Principales

- **Gestión de Clientes**: CRUD completo para clientes bancarios
- **Gestión de Cuentas**: Administración de cuentas de ahorro y corriente
- **Transacciones Bancarias**: Operaciones de consignación, retiro y transferencia
- **Documentación Interactiva**: Swagger UI integrado para pruebas de API
- **Validación de Datos**: Modelos Pydantic para validación automática
- **Manejo de Errores**: Respuestas HTTP apropiadas con mensajes descriptivos

## Requisitos del Sistema

### Software Requerido
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

### Dependencias
Las dependencias se instalan automáticamente con el archivo `requirements.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
```

## Instalación y Configuración

### 1. Clonar el Repositorio / También puedes descargar o clonar el repositorio desde Vscode
```bash
git clone <url-del-repositorio>
cd MiprimerApi-G1
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```
También puedes
```bash
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install pydantic==2.5.0
pip install python-multipart==0.0.6
```

### 3. Ejecutar la Aplicación
```bash
cd apis
python main.py
```
```bash
cd apis
uvicorn main:app --reload
```
```bash
cd apis
uvicorn apis.main:app --host 127.0.0.1 --port 8000 --reload
```
Si no... es válido rezar.
La API estará disponible en: `http://127.0.0.1:8000`

### 4. Acceder a la Documentación
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Estructura del Proyecto

```
MiprimerApi-G1/
├── apis/
│   ├── main.py                 # Archivo principal de la API
│   └── datos/                  # Base de datos JSON simulada
│       ├── clientes.json       # Datos de clientes
│       ├── cuentas.json        # Datos de cuentas
│       └── transacciones.json  # Datos de transacciones
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Endpoints de la API

### Información General

#### GET /
Información general de la API bancaria.

**Respuesta:**
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

#### GET /health
Verificación del estado de salud de la API.

**Respuesta:**
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

### Gestión de Clientes

#### GET /clientes
Obtiene la lista completa de clientes bancarios.

**Parámetros de consulta:**
- `tipo_documento` (opcional): Filtra por tipo de documento (CC, CE, NIT, etc.)

**Ejemplo:**
```bash
GET /clientes
GET /clientes?tipo_documento=CC
```

#### GET /clientes/{id_cliente}
Obtiene un cliente específico por su ID.

**Ejemplo:**
```bash
GET /clientes/1
```

#### POST /clientes
Crea un nuevo cliente bancario.

**Cuerpo de la petición:**
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

#### PUT /clientes/{id_cliente}
Actualiza la información de un cliente existente.

#### DELETE /clientes/{id_cliente}
Elimina un cliente del sistema.

### Gestión de Cuentas

#### GET /cuentas
Obtiene la lista completa de cuentas bancarias.

**Parámetros de consulta:**
- `tipo_cuenta` (opcional): Filtra por tipo de cuenta (Ahorros, Corriente, etc.)

#### GET /cuentas/{numero_cuenta}
Obtiene una cuenta específica por su número.

#### POST /cuentas
Crea una nueva cuenta bancaria.

**Cuerpo de la petición:**
```json
{
    "numeroCuenta": "5555666677",
    "idCliente": 3,
    "tipoCuenta": "Ahorros",
    "saldoActual": 0.00,
    "estadoCuenta": "Activa"
}
```

#### PUT /cuentas/{numero_cuenta}
Actualiza la información de una cuenta existente.

#### DELETE /cuentas/{numero_cuenta}
Elimina una cuenta del sistema.

### Gestión de Transacciones

#### GET /transacciones
Obtiene la lista completa de transacciones bancarias.

**Parámetros de consulta:**
- `tipo_transaccion` (opcional): Filtra por tipo de transacción

#### GET /transacciones/{id_transaccion}
Obtiene una transacción específica por su ID.

#### POST /transacciones
Crea una nueva transacción bancaria.

**Cuerpo de la petición:**
```json
{
    "idTransaccion": 3,
    "numeroCuentaOrigen": "1234567890",
    "tipoTransaccion": "Transferencia",
    "montoTransaccion": 250000.00,
    "descripcionTransaccion": "Transferencia a cuenta destino"
}
```

#### PUT /transacciones/{id_transaccion}
Actualiza la información de una transacción existente.

#### DELETE /transacciones/{id_transaccion}
Elimina una transacción del sistema.

### Operaciones Bancarias Especiales

#### POST /transacciones/consignar
Realiza una consignación a una cuenta bancaria.

**Cuerpo de la petición:**
```json
{
    "numeroCuenta": "1234567890",
    "monto": 500000.00,
    "descripcion": "Consignación de salario"
}
```

**Respuesta:**
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

#### POST /transacciones/retirar
Realiza un retiro de una cuenta bancaria.

**Cuerpo de la petición:**
```json
{
    "numeroCuenta": "1234567890",
    "monto": 100000.00,
    "descripcion": "Retiro en cajero"
}
```

#### POST /transacciones/transferir
Realiza una transferencia entre dos cuentas bancarias.

**Cuerpo de la petición:**
```json
{
    "numeroCuentaOrigen": "1234567890",
    "numeroCuentaDestino": "0987654321",
    "monto": 250000.00,
    "descripcion": "Transferencia de pago"
}
```

## Modelos de Datos

### Cliente
```json
{
    "idCliente": 1,
    "nombreCompleto": "Juan Pérez García",
    "correoElectronico": "juan.perez@email.com",
    "numeroTelefono": "+57 300 123 4567",
    "numeroDocumento": "12345678",
    "tipoDocumento": "CC"
}
```

### Cuenta
```json
{
    "numeroCuenta": "1001234567",
    "idCliente": 1,
    "tipoCuenta": "ahorro",
    "saldoActual": 1500000.0,
    "estadoCuenta": "activa"
}
```

### Transacción
```json
{
    "idTransaccion": 1,
    "numeroCuentaOrigen": "1001234567",
    "tipoTransaccion": "consignacion",
    "montoTransaccion": 500000.0,
    "descripcionTransaccion": "Consignación inicial",
    "estadoTransaccion": "exitosa",
    "fechaTransaccion": "2024-01-15T10:30:00"
}
```

## Códigos de Estado HTTP

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **400**: Error en la solicitud del cliente
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

## Ejemplos de Uso

### Crear un Cliente y su Cuenta

1. **Crear cliente:**
```bash
curl -X POST "http://127.0.0.1:8000/clientes" \
     -H "Content-Type: application/json" \
     -d '{
         "idCliente": 5,
         "nombreCompleto": "Carlos Rodríguez",
         "correoElectronico": "carlos.rodriguez@email.com",
         "numeroTelefono": "3201234567",
         "numeroDocumento": "11223344",
         "tipoDocumento": "CC"
     }'
```

2. **Crear cuenta para el cliente:**
```bash
curl -X POST "http://127.0.0.1:8000/cuentas" \
     -H "Content-Type: application/json" \
     -d '{
         "numeroCuenta": "1001122334",
         "idCliente": 5,
         "tipoCuenta": "Ahorros",
         "saldoActual": 0.00,
         "estadoCuenta": "Activa"
     }'
```

3. **Realizar una consignación:**
```bash
curl -X POST "http://127.0.0.1:8000/transacciones/consignar" \
     -H "Content-Type: application/json" \
     -d '{
         "numeroCuenta": "1001122334",
         "monto": 1000000.00,
         "descripcion": "Consignación inicial"
     }'
```

### Mejoras Futuras
- Implementar base de datos real (PostgreSQL, MySQL)
- Agregar autenticación JWT
- Implementar validaciones más robustas
- Agregar logs y monitoreo
- Implementar tests automatizados
- Implementar arquitectura de capas

