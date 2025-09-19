import json
import os
import sys
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dotenv import load_dotenv
import uuid

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apis.models.models import Base, Cliente, Cuenta, Transaccion, Usuario, Tarjeta, Prestamo, Empleado, Sucursal, Cheque, Inversion
from apis.database.connection import get_engine, SessionLocal

load_dotenv()

# Obtener el motor de SQLAlchemy
engine = get_engine()

def migrate_admin_user():
    """Inserta el usuario administrador por defecto si no existe"""
    try:
        with SessionLocal() as session:
            admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()
            if not admin_user:
                admin_user_id = uuid.UUID('550e8400-e29b-41d4-a716-446655440001') # ID fijo para el admin
                nuevo_admin = Usuario(
                    id=admin_user_id,
                    nombre_usuario='admin',
                    correo_electronico='admin@bancoapi.com',
                    contrasena='hashed_password_here', # Considerar usar un hash real en producción
                    rol='administrador',
                    fecha_creacion=datetime.now(),
                    activo=True
                )
                session.add(nuevo_admin)
                session.commit()
                print("✅ Usuario administrador insertado exitosamente.")
            else:
                print("Usuario administrador ya existe.")
    except Exception as e:
        print(f"❌ Error al insertar usuario administrador: {e}")
        raise


def migrate_json_to_db():
    """Migra los datos de los archivos JSON a la base de datos SQL Server"""
    try:
        print("Iniciando migración de datos JSON a la base de datos...")
        
        # Verificar conexión a la base de datos
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión a la base de datos exitosa")

        # Insertar usuario administrador antes de migrar otros datos que dependen de él
        migrate_admin_user()
        
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
                for tarjeta_data in tarjetas:
                    # Verificar si la tarjeta ya existe
                    tarjeta_existente = session.query(Tarjeta).filter(Tarjeta.id_tarjeta == tarjeta_data["idTarjeta"]).first()
                    
                    if not tarjeta_existente:
                        # Verificar si la cuenta y el cliente existen
                        cuenta = session.query(Cuenta).filter(Cuenta.id == tarjeta_data["idCuenta"]).first()
                        cliente = session.query(Cliente).filter(Cliente.id_cliente == tarjeta_data["idCliente"]).first()
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()

                        if cuenta and cliente and admin_user:
                            # Crear nueva tarjeta
                            nueva_tarjeta = Tarjeta(
                                id_tarjeta=tarjeta_data['idTarjeta'],
                                numero_tarjeta=tarjeta_data['numeroTarjeta'],
                                tipo_tarjeta=tarjeta_data['tipoTarjeta'],
                                id_cuenta=tarjeta_data['idCuenta'],
                                id_cliente=tarjeta_data['idCliente'],
                                fecha_vencimiento=datetime.strptime(tarjeta_data['fechaVencimiento'], '%Y-%m-%d'),
                                cvv=tarjeta_data['cvv'],
                                estado_tarjeta=tarjeta_data['estadoTarjeta'],
                                limite_credito=tarjeta_data.get('limiteCredito'),
                                id_usuario_creacion=admin_user.id,
                                fecha_creacion=datetime.now(),
                                activo=tarjeta_data.get('activo', True)
                            )
                            
                            session.add(nueva_tarjeta)
                        else:
                            print(f"Advertencia: No se pudo migrar la tarjeta {tarjeta_data['idTarjeta']} - cuenta, cliente o usuario administrador no encontrado.")
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
                for prestamo_data in prestamos:
                    # Verificar si el préstamo ya existe
                    prestamo_existente = session.query(Prestamo).filter(Prestamo.id_prestamo == prestamo_data["idPrestamo"]).first()
                    
                    if not prestamo_existente:
                        # Verificar si el cliente, la cuenta y el usuario administrador existen
                        cliente = session.query(Cliente).filter(Cliente.id_cliente == prestamo_data["idCliente"]).first()
                        cuenta = session.query(Cuenta).filter(Cuenta.id == prestamo_data["idCuenta"]).first()
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()

                        if cliente and cuenta and admin_user:
                            # Crear nuevo préstamo
                            nuevo_prestamo = Prestamo(
                                id_prestamo=prestamo_data['idPrestamo'],
                                id_cliente=prestamo_data['idCliente'],
                                numero_prestamo=prestamo_data['numeroPrestamo'],
                                monto_prestado=prestamo_data['montoPrestado'],
                                tas_interes=prestamo_data['tasaInteres'],
                                plazo_meses=prestamo_data['plazoMeses'],
                                fecha_desembolso=datetime.strptime(prestamo_data['fechaDesembolso'], '%Y-%m-%d'),
                                saldo_pendiente=prestamo_data['saldoPendiente'],
                                estado_prestamo=prestamo_data['estadoPrestamo'],
                                id_cuenta=prestamo_data['idCuenta'],
                                id_usuario_creacion=admin_user.id,
                                fecha_creacion=datetime.now(),
                                activo=prestamo_data.get('activo', True)
                            )
                            
                            session.add(nuevo_prestamo)
                        else:
                            print(f"Advertencia: No se pudo migrar el préstamo {prestamo_data['idPrestamo']} - cliente, cuenta o usuario administrador no encontrado.")
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
                for sucursal_data in sucursales:
                    # Verificar si la sucursal ya existe
                    sucursal_existente = session.query(Sucursal).filter(Sucursal.id_sucursal == sucursal_data["idSucursal"]).first()
                    
                    if not sucursal_existente:
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()
                        gerente = None
                        if sucursal_data.get("gerenteId"):
                            gerente = session.query(Empleado).filter(Empleado.id_empleado == sucursal_data["gerenteId"]).first()

                        if admin_user:
                            # Crear nueva sucursal
                            nueva_sucursal = Sucursal(
                                id_sucursal=sucursal_data['idSucursal'],
                                nombre_sucursal=sucursal_data['nombreSucursal'],
                                direccion=sucursal_data['direccion'],
                                ciudad=sucursal_data['ciudad'],
                                codigo_postal=sucursal_data['codigoPostal'],
                                telefono=sucursal_data['telefono'],
                                gerente_id=sucursal_data.get('gerenteId'),
                                estado_sucursal=sucursal_data['estadoSucursal'],
                                activo=sucursal_data.get('activo', True)
                            )
                            
                            session.add(nueva_sucursal)
                        else:
                            print(f"Advertencia: No se pudo migrar la sucursal {sucursal_data['idSucursal']} - usuario administrador no encontrado.")
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
                for empleado_data in empleados:
                    # Verificar si el empleado ya existe
                    empleado_existente = session.query(Empleado).filter(Empleado.id_empleado == empleado_data["idEmpleado"]).first()
                    
                    if not empleado_existente:
                        # Verificar si la sucursal y el usuario administrador existen
                        sucursal = session.query(Sucursal).filter(Sucursal.id_sucursal == empleado_data["idSucursal"]).first()
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()

                        if sucursal and admin_user:
                            # Crear nuevo empleado
                            nuevo_empleado = Empleado(
                                id_empleado=empleado_data['idEmpleado'],
                                nombre_completo=empleado_data['nombreCompleto'],
                                cargo=empleado_data['cargo'],
                                id_sucursal=empleado_data['idSucursal'],
                                numero_documento=empleado_data['numeroDocumento'],
                                tipo_documento=empleado_data['tipoDocumento'],
                                correo_electronico=empleado_data['correoElectronico'],
                                telefono=empleado_data['telefono'],
                                estado_empleado=empleado_data['estadoEmpleado'],
                                activo=empleado_data.get('activo', True),
                                id_usuario_creacion=admin_user.id,
                                fecha_creacion=datetime.now()
                            )
                            
                            session.add(nuevo_empleado)
                        else:
                            print(f"Advertencia: No se pudo migrar el empleado {empleado_data['idEmpleado']} - sucursal o usuario administrador no encontrado.")
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
                for cheque_data in cheques:
                    # Verificar si el cheque ya existe
                    cheque_existente = session.query(Cheque).filter(Cheque.id_cheque == cheque_data["idCheque"]).first()
                    
                    if not cheque_existente:
                        # Verificar si la cuenta y el usuario administrador existen
                        cuenta = session.query(Cuenta).filter(Cuenta.id == cheque_data["idCuenta"]).first()
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()

                        if cuenta and admin_user:
                            # Crear nuevo cheque
                            nuevo_cheque = Cheque(
                                id_cheque=cheque_data['idCheque'],
                                numero_cheque=cheque_data['numeroCheque'],
                                id_cuenta=cheque_data['idCuenta'],
                                monto=cheque_data['monto'],
                                beneficiario=cheque_data['beneficiario'],
                                fecha_emision=datetime.strptime(cheque_data['fechaEmision'], '%Y-%m-%d'),
                                fecha_vencimiento=datetime.strptime(cheque_data['fechaVencimiento'], '%Y-%m-%d'),
                                estado_cheque=cheque_data['estadoCheque'],
                                activo=cheque_data.get('activo', True),
                                id_usuario_creacion=admin_user.id,
                                fecha_creacion=datetime.now()
                            )
                            
                            session.add(nuevo_cheque)
                        else:
                            print(f"Advertencia: No se pudo migrar el cheque {cheque_data['idCheque']} - cuenta o usuario administrador no encontrado.")
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
                for inversion_data in inversiones:
                    # Verificar si la inversión ya existe
                    inversion_existente = session.query(Inversion).filter(Inversion.id_inversion == inversion_data["idInversion"]).first()
                    
                    if not inversion_existente:
                        # Verificar si el cliente, la cuenta y el usuario administrador existen
                        cliente = session.query(Cliente).filter(Cliente.id_cliente == inversion_data["idCliente"]).first()
                        cuenta = session.query(Cuenta).filter(Cuenta.id == inversion_data["idCuenta"]).first()
                        admin_user = session.query(Usuario).filter(Usuario.correo_electronico == 'admin@bancoapi.com').first()

                        if cliente and cuenta and admin_user:
                            # Crear nueva inversión
                            nueva_inversion = Inversion(
                                id_inversion=inversion_data['idInversion'],
                                id_cliente=inversion_data['idCliente'],
                                tipo_inversion=inversion_data['tipoInversion'],
                                monto_invertido=inversion_data['montoInvertido'],
                                fecha_inicio=datetime.strptime(inversion_data['fechaInicio'], '%Y-%m-%d'),
                                plazo=inversion_data['plazo'],
                                rendimiento_esperado=inversion_data['rendimientoEsperado'],
                                estado_inversion=inversion_data['estadoInversion'],
                                id_cuenta=inversion_data['idCuenta'],
                                id_usuario_creacion=admin_user.id,
                                fecha_creacion=datetime.now(),
                                activo=inversion_data.get('activo', True)
                            )
                            
                            session.add(nueva_inversion)
                        else:
                            print(f"Advertencia: No se pudo migrar la inversión {inversion_data['idInversion']} - cliente, cuenta o usuario administrador no encontrado.")
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

def ejecutar_migracion():
    """Ejecuta todas las migraciones en orden"""
    try:
        print("Iniciando migración de datos JSON a SQL Server...")
        
        # Ejecutar migraciones en orden
        migrate_clientes()
        migrate_cuentas()
        migrate_transacciones()
        migrate_tarjetas()
        migrate_prestamos()
        migrate_sucursales()
        migrate_empleados()
        migrate_cheques()
        migrate_inversiones()
        
        # Preguntar si se desean eliminar los archivos JSON
        respuesta = input("¿Desea eliminar los archivos JSON originales después de la migración? (s/n): ")
        if respuesta.lower() == 's':
            delete_json_files()
            
        print("Migración completada exitosamente")
    except Exception as e:
        print(f"Error durante la migración: {e}")
        print("La migración no se completó correctamente")

if __name__ == "__main__":
    # Ejecutar migraciones
    ejecutar_migracion()