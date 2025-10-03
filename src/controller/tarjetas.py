from sqlalchemy.orm import Session
from src.entities.tarjetas import Tarjetas


def create_tarjeta(db: Session, tarjeta: Tarjetas):
    new_tarjeta = Tarjetas(
        idCuenta=tarjeta.idCuenta,
        numeroTarjeta=tarjeta.numeroTarjeta,
        tipo=tarjeta.tipo,
        limiteCredito=tarjeta.limiteCredito,
        saldoDisponible=tarjeta.saldoDisponible,
        fechaExpiracion=tarjeta.fechaExpiracion,
        estado=tarjeta.estado,
    )
    db.add(new_tarjeta)
    db.commit()
    db.refresh(new_tarjeta)
    return new_tarjeta


def get_tarjeta(db: Session, tarjeta_id: str):
    return db.query(Tarjetas).filter(Tarjetas.idTarjeta == tarjeta_id).first()


def get_tarjetas(db: Session):
    return db.query(Tarjetas).all()


def update_tarjeta(db: Session, tarjeta_id: str, tarjeta: Tarjetas):
    db_tarjeta = db.query(Tarjetas).filter(Tarjetas.idTarjeta == tarjeta_id).first()
    if db_tarjeta:
        db_tarjeta.idCuenta = tarjeta.idCuenta
        db_tarjeta.numeroTarjeta = tarjeta.numeroTarjeta
        db_tarjeta.tipo = tarjeta.tipo
        db_tarjeta.limiteCredito = tarjeta.limiteCredito
        db_tarjeta.saldoDisponible = tarjeta.saldoDisponible
        db_tarjeta.fechaExpiracion = tarjeta.fechaExpiracion
        db_tarjeta.estado = tarjeta.estado
        db.commit()
        db.refresh(db_tarjeta)
    return db_tarjeta


def delete_tarjeta(db: Session, tarjeta_id: str):
    db_tarjeta = db.query(Tarjetas).filter(Tarjetas.idTarjeta == tarjeta_id).first()
    if db_tarjeta:
        db.delete(db_tarjeta)
        db.commit()
    return db_tarjeta
