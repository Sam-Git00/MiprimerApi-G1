from sqlalchemy.orm import Session
from src.entities.prestamos import Prestamos


def create_prestamo(db: Session, prestamo: Prestamos):
    new_prestamo = Prestamos(
        idCliente=prestamo.idCliente,
        idEmpleado=prestamo.idEmpleado,
        monto=prestamo.monto,
        interes=prestamo.interes,
        plazo=prestamo.plazoMeses,
        estado=prestamo.estado,
    )
    db.add(new_prestamo)
    db.commit()
    db.refresh(new_prestamo)
    return new_prestamo


def get_prestamo(db: Session, prestamo_id: str):
    return db.query(Prestamos).filter(Prestamos.idPrestamo == prestamo_id).first()


def get_prestamos(db: Session):
    return db.query(Prestamos).all()


def update_prestamo(db: Session, prestamo_id: str, prestamo: Prestamos):
    db_prestamo = db.query(Prestamos).filter(Prestamos.idPrestamo == prestamo_id).first()
    if db_prestamo:
        db_prestamo.idCliente = prestamo.idCliente
        db_prestamo.monto = prestamo.monto
        db_prestamo.tasaInteres = prestamo.tasaInteres
        db_prestamo.fechaInicio = prestamo.fechaInicio
        db_prestamo.fechaFin = prestamo.fechaFin
        db_prestamo.estado = prestamo.estado
        db.commit()
        db.refresh(db_prestamo)
    return db_prestamo


def delete_prestamo(db: Session, prestamo_id: str):
    db_prestamo = db.query(Prestamos).filter(Prestamos.idPrestamo == prestamo_id).first()
    if db_prestamo:
        db.delete(db_prestamo)
        db.commit()
    return db_prestamo
