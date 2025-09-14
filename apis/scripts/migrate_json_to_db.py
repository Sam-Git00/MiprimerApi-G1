import json
import os
import sys
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dotenv import load_dotenv

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apis.models.models import Base, Cliente, Cuenta, Transaccion
from apis.database.connection import get_engine, get_db, SessionLocal

load_dotenv()

# Obtener el motor de SQLAlchemy
engine = get_engine()


def migrate_json_to_db():
    """Migra los datos de los archivos JSON a la base de datos SQL Server"""
    try:
        print("Iniciando migración de datos JSON a la base de datos...")
        
        # Verificar conexión a la base de datos
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión a la base de datos exitosa")
        
        # Migrar datos de clientes
        migrate_clientes()
        
        # Migrar datos de cuentas
        migrate_cuentas()
        
        # Migrar datos de transacciones
        migrate_transacciones()
        
        # Migrar datos de tarjetas
        migrate_tarjetas()
        
        # Migrar datos de préstamos
        migrate_prestamos()
        
        # Migrar datos de sucursales
        migrate_sucursales()
        
        # Migrar datos de empleados
        migrate_empleados()
        
        # Migrar datos de cheques
        migrate_cheques()
        
        # Migrar datos de inversiones
        migrate_inversiones()
        
        print("Migración de datos completada exitosamente")
        return True
    except Exception as e:
        print(f"Error en la migración de datos: {e}")
        return False


def migrate_clientes():
    """Migra los datos de clientes desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/clientes.json.json"):
            with open("apis/datos/clientes.json.json", 'r', encoding='utf-8') as f:
                clientes = json.load(f)
            
            with SessionLocal() as session:
                for cliente_data in clientes:
                    # Verificar si el cliente ya existe
                    cliente_existente = session.query(Cliente).filter(Cliente.idCliente == cliente_data["idCliente"]).first()
                    
                    if not cliente_existente:
                        # Extraer nombre y apellido del nombreCompleto
                        nombre_completo = cliente_data.get('nombreCompleto', '')
                        partes_nombre = nombre_completo.split(' ', 1)
                        nombre = partes_nombre[0] if partes_nombre else ''
                        apellido = partes_nombre[1] if len(partes_nombre) > 1 else ''
                        
                        # Crear nuevo cliente
                        nuevo_cliente = Cliente(
                            idCliente=cliente_data['idCliente'],
                            tipoDocumento=cliente_data['tipoDocumento'],
                            numeroDocumento=cliente_data['numeroDocumento'],
                            nombre=nombre,
                            apellido=apellido,
                            correo=cliente_data.get('correoElectronico', None),
                            celular=cliente_data.get('numeroTelefono', None),
                            activo=True,
                            fecha_creacion=datetime.now(),
                            fecha_edicion=datetime.now(),
                            id_usuario_creacion=1,  # Usuario por defecto
                            id_usuario_edicion=1    # Usuario por defecto
                        )
                        
                        session.add(nuevo_cliente)
                session.commit()
            print(f"Migrados {len(clientes)} clientes")
    except Exception as e:
        print(f"Error migrando clientes: {e}")
        raise


def migrate_cuentas():
    """Migra los datos de cuentas desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/cuentas.json.json"):
            with open("apis/datos/cuentas.json.json", 'r', encoding='utf-8') as f:
                cuentas = json.load(f)
            
            with SessionLocal() as session:
                for cuenta_data in cuentas:
                    # Verificar si la cuenta ya existe
                    cuenta_existente = session.query(Cuenta).filter(Cuenta.numeroCuenta == cuenta_data["numeroCuenta"]).first()
                    
                    if not cuenta_existente:
                        # Verificar si el cliente existe
                        cliente = session.query(Cliente).filter(Cliente.idCliente == cuenta_data["idCliente"]).first()
                        
                        if cliente:
                            # Crear nueva cuenta
                            nueva_cuenta = Cuenta(
                                numeroCuenta=cuenta_data['numeroCuenta'],
                                idCliente=cuenta_data['idCliente'],
                                tipoCuenta=cuenta_data['tipoCuenta'],
                                saldoActual=cuenta_data['saldoActual'],
                                activo=cuenta_data.get('estadoCuenta', 'activa') == 'activa',
                                fecha_creacion=datetime.now(),
                                fecha_edicion=datetime.now(),
                                id_usuario_creacion=1,  # Usuario por defecto
                                id_usuario_edicion=1    # Usuario por defecto
                            )
                            
                            session.add(nueva_cuenta)
                session.commit()
            print(f"Migradas {len(cuentas)} cuentas")
    except Exception as e:
        print(f"Error migrando cuentas: {e}")
        raise


