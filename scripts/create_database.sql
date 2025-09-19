-- Script para crear la base de datos del banco en SQL Server

-- Crear la base de datos
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'BancoAPI')
BEGIN
    CREATE DATABASE BancoAPI;
END
GO

USE BancoAPI;
GO

-- Crear tabla de auditoría
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Auditoria')
BEGIN
    CREATE TABLE Auditoria (
        id_auditoria INT IDENTITY(1,1) PRIMARY KEY,
        tabla VARCHAR(100) NOT NULL,
        accion VARCHAR(50) NOT NULL,
        fecha DATETIME NOT NULL DEFAULT GETDATE(),
        usuario VARCHAR(100) NOT NULL,
        datos_anteriores NVARCHAR(MAX) NULL,
        datos_nuevos NVARCHAR(MAX) NULL
    );
END
GO

-- Crear tabla de Clientes
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Clientes')
BEGIN
    CREATE TABLE Clientes (
        idCliente INT PRIMARY KEY,
        tipoDocumento VARCHAR(50) NOT NULL,
        numeroDocumento VARCHAR(50) NOT NULL,
        nombre VARCHAR(100) NOT NULL,
        apellido VARCHAR(100) NOT NULL,
        correo VARCHAR(100) NULL,
        celular VARCHAR(20) NULL,
        activo BIT NOT NULL DEFAULT 1,
        fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_edicion DATETIME NOT NULL DEFAULT GETDATE(),
        id_usuario_creacion INT NOT NULL,
        id_usuario_edicion INT NOT NULL,
        CONSTRAINT UQ_Cliente_Documento UNIQUE (tipoDocumento, numeroDocumento)
    );
END
GO

-- Crear tabla de Cuentas
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Cuentas')
BEGIN
    CREATE TABLE Cuentas (
        numeroCuenta VARCHAR(20) PRIMARY KEY,
        idCliente INT NOT NULL,
        tipoCuenta VARCHAR(50) NOT NULL,
        saldoActual DECIMAL(18, 2) NOT NULL DEFAULT 0,
        activo BIT NOT NULL DEFAULT 1,
        fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_edicion DATETIME NOT NULL DEFAULT GETDATE(),
        id_usuario_creacion INT NOT NULL,
        id_usuario_edicion INT NOT NULL,
        CONSTRAINT FK_Cuenta_Cliente FOREIGN KEY (idCliente) REFERENCES Clientes(idCliente)
    );
END
GO

-- Crear tabla de Transacciones
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Transacciones')
BEGIN
    CREATE TABLE Transacciones (
        idTransaccion INT PRIMARY KEY,
        numeroCuentaOrigen VARCHAR(20) NOT NULL,
        numeroCuentaDestino VARCHAR(20) NULL,
        tipoTransaccion VARCHAR(50) NOT NULL,
        montoTransaccion DECIMAL(18, 2) NOT NULL,
        descripcionTransaccion VARCHAR(255) NULL,
        activo BIT NOT NULL DEFAULT 1,
        fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_edicion DATETIME NOT NULL DEFAULT GETDATE(),
        id_usuario_creacion INT NOT NULL,
        id_usuario_edicion INT NOT NULL,
        CONSTRAINT FK_Transaccion_CuentaOrigen FOREIGN KEY (numeroCuentaOrigen) REFERENCES Cuentas(numeroCuenta)
    );
END
GO

-- Crear índices para mejorar el rendimiento
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Clientes_TipoNumeroDocumento')
BEGIN
    CREATE INDEX IX_Clientes_TipoNumeroDocumento ON Clientes(tipoDocumento, numeroDocumento);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Cuentas_IdCliente')
BEGIN
    CREATE INDEX IX_Cuentas_IdCliente ON Cuentas(idCliente);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Transacciones_NumeroCuentaOrigen')
BEGIN
    CREATE INDEX IX_Transacciones_NumeroCuentaOrigen ON Transacciones(numeroCuentaOrigen);
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Transacciones_TipoTransaccion')
BEGIN
    CREATE INDEX IX_Transacciones_TipoTransaccion ON Transacciones(tipoTransaccion);
END
GO

-- Crear triggers para auditoría

-- Trigger para auditar cambios en Clientes
IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_Clientes_Auditoria')
    DROP TRIGGER TR_Clientes_Auditoria;
GO

CREATE TRIGGER TR_Clientes_Auditoria
ON Clientes
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    DECLARE @accion VARCHAR(50);
    
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
        SET @accion = 'UPDATE';
    ELSE IF EXISTS (SELECT * FROM inserted)
        SET @accion = 'INSERT';
    ELSE
        SET @accion = 'DELETE';
    
    INSERT INTO Auditoria (tabla, accion, fecha, usuario, datos_anteriores, datos_nuevos)
    SELECT 
        'Clientes', 
        @accion, 
        GETDATE(), 
        SYSTEM_USER,
        CASE 
            WHEN @accion IN ('UPDATE', 'DELETE') THEN 
                (SELECT * FROM deleted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END,
        CASE 
            WHEN @accion IN ('INSERT', 'UPDATE') THEN 
                (SELECT * FROM inserted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END;
END;
GO

-- Trigger para auditar cambios en Cuentas
IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_Cuentas_Auditoria')
    DROP TRIGGER TR_Cuentas_Auditoria;
GO

CREATE TRIGGER TR_Cuentas_Auditoria
ON Cuentas
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    DECLARE @accion VARCHAR(50);
    
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
        SET @accion = 'UPDATE';
    ELSE IF EXISTS (SELECT * FROM inserted)
        SET @accion = 'INSERT';
    ELSE
        SET @accion = 'DELETE';
    
    INSERT INTO Auditoria (tabla, accion, fecha, usuario, datos_anteriores, datos_nuevos)
    SELECT 
        'Cuentas', 
        @accion, 
        GETDATE(), 
        SYSTEM_USER,
        CASE 
            WHEN @accion IN ('UPDATE', 'DELETE') THEN 
                (SELECT * FROM deleted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END,
        CASE 
            WHEN @accion IN ('INSERT', 'UPDATE') THEN 
                (SELECT * FROM inserted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END;
END;
GO

-- Trigger para auditar cambios en Transacciones
IF EXISTS (SELECT * FROM sys.triggers WHERE name = 'TR_Transacciones_Auditoria')
    DROP TRIGGER TR_Transacciones_Auditoria;
GO

CREATE TRIGGER TR_Transacciones_Auditoria
ON Transacciones
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    DECLARE @accion VARCHAR(50);
    
    IF EXISTS (SELECT * FROM inserted) AND EXISTS (SELECT * FROM deleted)
        SET @accion = 'UPDATE';
    ELSE IF EXISTS (SELECT * FROM inserted)
        SET @accion = 'INSERT';
    ELSE
        SET @accion = 'DELETE';
    
    INSERT INTO Auditoria (tabla, accion, fecha, usuario, datos_anteriores, datos_nuevos)
    SELECT 
        'Transacciones', 
        @accion, 
        GETDATE(), 
        SYSTEM_USER,
        CASE 
            WHEN @accion IN ('UPDATE', 'DELETE') THEN 
                (SELECT * FROM deleted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END,
        CASE 
            WHEN @accion IN ('INSERT', 'UPDATE') THEN 
                (SELECT * FROM inserted FOR JSON PATH, WITHOUT_ARRAY_WRAPPER)
            ELSE NULL
        END;
END;
GO

PRINT 'Base de datos BancoAPI creada exitosamente con todas sus tablas, índices y triggers.';
GO