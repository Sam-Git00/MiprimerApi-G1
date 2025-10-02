from sqlalchemy.orm import Session
from src.entities.empleados import Empleados


# Crear Empleado
def create_empleado(db: Session, empleado: Empleados):
    new_empleado = Empleados(
        nombre=empleado.nombre,
        apellido=empleado.apellido,
        documento=empleado.documento,
        cargo=empleado.cargo,
        telefono=empleado.telefono,
        email=empleado.email,
        fechaContratacion=empleado.fechaContratacion,
    )
    db.add(new_empleado)
    db.commit()
    db.refresh(new_empleado)
    return new_empleado


# Obtener Empleado por ID
def get_empleado(db: Session, empleado_id: str):
    return db.query(Empleados).filter(Empleados.idEmpleado == empleado_id).first()


# Listar todos los Empleados
def get_empleados(db: Session):
    return db.query(Empleados).all()


# Actualizar Empleado
def update_empleado(db: Session, empleado_id: str, empleado: Empleados):
    db_empleado = db.query(Empleados).filter(Empleados.idEmpleado == empleado_id).first()
    if db_empleado:
        db_empleado.nombre = empleado.nombre
        db_empleado.apellido = empleado.apellido
        db_empleado.documento = empleado.documento
        db_empleado.cargo = empleado.cargo
        db_empleado.telefono = empleado.telefono
        db_empleado.email = empleado.email
        db_empleado.fechaContratacion = empleado.fechaContratacion
        db.commit()
        db.refresh(db_empleado)
    return db_empleado


# Eliminar Empleado
def delete_empleado(db: Session, empleado_id: str):
    db_empleado = db.query(Empleados).filter(Empleados.idEmpleado == empleado_id).first()
    if db_empleado:
        db.delete(db_empleado)
        db.commit()
    return db_empleado