def migrate_transacciones():
    """Migra los datos de transacciones desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/transacciones.json"):
            with open("apis/datos/transacciones.json", 'r', encoding='utf-8') as f:
                transacciones = json.load(f)
            
            with SessionLocal() as session:
                for transaccion_data in transacciones:
                    # Verificar si la transacción ya existe
                    transaccion_existente = session.query(Transaccion).filter(Transaccion.idTransaccion == transaccion_data["idTransaccion"]).first()
                    
                    if not transaccion_existente:
                        # Verificar si la cuenta origen existe
                        cuenta_origen = session.query(Cuenta).filter(Cuenta.numeroCuenta == transaccion_data["numeroCuentaOrigen"]).first()
                        
                        if cuenta_origen:
                            # Verificar si la cuenta destino existe (para transferencias)
                            cuenta_destino = None
                            if transaccion_data.get("numeroCuentaDestino"):
                                cuenta_destino = session.query(Cuenta).filter(Cuenta.numeroCuenta == transaccion_data["numeroCuentaDestino"]).first()
                            
                            # Crear nueva transacción
                            nueva_transaccion = Transaccion(
                                idTransaccion=transaccion_data['idTransaccion'],
                                tipoTransaccion=transaccion_data['tipoTransaccion'],
                                numeroCuentaOrigen=transaccion_data['numeroCuentaOrigen'],
                                numeroCuentaDestino=transaccion_data.get('numeroCuentaDestino'),
                                monto=transaccion_data['montoTransaccion'],
                                descripcion=transaccion_data.get('descripcionTransaccion', ''),
                                activo=True,
                                fecha_creacion=datetime.now(),
                                fecha_edicion=datetime.now(),
                                id_usuario_creacion=1,  # Usuario por defecto
                                id_usuario_edicion=1    # Usuario por defecto
                            )
                            
                            session.add(nueva_transaccion)
                session.commit()
            print(f"Migradas {len(transacciones)} transacciones")
    except Exception as e:
        print(f"Error migrando transacciones: {e}")
        raise


def migrate_tarjetas():
    """Migra los datos de tarjetas desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/tarjetas.json"):
            with open("apis/datos/tarjetas.json", 'r', encoding='utf-8') as f:
                tarjetas = json.load(f)
            
            with SessionLocal() as session:
                for tarjeta in tarjetas:
                    # Verificar si la tarjeta ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM tarjetas WHERE id_tarjeta = :id_tarjeta"),
                        {"id_tarjeta": tarjeta["idTarjeta"]}
                    ).scalar()
                    
                    if result == 0:
                        # Obtener el ID interno de la cuenta
                        cuenta_id = session.execute(
                            text("SELECT id FROM cuentas WHERE id = :id_cuenta"),
                            {"id_cuenta": tarjeta["idCuenta"]}
                        ).scalar()
                        
                        if cuenta_id:
                            # Insertar tarjeta
                            session.execute(
                                text("""
                                INSERT INTO tarjetas 
                                (id_tarjeta, numero_tarjeta, tipo_tarjeta, id_cuenta, id_cliente, 
                                fecha_vencimiento, cvv, estado_tarjeta, limite_credito, 
                                id_usuario_creacion, id_usuario_edicion, fecha_creacion, fecha_edicion, activo)
                                VALUES 
                                (:id_tarjeta, :numero_tarjeta, :tipo_tarjeta, :id_cuenta, :id_cliente, 
                                :fecha_vencimiento, :cvv, :estado_tarjeta, :limite_credito, 
                                :id_usuario_creacion, :id_usuario_edicion, :fecha_creacion, :fecha_edicion, :activo)
                                """),
                                {
                                    "id_tarjeta": tarjeta["idTarjeta"],
                                    "numero_tarjeta": tarjeta["numeroTarjeta"],
                                    "tipo_tarjeta": tarjeta["tipoTarjeta"],
                                    "id_cuenta": tarjeta["idCuenta"],
                                    "id_cliente": tarjeta["idCliente"],
                                    "fecha_vencimiento": tarjeta["fechaVencimiento"],
                                    "cvv": tarjeta["cvv"],
                                    "estado_tarjeta": tarjeta["estadoTarjeta"],
                                    "limite_credito": tarjeta.get("limiteCredito"),
                                    "id_usuario_creacion": tarjeta["id_usuario_creacion"],
                                    "id_usuario_edicion": tarjeta.get("id_usuario_edicion"),
                                    "fecha_creacion": tarjeta["fecha_creacion"],
                                    "fecha_edicion": tarjeta.get("fecha_edicion"),
                                    "activo": tarjeta.get("activo", True)
                                }
                            )
                session.commit()
            print(f"✅ Migradas {len(tarjetas)} tarjetas")
    except Exception as e:
        print(f"❌ Error migrando tarjetas: {e}")
        raise


