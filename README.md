# API Bancaria G1 - Versión con SQLAlchemy

# Autores
Samuel Oliveros Granada
Julian Morales Saavedra

## Descripción

API REST desarrollada con FastAPI para la gestión integral de un sistema bancario. Proporciona funcionalidades completas para la administración de clientes, cuentas bancarias y transacciones financieras. Inicialmente utilizaba archivos JSON como base de datos simulada, pero ahora ha evolucionado a una implementación con SQLAlchemy y bases de datos relacionales para un manejo más robusto y escalable de los datos.

## Características Principales
 
- **Gestión de Clientes**: CRUD completo para clientes bancarios
- **Gestión de Cuentas**: Administración de cuentas de ahorro y corriente
- **Transacciones Bancarias**: Operaciones de consignación, retiro y transferencia
- **Documentación Interactiva**: Swagger UI integrado para pruebas de API
- **Validación de Datos**: Modelos Pydantic para validación automática
- **Manejo de Errores**: Respuestas HTTP apropiadas con mensajes descriptivos
- **SQLAlchemy ORM**: Implementación de mapeo objeto-relacional para gestión de base de datos
- **Modelos Relacionales**: Estructura de datos normalizada con relaciones entre entidades
- **Soft Delete**: Implementación de borrado lógico para mantener integridad histórica
- **Filtros Avanzados**: Búsqueda y filtrado de datos con múltiples criterios
- **Scripts de Migración**: Herramientas para migrar datos desde JSON a bases de datos SQL
 
  ## Postman
 pruebas hechas en postman para mostrar la funcionalidad
