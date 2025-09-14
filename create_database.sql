-- Script para crear la base de datos bancaria

-- Crear la base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'BancoAPI')
BEGIN
    CREATE DATABASE BancoAPI;
    PRINT 'Base de datos BancoAPI creada exitosamente';
END
ELSE
BEGIN
    PRINT 'La base de datos BancoAPI ya existe';
END
GO

-- Usar la base de datos
USE BancoAPI;
GO

-- Tabla de Usuarios (para auditoría)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='usuarios' AND xtype='U')
BEGIN
    CREATE TABLE usuarios (
        id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        nombre_usuario NVARCHAR(100) NOT NULL,
        correo_electronico NVARCHAR(150) UNIQUE NOT NULL,
        contrasena NVARCHAR(255) NOT NULL,
        rol NVARCHAR(50) NOT NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_ultimo_acceso DATETIME2 NULL,
        activo BIT DEFAULT 1
    );
    
    PRINT 'Tabla usuarios creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla usuarios ya existe';
END
GO

-- Tabla de Clientes
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='clientes' AND xtype='U')
BEGIN
    CREATE TABLE clientes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_cliente INT UNIQUE NOT NULL,
        nombre_completo NVARCHAR(100) NOT NULL,
        correo_electronico NVARCHAR(150) UNIQUE NOT NULL,
        numero_telefono NVARCHAR(20) NOT NULL,
        numero_documento NVARCHAR(20) UNIQUE NOT NULL,
        tipo_documento NVARCHAR(10) NOT NULL,
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_clientes_id_cliente ON clientes(id_cliente);
    CREATE INDEX IX_clientes_documento ON clientes(numero_documento);
    
    PRINT 'Tabla clientes creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla clientes ya existe';
END
GO

-- Tabla de Cuentas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cuentas' AND xtype='U')
BEGIN
    CREATE TABLE cuentas (
        id INT IDENTITY(1,1) PRIMARY KEY,
        numero_cuenta NVARCHAR(20) UNIQUE NOT NULL,
        id_cliente INT NOT NULL,
        tipo_cuenta NVARCHAR(20) NOT NULL,
        saldo_actual DECIMAL(15,2) DEFAULT 0.00,
        estado_cuenta NVARCHAR(20) DEFAULT 'activa',
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_cuentas_numero ON cuentas(numero_cuenta);
    CREATE INDEX IX_cuentas_cliente ON cuentas(id_cliente);
    
    PRINT 'Tabla cuentas creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla cuentas ya existe';
END
GO

-- Tabla de Transacciones
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='transacciones' AND xtype='U')
BEGIN
    CREATE TABLE transacciones (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_transaccion INT UNIQUE NOT NULL,
        numero_cuenta_origen NVARCHAR(20) NOT NULL,
        numero_cuenta_destino NVARCHAR(20) NULL,
        tipo_transaccion NVARCHAR(20) NOT NULL,
        monto_transaccion DECIMAL(15,2) NOT NULL,
        descripcion_transaccion NVARCHAR(200),
        estado_transaccion NVARCHAR(20) DEFAULT 'exitosa',
        fecha_transaccion DATETIME2 DEFAULT GETDATE(),
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (numero_cuenta_origen) REFERENCES cuentas(numero_cuenta),
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_transacciones_id ON transacciones(id_transaccion);
    CREATE INDEX IX_transacciones_cuenta_origen ON transacciones(numero_cuenta_origen);
    CREATE INDEX IX_transacciones_cuenta_destino ON transacciones(numero_cuenta_destino);
    
    PRINT 'Tabla transacciones creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla transacciones ya existe';
END
GO

-- Tabla de Tarjetas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tarjetas' AND xtype='U')
BEGIN
    CREATE TABLE tarjetas (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_tarjeta INT UNIQUE NOT NULL,
        numero_tarjeta NVARCHAR(20) UNIQUE NOT NULL,
        tipo_tarjeta NVARCHAR(20) NOT NULL,
        id_cuenta INT NOT NULL,
        id_cliente INT NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        cvv NVARCHAR(5) NOT NULL,
        estado_tarjeta NVARCHAR(20) DEFAULT 'activa',
        limite_credito DECIMAL(15,2) NULL,
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_cuenta) REFERENCES cuentas(id),
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_tarjetas_id ON tarjetas(id_tarjeta);
    CREATE INDEX IX_tarjetas_numero ON tarjetas(numero_tarjeta);
    
    PRINT 'Tabla tarjetas creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla tarjetas ya existe';
END
GO

-- Tabla de Préstamos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='prestamos' AND xtype='U')
BEGIN
    CREATE TABLE prestamos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_prestamo INT UNIQUE NOT NULL,
        id_cliente INT NOT NULL,
        numero_prestamo NVARCHAR(20) UNIQUE NOT NULL,
        monto_prestado DECIMAL(15,2) NOT NULL,
        tasa_interes DECIMAL(5,2) NOT NULL,
        plazo_meses INT NOT NULL,
        fecha_desembolso DATE NOT NULL,
        saldo_pendiente DECIMAL(15,2) NOT NULL,
        estado_prestamo NVARCHAR(20) DEFAULT 'aprobado',
        id_cuenta INT NOT NULL,
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_cuenta) REFERENCES cuentas(id),
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_prestamos_id ON prestamos(id_prestamo);
    CREATE INDEX IX_prestamos_cliente ON prestamos(id_cliente);
    
    PRINT 'Tabla prestamos creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla prestamos ya existe';