def migrate_prestamos():
    """Migra los datos de préstamos desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/prestamos.json"):
            with open("apis/datos/prestamos.json", 'r', encoding='utf-8') as f:
                prestamos = json.load(f)
            
            with SessionLocal() as session:
                for prestamo in prestamos:
                    # Verificar si el préstamo ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM prestamos WHERE id_prestamo = :id_prestamo"),
                        {"id_prestamo": prestamo["idPrestamo"]}
                    ).scalar()
                    
                    if result == 0:
                        # Obtener el ID interno de la cuenta
                        cuenta_id = session.execute(
                            text("SELECT id FROM cuentas WHERE id = :id_cuenta"),
                            {"id_cuenta": prestamo["idCuenta"]}
                        ).scalar()
                        
                        if cuenta_id:
                            # Insertar préstamo
                            session.execute(
                                text("""
                                INSERT INTO prestamos 
                                (id_prestamo, id_cliente, numero_prestamo, monto_prestado, tasa_interes, 
                                plazo_meses, fecha_desembolso, saldo_pendiente, estado_prestamo, id_cuenta, 
                                id_usuario_creacion, id_usuario_edicion, fecha_creacion, fecha_edicion, activo)
                                VALUES 
                                (:id_prestamo, :id_cliente, :numero_prestamo, :monto_prestado, :tasa_interes, 
                                :plazo_meses, :fecha_desembolso, :saldo_pendiente, :estado_prestamo, :id_cuenta, 
                                :id_usuario_creacion, :id_usuario_edicion, :fecha_creacion, :fecha_edicion, :activo)
                                """),
                                {
                                    "id_prestamo": prestamo["idPrestamo"],
                                    "id_cliente": prestamo["idCliente"],
                                    "numero_prestamo": prestamo["numeroPrestamo"],
                                    "monto_prestado": prestamo["montoPrestado"],
                                    "tasa_interes": prestamo["tasaInteres"],
                                    "plazo_meses": prestamo["plazoMeses"],
                                    "fecha_desembolso": prestamo["fechaDesembolso"],
                                    "saldo_pendiente": prestamo["saldoPendiente"],
                                    "estado_prestamo": prestamo["estadoPrestamo"],
                                    "id_cuenta": prestamo["idCuenta"],
                                    "id_usuario_creacion": prestamo["id_usuario_creacion"],
                                    "id_usuario_edicion": prestamo.get("id_usuario_edicion"),
                                    "fecha_creacion": prestamo["fecha_creacion"],
                                    "fecha_edicion": prestamo.get("fecha_edicion"),
                                    "activo": prestamo.get("activo", True)
                                }
                            )
                session.commit()
            print(f"✅ Migrados {len(prestamos)} préstamos")
    except Exception as e:
        print(f"❌ Error migrando préstamos: {e}")
        raise


def migrate_sucursales():
    """Migra los datos de sucursales desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/sucursales.json"):
            with open("apis/datos/sucursales.json", 'r', encoding='utf-8') as f:
                sucursales = json.load(f)
            
            with SessionLocal() as session:
                for sucursal in sucursales:
                    # Verificar si la sucursal ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM sucursales WHERE id_sucursal = :id_sucursal"),
                        {"id_sucursal": sucursal["idSucursal"]}
                    ).scalar()
                    
                    if result == 0:
                        # Insertar sucursal
                        session.execute(
                            text("""
                            INSERT INTO sucursales 
                            (id_sucursal, nombre_sucursal, direccion, ciudad, codigo_postal, 
                            telefono, gerente_id, estado_sucursal, activo)
                            VALUES 
                            (:id_sucursal, :nombre_sucursal, :direccion, :ciudad, :codigo_postal, 
                            :telefono, :gerente_id, :estado_sucursal, :activo)
                            """),
                            {
                                "id_sucursal": sucursal["idSucursal"],
                                "nombre_sucursal": sucursal["nombreSucursal"],
                                "direccion": sucursal["direccion"],
                                "ciudad": sucursal["ciudad"],
                                "codigo_postal": sucursal["codigoPostal"],
                                "telefono": sucursal["telefono"],
                                "gerente_id": sucursal.get("gerenteId"),
                                "estado_sucursal": sucursal["estadoSucursal"],
                                "activo": sucursal.get("activo", True)
                            }
                        )
                session.commit()
            print(f"✅ Migradas {len(sucursales)} sucursales")
    except Exception as e:
        print(f"❌ Error migrando sucursales: {e}")
        raise


