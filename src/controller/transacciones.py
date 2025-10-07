from sqlalchemy.orm import Session
from src.entities.transacciones import Transacciones


# Crear Transacción
def create_transaccion(db: Session, transaccion: Transacciones):
    new_transaccion = Transacciones(
        idCuenta=str(transaccion.idCuenta),
        tipo=transaccion.tipo,
        monto=transaccion.monto,
        fecha=transaccion.fecha,
        descripcion=transaccion.descripcion,
    )
    db.add(new_transaccion)
    db.commit()
    db.refresh(new_transaccion)
    return new_transaccion


# Obtener Transacción por ID
def get_transaccion(db: Session, transaccion_id: str):
    return db.query(Transacciones).filter(Transacciones.idTransaccion == transaccion_id).first()


# Listar todas las Transacciones
def get_transacciones(db: Session):
    return db.query(Transacciones).all()


# Actualizar Transacción
def update_transaccion(db: Session, transaccion_id: str, transaccion: Transacciones):
    db_transaccion = db.query(Transacciones).filter(Transacciones.idTransaccion == transaccion_id).first()
    if db_transaccion:
        db_transaccion.idCuenta = str(transaccion.idCuenta)
        db_transaccion.tipo = transaccion.tipo
        db_transaccion.monto = transaccion.monto
        db_transaccion.fecha = transaccion.fecha
        db_transaccion.descripcion = transaccion.descripcion
        db.commit()
        db.refresh(db_transaccion)
    return db_transaccion


# Eliminar Transacción
def delete_transaccion(db: Session, transaccion_id: str):
    db_transaccion = db.query(Transacciones).filter(Transacciones.idTransaccion == transaccion_id).first()
    if db_transaccion:
        db.delete(db_transaccion)
        db.commit()
    return db_transaccion
