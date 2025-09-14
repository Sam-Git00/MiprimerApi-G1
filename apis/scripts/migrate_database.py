from database.connection import engine
from sqlalchemy import text
import json
import os
from datetime import datetime

def migrate_database():
    """Migra la base de datos creando tablas e insertando datos de ejemplo"""
    
    try:
        print("Iniciando migración de la base de datos...")
        
        # Scripts SQL para crear las tablas bancarias con auditoría
        create_clientes_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='clientes' AND xtype='U')
        BEGIN
            CREATE TABLE clientes (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                nombre NVARCHAR(100) NOT NULL,
                apellido NVARCHAR(100) NOT NULL,
                email NVARCHAR(150) UNIQUE NOT NULL,
                telefono NVARCHAR(20),
                direccion NVARCHAR(200),
                fecha_nacimiento DATE,
                documento_identidad NVARCHAR(20) UNIQUE NOT NULL,
                tipo_documento NVARCHAR(10) NOT NULL,
                estado NVARCHAR(20) DEFAULT 'activo',
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL
            )
            
            CREATE INDEX IX_clientes_email ON clientes(email)
            CREATE INDEX IX_clientes_documento ON clientes(documento_identidad)
            CREATE INDEX IX_clientes_estado ON clientes(estado)
            
            PRINT 'Tabla clientes creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla clientes ya existe'
        END
        """
        
        create_cuentas_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cuentas' AND xtype='U')
        BEGIN
            CREATE TABLE cuentas (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                numero_cuenta NVARCHAR(20) UNIQUE NOT NULL,
                cliente_id UNIQUEIDENTIFIER NOT NULL,
                tipo_cuenta NVARCHAR(20) NOT NULL,
                saldo DECIMAL(15,2) DEFAULT 0.00,
                estado NVARCHAR(20) DEFAULT 'activa',
                limite_sobregiro DECIMAL(15,2) DEFAULT 0.00,
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
            
            CREATE INDEX IX_cuentas_numero ON cuentas(numero_cuenta)
            CREATE INDEX IX_cuentas_cliente ON cuentas(cliente_id)
            CREATE INDEX IX_cuentas_tipo ON cuentas(tipo_cuenta)
            
            PRINT 'Tabla cuentas creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla cuentas ya existe'
        END
        """
        
        create_transacciones_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='transacciones' AND xtype='U')
        BEGIN
            CREATE TABLE transacciones (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                cuenta_origen_id UNIQUEIDENTIFIER,
                cuenta_destino_id UNIQUEIDENTIFIER,
                tipo_transaccion NVARCHAR(20) NOT NULL,
                monto DECIMAL(15,2) NOT NULL,
                descripcion NVARCHAR(200),
                estado NVARCHAR(20) DEFAULT 'completada',
                referencia NVARCHAR(50),
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL,
                FOREIGN KEY (cuenta_origen_id) REFERENCES cuentas(id),
                FOREIGN KEY (cuenta_destino_id) REFERENCES cuentas(id)
            )
            
            CREATE INDEX IX_transacciones_origen ON transacciones(cuenta_origen_id)
            CREATE INDEX IX_transacciones_destino ON transacciones(cuenta_destino_id)
            CREATE INDEX IX_transacciones_tipo ON transacciones(tipo_transaccion)
            CREATE INDEX IX_transacciones_fecha ON transacciones(fecha_creacion)
            
            PRINT 'Tabla transacciones creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla transacciones ya existe'
        END
        """
        
        create_tarjetas_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tarjetas' AND xtype='U')
        BEGIN
            CREATE TABLE tarjetas (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                numero_tarjeta NVARCHAR(20) UNIQUE NOT NULL,
                cuenta_id UNIQUEIDENTIFIER NOT NULL,
                tipo_tarjeta NVARCHAR(20) NOT NULL,
                limite_credito DECIMAL(15,2) DEFAULT 0.00,
                saldo_disponible DECIMAL(15,2) DEFAULT 0.00,
                fecha_vencimiento DATE NOT NULL,
                estado NVARCHAR(20) DEFAULT 'activa',
                cvv NVARCHAR(4) NOT NULL,
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL,
                FOREIGN KEY (cuenta_id) REFERENCES cuentas(id)
            )
            
            CREATE INDEX IX_tarjetas_numero ON tarjetas(numero_tarjeta)
            CREATE INDEX IX_tarjetas_cuenta ON tarjetas(cuenta_id)
            CREATE INDEX IX_tarjetas_tipo ON tarjetas(tipo_tarjeta)
            
            PRINT 'Tabla tarjetas creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla tarjetas ya existe'
        END
        """
        
        create_prestamos_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='prestamos' AND xtype='U')
        BEGIN
            CREATE TABLE prestamos (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                cliente_id UNIQUEIDENTIFIER NOT NULL,
                monto_solicitado DECIMAL(15,2) NOT NULL,
                monto_aprobado DECIMAL(15,2),
                tasa_interes DECIMAL(5,2) NOT NULL,
                plazo_meses INT NOT NULL,
                cuota_mensual DECIMAL(15,2),
                saldo_pendiente DECIMAL(15,2),
                estado NVARCHAR(20) DEFAULT 'pendiente',
                tipo_prestamo NVARCHAR(30) NOT NULL,
                fecha_aprobacion DATE,
                fecha_vencimiento DATE,
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
            
            CREATE INDEX IX_prestamos_cliente ON prestamos(cliente_id)
            CREATE INDEX IX_prestamos_estado ON prestamos(estado)
            CREATE INDEX IX_prestamos_tipo ON prestamos(tipo_prestamo)
            
            PRINT 'Tabla prestamos creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla prestamos ya existe'
        END
        """
        
        create_inversiones_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='inversiones' AND xtype='U')
        BEGIN
            CREATE TABLE inversiones (
                id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
                cliente_id UNIQUEIDENTIFIER NOT NULL,
                tipo_inversion NVARCHAR(30) NOT NULL,
                monto_inicial DECIMAL(15,2) NOT NULL,
                monto_actual DECIMAL(15,2) NOT NULL,
                tasa_rendimiento DECIMAL(5,2) NOT NULL,
                plazo_dias INT NOT NULL,
                fecha_vencimiento DATE NOT NULL,
                estado NVARCHAR(20) DEFAULT 'activa',
                rendimiento_generado DECIMAL(15,2) DEFAULT 0.00,
                -- Campos de auditoría
                id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
                id_usuario_edicion UNIQUEIDENTIFIER NULL,
                fecha_creacion DATETIME2 DEFAULT GETDATE(),
                fecha_edicion DATETIME2 NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
            
            CREATE INDEX IX_inversiones_cliente ON inversiones(cliente_id)
            CREATE INDEX IX_inversiones_tipo ON inversiones(tipo_inversion)
            CREATE INDEX IX_inversiones_estado ON inversiones(estado)
            
            PRINT 'Tabla inversiones creada exitosamente'
        END
        ELSE
        BEGIN
            PRINT 'Tabla inversiones ya existe'
        END
        """
        
        # Ejecutar scripts usando SQLAlchemy
        with engine.connect() as connection:
            # Crear tablas principales
            connection.execute(text(create_clientes_table))
            connection.execute(text(create_cuentas_table))
            connection.execute(text(create_transacciones_table))
            connection.execute(text(create_tarjetas_table))
            connection.execute(text(create_prestamos_table))
            connection.execute(text(create_inversiones_table))
            
            # Insertar datos de ejemplo desde archivos JSON
            insert_sample_data(connection)
            
            # Commit de los cambios
            connection.commit()
        
        print("Migración completada exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        raise

def insert_sample_data(connection):
    """Inserta datos de ejemplo desde archivos JSON"""
    try:
        # Cargar y insertar clientes
        if os.path.exists("apis/datos/clientes.json"):
            with open("apis/datos/clientes.json", 'r', encoding='utf-8') as f:
                clientes_data = json.load(f)
                
            for cliente in clientes_data:
                insert_cliente = text("""
                IF NOT EXISTS (SELECT * FROM clientes WHERE documento_identidad = :documento)
                BEGIN
                    INSERT INTO clientes (id, nombre, apellido, email, telefono, direccion, 
                                        fecha_nacimiento, documento_identidad, tipo_documento, estado,
                                        id_usuario_creacion, id_usuario_edicion, fecha_creacion, fecha_edicion)
                    VALUES (:id, :nombre, :apellido, :email, :telefono, :direccion,
                           :fecha_nacimiento, :documento_identidad, :tipo_documento, :estado,
                           :id_usuario_creacion, :id_usuario_edicion, :fecha_creacion, :fecha_edicion)
                END
                """)
                
                connection.execute(insert_cliente, cliente)
            
            print(f"Insertados {len(clientes_data)} clientes de ejemplo")
        
        # Similar para otras entidades...
        print("Datos de ejemplo insertados exitosamente")
        
    except Exception as e:
        print(f"Error insertando datos de ejemplo: {e}")
        raise

if __name__ == "__main__":
    migrate_database()