def migrate_empleados():
    """Migra los datos de empleados desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/empleados.json"):
            with open("apis/datos/empleados.json", 'r', encoding='utf-8') as f:
                empleados = json.load(f)
            
            with SessionLocal() as session:
                for empleado in empleados:
                    # Verificar si el empleado ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM empleados WHERE id_empleado = :id_empleado"),
                        {"id_empleado": empleado["idEmpleado"]}
                    ).scalar()
                    
                    if result == 0:
                        # Verificar si la sucursal existe
                        sucursal_id = session.execute(
                            text("SELECT id FROM sucursales WHERE id_sucursal = :id_sucursal"),
                            {"id_sucursal": empleado["idSucursal"]}
                        ).scalar()
                        
                        if sucursal_id:
                            # Insertar empleado
                            session.execute(
                                text("""
                                INSERT INTO empleados 
                                (id_empleado, nombre_completo, cargo, id_sucursal, numero_documento, 
                                tipo_documento, correo_electronico, telefono, estado_empleado, activo)
                                VALUES 
                                (:id_empleado, :nombre_completo, :cargo, :id_sucursal, :numero_documento, 
                                :tipo_documento, :correo_electronico, :telefono, :estado_empleado, :activo)
                                """),
                                {
                                    "id_empleado": empleado["idEmpleado"],
                                    "nombre_completo": empleado["nombreCompleto"],
                                    "cargo": empleado["cargo"],
                                    "id_sucursal": empleado["idSucursal"],
                                    "numero_documento": empleado["numeroDocumento"],
                                    "tipo_documento": empleado["tipoDocumento"],
                                    "correo_electronico": empleado["correoElectronico"],
                                    "telefono": empleado["telefono"],
                                    "estado_empleado": empleado["estadoEmpleado"],
                                    "activo": empleado.get("activo", True)
                                }
                            )
                session.commit()
            print(f"✅ Migrados {len(empleados)} empleados")
    except Exception as e:
        print(f"❌ Error migrando empleados: {e}")
        raise


def migrate_cheques():
    """Migra los datos de cheques desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/cheques.json"):
            with open("apis/datos/cheques.json", 'r', encoding='utf-8') as f:
                cheques = json.load(f)
            
            with SessionLocal() as session:
                for cheque in cheques:
                    # Verificar si el cheque ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM cheques WHERE id_cheque = :id_cheque"),
                        {"id_cheque": cheque["idCheque"]}
                    ).scalar()
                    
                    if result == 0:
                        # Obtener el ID interno de la cuenta
                        cuenta_id = session.execute(
                            text("SELECT id FROM cuentas WHERE id = :id_cuenta"),
                            {"id_cuenta": cheque["idCuenta"]}
                        ).scalar()
                        
                        if cuenta_id:
                            # Insertar cheque
                            session.execute(
                                text("""
                                INSERT INTO cheques 
                                (id_cheque, numero_cheque, id_cuenta, monto, beneficiario, 
                                fecha_emision, fecha_vencimiento, estado_cheque, activo)
                                VALUES 
                                (:id_cheque, :numero_cheque, :id_cuenta, :monto, :beneficiario, 
                                :fecha_emision, :fecha_vencimiento, :estado_cheque, :activo)
                                """),
                                {
                                    "id_cheque": cheque["idCheque"],
                                    "numero_cheque": cheque["numeroCheque"],
                                    "id_cuenta": cheque["idCuenta"],
                                    "monto": cheque["monto"],
                                    "beneficiario": cheque["beneficiario"],
                                    "fecha_emision": cheque["fechaEmision"],
                                    "fecha_vencimiento": cheque["fechaVencimiento"],
                                    "estado_cheque": cheque["estadoCheque"],
                                    "activo": cheque.get("activo", True)
                                }
                            )
                session.commit()
            print(f"✅ Migrados {len(cheques)} cheques")
    except Exception as e:
        print(f"❌ Error migrando cheques: {e}")
        raise