[PANTALLAZOS DE POSTMAN](https://drive.google.com/drive/folders/1UrkmbECGcl_08ozzAXWk8exO4xzylLCj?usp=drive_link)
## Requisitos del Sistema

### Software Requerido
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Base de datos SQL** (SQL Server, PostgreSQL, SQLite)

### Dependencias
Las dependencias se instalan automáticamente con el archivo `requirements.txt`:

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
sqlalchemy==2.0.23
python-dotenv==1.0.0
```

## Instalación y Configuración

### 1. Clonar el Repositorio / También puedes descargar o clonar el repositorio desde Vscode
```bash
git clone <url-del-repositorio>
cd MiprimerApi-G1
```

### 2. Instalar Dependencias
```bash
py -m pip install -r requirements.txt
```
También puedes
```bash
pip install fastapi==0.104.1
pip install "uvicorn[standard]==0.24.0"
pip install pydantic==2.5.0
pip install python-multipart==0.0.6
pip install sqlalchemy==2.0.23
pip install python-dotenv==1.0.0
```

### 3. Configurar variables de entorno
Crea un archivo `.env` en la carpeta `apis` con las siguientes variables:
```
DB_TYPE=sqlserver  # o postgresql, sqlite
DB_HOST=localhost
DB_PORT=1433  # Puerto por defecto para SQL Server
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=nombre_base_datos
```

### 4. Migrar la base de datos
```bash
python -m apis.scripts.migrate_database
```

### 5. Migrar datos de JSON a la base de datos (opcional)
```bash
python -m apis.scripts.migrate_json_to_db
```

### 6. Ejecutar la Aplicación
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

### 7. Acceder a la Documentación
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Estructura del Proyecto

```
MiprimerApi-G1/
├── apis/
│   ├── main.py                 # Archivo principal de la API
│   ├── .env                    # Variables de entorno para la conexión a la BD
│   ├── database/               # Configuración de la base de datos
│   │   ├── __init__.py
│   │   └── connection.py       # Configuración de conexión a la base de datos
│   ├── datos/                  # Base de datos JSON simulada (para compatibilidad)
│   │   ├── clientes.json       # Datos de clientes
│   │   ├── cuentas.json        # Datos de cuentas
│   │   └── transacciones.json  # Datos de transacciones
│   ├── endpoints/              # Controladores de la API
│   │   ├── clientes.py
│   │   ├── cuentas.py
│   │   ├── transacciones.py
│   │   └── ...
│   ├── models/                 # Modelos y esquemas
│   │   ├── models.py           # Modelos SQLAlchemy
│   │   └── schemas.py          # Esquemas Pydantic
│   └── scripts/                # Scripts de utilidad
│       ├── migrate_database.py # Script para crear tablas
│       └── migrate_json_to_db.py # Script para migrar datos JSON a SQL
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
    "message": "API Bancaria G1 - Versión con SQLAlchemy",
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
Elimina un cliente del sistema (borrado lógico con SQLAlchemy).

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
Elimina una cuenta del sistema (borrado lógico con SQLAlchemy).

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
Elimina una transacción del sistema (borrado lógico con SQLAlchemy).

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

## Migración desde JSON a Base de Datos
El proyecto incluye scripts para migrar datos desde los archivos JSON a una base de datos SQL:

1. Asegúrate de tener configuradas las variables de entorno para la conexión a la base de datos en el archivo `.env`.
2. Ejecuta el script de migración de base de datos para crear las tablas:
   ```bash
   python -m apis.scripts.migrate_database
   ```
3. Ejecuta el script de migración de datos JSON a la base de datos:
   ```bash
   python -m apis.scripts.migrate_json_to_db
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

### Mejoras Implementadas
- Migración de base de datos JSON a SQL con SQLAlchemy
- Implementación de modelos relacionales
- Borrado lógico (soft delete) para mantener integridad histórica
- Filtros avanzados para búsqueda de datos
- Scripts de migración para facilitar la transición

### Mejoras Futuras
- Implementar autenticación JWT
-Implementar CORS
- Implementar validaciones más robustas
- Agregar logs y monitoreo
- Implementar tests automatizados
- Implementar arquitectura de capas completa










Se realizaron los siguientes cambios :

1.  **Refactorización de Modelos SQLAlchemy (`apis/models/models.py`):**
    *   **Creación del modelo `Usuario`:** Se añadió un nuevo modelo `Usuario` para gestionar la autenticación y los campos de auditoría, como `id_usuario_creacion` y `id_usuario_edicion`, que son esenciales para el seguimiento de cambios.
    *   **Actualización de modelos existentes (`Cliente`, `Cuenta`, `Transaccion`):**
        *   Se corrigieron los tipos de datos para alinearlos con el esquema de SQL Server (ej. `String(150)` para correos, `Numeric(15,2)` para saldos/montos, `UNIQUEIDENTIFIER` para IDs de usuario).
        *   Se añadió el campo `id_transaccion` al modelo `Transaccion` para que coincida con el esquema SQL.
        *   Se establecieron relaciones de clave foránea (`ForeignKey`) hacia el nuevo modelo `Usuario` para los campos de auditoría en todos los modelos relevantes.
        *   Se ajustaron y añadieron relaciones (`relationship`) para asegurar la correcta conexión entre las entidades del ORM.
    *   **Creación de modelos faltantes (`Tarjeta`, `Prestamo`, `Sucursal`, `Empleado`, `Cheque`, `Inversion`):** Se crearon los modelos SQLAlchemy correspondientes a todas las tablas restantes en la base de datos, asegurando que sus campos, tipos de datos y relaciones reflejen fielmente el esquema de `create_database.sql`.

2.  **Consolidación de la Lógica de Conexión a la Base de Datos (`apis/database/connection.py`):**
    *   Se añadió la función `get_engine()` para exportar el motor de SQLAlchemy, permitiendo que otros scripts lo utilicen de manera consistente.

3.  **Refactorización y Consolidación de Scripts de Migración (`apis/scripts/migrate_json_to_db.py`):**
    *   **Inclusión del usuario administrador:** Se añadió lógica para insertar un usuario administrador por defecto al inicio del proceso de migración, lo que es necesario para los campos de auditoría.
    *   **Uso consistente del ORM de SQLAlchemy:** Se modificaron todas las funciones de migración (`migrate_clientes`, `migrate_cuentas`, `migrate_transacciones`, `migrate_tarjetas`, `migrate_prestamos`, `migrate_sucursales`, `migrate_empleados`, `migrate_cheques`, `migrate_inversiones`) para que utilicen exclusivamente el ORM de SQLAlchemy para la verificación de existencia y la inserción de datos. Esto elimina la dependencia de sentencias SQL crudas, haciendo el código más robusto y fácil de mantener.
    *   **Consolidación de limpieza de archivos JSON:** Se unificaron las funciones de eliminación de archivos JSON, manteniendo una sola función (`delete_json_files`) y actualizando `ejecutar_migracion` para usarla, simplificando el proceso post-migración.
