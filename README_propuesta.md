# API Bancaria - Propuesta de Actualización del README

## Autores
- Samuel Pérez
- Otros colaboradores

## Descripción
API Bancaria es una aplicación que simula operaciones bancarias básicas, permitiendo gestionar clientes, cuentas, transacciones y otros servicios financieros. La API ha evolucionado desde el uso de archivos JSON como base de datos simulada a una implementación con SQLAlchemy y bases de datos relacionales.

## Características Principales
- **Gestión de Clientes**: Crear, consultar, actualizar y eliminar clientes.
- **Gestión de Cuentas**: Administrar cuentas bancarias con diferentes tipos (Ahorros, Corriente).
- **Transacciones**: Realizar consignaciones, retiros y transferencias entre cuentas.
- **Tarjetas**: Administrar tarjetas de débito y crédito asociadas a cuentas.
- **Préstamos**: Gestionar préstamos bancarios con diferentes condiciones.
- **Sucursales**: Administrar información de sucursales bancarias.
- **Empleados**: Gestionar información del personal bancario.
- **Cheques e Inversiones**: Administrar instrumentos financieros adicionales.

## Mejoras Técnicas Implementadas
- **Migración a SQLAlchemy**: Implementación de ORM para gestión de base de datos.
- **Modelos Relacionales**: Estructura de datos normalizada con relaciones entre entidades.
- **Soft Delete**: Implementación de borrado lógico para mantener integridad histórica.
- **Filtros Avanzados**: Búsqueda y filtrado de datos con múltiples criterios.
- **Validación de Datos**: Esquemas Pydantic para validación de entrada/salida.
- **Scripts de Migración**: Herramientas para migrar datos desde JSON a bases de datos SQL.

## Requisitos del Sistema
- Python 3.8 o superior
- FastAPI
- SQLAlchemy
- Base de datos SQL (SQL Server, PostgreSQL, SQLite)
- Uvicorn (servidor ASGI)
- Otras dependencias en requirements.txt

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/api-bancaria.git
cd api-bancaria
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
DB_TYPE=sqlserver  # o postgresql, sqlite
DB_HOST=localhost
DB_PORT=1433  # Puerto por defecto para SQL Server
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=nombre_base_datos
```

### 5. Migrar la base de datos
```bash
python -m apis.scripts.migrate_database
```

### 6. Migrar datos de JSON a la base de datos (opcional)
```bash
python -m apis.scripts.migrate_json_to_db
```

### 7. Iniciar el servidor
```bash
python main.py
```

## Estructura del Proyecto
```
api-bancaria/
├── apis/
│   ├── database/
│   │   ├── connection.py  # Configuración de conexión a la base de datos
│   │   └── __init__.py
│   ├── datos/
│   │   └── *.json  # Archivos JSON (para compatibilidad)
│   ├── endpoints/
│   │   ├── clientes.py
│   │   ├── cuentas.py
│   │   ├── transacciones.py
│   │   └── ...
│   ├── models/
│   │   ├── models.py  # Modelos SQLAlchemy
│   │   ├── schemas.py  # Esquemas Pydantic
│   │   └── __init__.py
│   └── scripts/
│       ├── migrate_database.py  # Script para crear tablas
│       ├── migrate_json_to_db.py  # Script para migrar datos JSON a SQL
│       └── __init__.py
├── main.py  # Punto de entrada de la aplicación
├── requirements.txt
└── README.md
```

## Endpoints Principales

### Clientes
- `GET /clientes`: Listar todos los clientes
- `GET /clientes/{id_cliente}`: Obtener cliente por ID
- `POST /clientes`: Crear nuevo cliente
- `PUT /clientes/{id_cliente}`: Actualizar cliente
- `DELETE /clientes/{id_cliente}`: Eliminar cliente (borrado lógico)

### Cuentas
- `GET /cuentas`: Listar todas las cuentas
- `GET /cuentas/{numero_cuenta}`: Obtener cuenta por número
- `POST /cuentas`: Crear nueva cuenta
- `PUT /cuentas/{numero_cuenta}`: Actualizar cuenta
- `DELETE /cuentas/{numero_cuenta}`: Eliminar cuenta (borrado lógico)

### Transacciones
- `GET /transacciones`: Listar todas las transacciones
- `GET /transacciones/{id_transaccion}`: Obtener transacción por ID
- `POST /transacciones/consignacion`: Realizar consignación
- `POST /transacciones/retiro`: Realizar retiro
- `POST /transacciones/transferencia`: Realizar transferencia

## Documentación API
La documentación interactiva está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Migración desde JSON a Base de Datos
El proyecto incluye scripts para migrar datos desde los archivos JSON a una base de datos SQL:

1. Asegúrate de tener configuradas las variables de entorno para la conexión a la base de datos.
2. Ejecuta el script de migración de base de datos para crear las tablas:
   ```bash
   python -m apis.scripts.migrate_database
   ```
3. Ejecuta el script de migración de datos JSON a la base de datos:
   ```bash
   python -m apis.scripts.migrate_json_to_db
   ```

## Contribución
Si deseas contribuir a este proyecto, por favor:
1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva característica'`)
4. Sube los cambios (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia
Este proyecto está licenciado bajo [especificar licencia].