def migrate_inversiones():
    """Migra los datos de inversiones desde JSON a la base de datos"""
    try:
        if os.path.exists("apis/datos/inversiones.json"):
            with open("apis/datos/inversiones.json", 'r', encoding='utf-8') as f:
                inversiones = json.load(f)
            
            with SessionLocal() as session:
                for inversion in inversiones:
                    # Verificar si la inversión ya existe
                    result = session.execute(
                        text("SELECT COUNT(*) FROM inversiones WHERE id_inversion = :id_inversion"),
                        {"id_inversion": inversion["idInversion"]}
                    ).scalar()
                    
                    if result == 0:
                        # Obtener el ID interno de la cuenta
                        cuenta_id = session.execute(
                            text("SELECT id FROM cuentas WHERE id = :id_cuenta"),
                            {"id_cuenta": inversion["idCuenta"]}
                        ).scalar()
                        
                        if cuenta_id:
                            # Insertar inversión
                            session.execute(
                                text("""
                                INSERT INTO inversiones 
                                (id_inversion, id_cliente, tipo_inversion, monto_invertido, fecha_inicio, 
                                plazo, rendimiento_esperado, estado_inversion, id_cuenta, 
                                id_usuario_creacion, id_usuario_edicion, fecha_creacion, fecha_edicion, activo)
                                VALUES 
                                (:id_inversion, :id_cliente, :tipo_inversion, :monto_invertido, :fecha_inicio, 
                                :plazo, :rendimiento_esperado, :estado_inversion, :id_cuenta, 
                                :id_usuario_creacion, :id_usuario_edicion, :fecha_creacion, :fecha_edicion, :activo)
                                """),
                                {
                                    "id_inversion": inversion["idInversion"],
                                    "id_cliente": inversion["idCliente"],
                                    "tipo_inversion": inversion["tipoInversion"],
                                    "monto_invertido": inversion["montoInvertido"],
                                    "fecha_inicio": inversion["fechaInicio"],
                                    "plazo": inversion["plazo"],
                                    "rendimiento_esperado": inversion["rendimientoEsperado"],
                                    "estado_inversion": inversion["estadoInversion"],
                                    "id_cuenta": inversion["idCuenta"],
                                    "id_usuario_creacion": inversion["id_usuario_creacion"],
                                    "id_usuario_edicion": inversion.get("id_usuario_edicion"),
                                    "fecha_creacion": inversion["fecha_creacion"],
                                    "fecha_edicion": inversion.get("fecha_edicion"),
                                    "activo": inversion.get("activo", True)
                                }
                            )
                session.commit()
            print(f"✅ Migradas {len(inversiones)} inversiones")
    except Exception as e:
        print(f"❌ Error migrando inversiones: {e}")
        raise


def delete_json_files():
    """Elimina los archivos JSON después de la migración"""
    try:
        json_files = [
            "apis/datos/clientes.json.json",
            "apis/datos/cuentas.json.json",
            "apis/datos/transacciones.json",
            "apis/datos/tarjetas.json",
            "apis/datos/prestamos.json",
            "apis/datos/sucursales.json",
            "apis/datos/empleados.json",
            "apis/datos/cheques.json",
            "apis/datos/inversiones.json"
        ]
        
        for file_path in json_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Archivo {file_path} eliminado")
        
        print("✅ Todos los archivos JSON han sido eliminados")
        return True
    except Exception as e:
        print(f"❌ Error eliminando archivos JSON: {e}")
        return False


def eliminar_archivos_json():
    """Elimina los archivos JSON después de la migración exitosa"""
    try:
        archivos_json = [
            "apis/datos/clientes.json.json",
            "apis/datos/cuentas.json.json",
            "apis/datos/transacciones.json"
        ]
        
        for archivo in archivos_json:
            if os.path.exists(archivo):
                # Crear una copia de respaldo antes de eliminar
                backup_path = f"{archivo}.bak"
                os.rename(archivo, backup_path)
                print(f"Archivo {archivo} respaldado como {backup_path}")
        
        print("Todos los archivos JSON han sido respaldados")
    except Exception as e:
        print(f"Error al respaldar archivos JSON: {e}")

def ejecutar_migracion():
    """Ejecuta todas las migraciones en orden"""
    try:
        print("Iniciando migración de datos JSON a SQL Server...")
        
        # Ejecutar migraciones en orden
        migrate_clientes()
        migrate_cuentas()
        migrate_transacciones()
        
        # Preguntar si se desean eliminar los archivos JSON
        respuesta = input("¿Desea respaldar los archivos JSON? (s/n): ")
        if respuesta.lower() == 's':
            eliminar_archivos_json()
            
        print("Migración completada exitosamente")
    except Exception as e:
        print(f"Error durante la migración: {e}")
        print("La migración no se completó correctamente")

if __name__ == "__main__":
    # Ejecutar migraciones
    ejecutar_migracion()