END
GO

-- Tabla de Sucursales
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sucursales' AND xtype='U')
BEGIN
    CREATE TABLE sucursales (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_sucursal INT UNIQUE NOT NULL,
        nombre_sucursal NVARCHAR(100) NOT NULL,
        direccion NVARCHAR(200) NOT NULL,
        ciudad NVARCHAR(50) NOT NULL,
        codigo_postal NVARCHAR(10) NOT NULL,
        telefono NVARCHAR(20) NOT NULL,
        gerente_id INT NULL,
        estado_sucursal NVARCHAR(20) DEFAULT 'abierta',
        activo BIT DEFAULT 1
    );
    
    CREATE INDEX IX_sucursales_id ON sucursales(id_sucursal);
    
    PRINT 'Tabla sucursales creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla sucursales ya existe';
END
GO

-- Tabla de Empleados
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='empleados' AND xtype='U')
BEGIN
    CREATE TABLE empleados (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_empleado INT UNIQUE NOT NULL,
        nombre_completo NVARCHAR(100) NOT NULL,
        cargo NVARCHAR(50) NOT NULL,
        id_sucursal INT NOT NULL,
        numero_documento NVARCHAR(20) UNIQUE NOT NULL,
        tipo_documento NVARCHAR(10) NOT NULL,
        correo_electronico NVARCHAR(150) UNIQUE NOT NULL,
        telefono NVARCHAR(20) NOT NULL,
        estado_empleado NVARCHAR(20) DEFAULT 'activo',
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_sucursal) REFERENCES sucursales(id_sucursal)
    );
    
    CREATE INDEX IX_empleados_id ON empleados(id_empleado);
    
    -- Actualizar la referencia de gerente en sucursales
    ALTER TABLE sucursales
    ADD CONSTRAINT FK_sucursales_gerente
    FOREIGN KEY (gerente_id) REFERENCES empleados(id_empleado);
    
    PRINT 'Tabla empleados creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla empleados ya existe';
END
GO

-- Tabla de Cheques
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='cheques' AND xtype='U')
BEGIN
    CREATE TABLE cheques (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_cheque INT UNIQUE NOT NULL,
        numero_cheque NVARCHAR(20) UNIQUE NOT NULL,
        id_cuenta INT NOT NULL,
        monto DECIMAL(15,2) NOT NULL,
        beneficiario NVARCHAR(100) NOT NULL,
        fecha_emision DATE NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        estado_cheque NVARCHAR(20) DEFAULT 'emitido',
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_cuenta) REFERENCES cuentas(id)
    );
    
    CREATE INDEX IX_cheques_id ON cheques(id_cheque);
    CREATE INDEX IX_cheques_numero ON cheques(numero_cheque);
    
    PRINT 'Tabla cheques creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla cheques ya existe';
END
GO

-- Tabla de Inversiones
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='inversiones' AND xtype='U')
BEGIN
    CREATE TABLE inversiones (
        id INT IDENTITY(1,1) PRIMARY KEY,
        id_inversion INT UNIQUE NOT NULL,
        id_cliente INT NOT NULL,
        tipo_inversion NVARCHAR(50) NOT NULL,
        monto_invertido DECIMAL(15,2) NOT NULL,
        fecha_inicio DATE NOT NULL,
        plazo INT NOT NULL,
        rendimiento_esperado DECIMAL(5,2) NOT NULL,
        estado_inversion NVARCHAR(20) DEFAULT 'activa',
        id_cuenta INT NOT NULL,
        -- Campos de auditoría
        id_usuario_creacion UNIQUEIDENTIFIER NOT NULL,
        id_usuario_edicion UNIQUEIDENTIFIER NULL,
        fecha_creacion DATETIME2 DEFAULT GETDATE(),
        fecha_edicion DATETIME2 NULL,
        activo BIT DEFAULT 1,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY (id_cuenta) REFERENCES cuentas(id),
        FOREIGN KEY (id_usuario_creacion) REFERENCES usuarios(id),
        FOREIGN KEY (id_usuario_edicion) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IX_inversiones_id ON inversiones(id_inversion);
    CREATE INDEX IX_inversiones_cliente ON inversiones(id_cliente);
    
    PRINT 'Tabla inversiones creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla inversiones ya existe';
END
GO

-- Insertar usuario administrador para auditoría
IF NOT EXISTS (SELECT * FROM usuarios WHERE correo_electronico = 'admin@bancoapi.com')
BEGIN
    INSERT INTO usuarios (id, nombre_usuario, correo_electronico, contrasena, rol)
    VALUES 
    ('550e8400-e29b-41d4-a716-446655440001', 'admin', 'admin@bancoapi.com', 'hashed_password_here', 'administrador');
    
    PRINT 'Usuario administrador creado exitosamente';
END
ELSE
BEGIN
    PRINT 'Usuario administrador ya existe';
END
GO