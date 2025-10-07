from sqlalchemy.orm import Session
from src.entities.cuentas import Cuentas


def create_cuenta(db: Session, cuenta: Cuentas):
    new_cuenta = Cuentas(
        idCliente=cuenta.idCliente,
        numeroCuenta=cuenta.numeroCuenta,
        tipoCuenta=cuenta.tipoCuenta,
        saldo=cuenta.saldo,
        estado=cuenta.estado,
    )
    db.add(new_cuenta)
    db.commit()
    db.refresh(new_cuenta)
    return new_cuenta


def get_cuenta(db: Session, cuenta_id: str):
    return db.query(Cuentas).filter(Cuentas.idCuenta == cuenta_id).first()


def get_cuentas(db: Session):
    return db.query(Cuentas).all()


def update_cuenta(db: Session, cuenta_id: str, cuenta: Cuentas):
    db_cuenta = db.query(Cuentas).filter(Cuentas.idCuenta == cuenta_id).first()
    if db_cuenta:
        db_cuenta.idCliente = cuenta.idCliente
        db_cuenta.numeroCuenta = cuenta.numeroCuenta
        db_cuenta.tipoCuenta = cuenta.tipoCuenta
        db_cuenta.saldo = cuenta.saldo
        db_cuenta.estado = cuenta.estado
        db.commit()
        db.refresh(db_cuenta)
    return db_cuenta


def delete_cuenta(db: Session, cuenta_id: str):
    db_cuenta = db.query(Cuentas).filter(Cuentas.idCuenta == cuenta_id).first()
    if db_cuenta:
        db.delete(db_cuenta)
        db.commit()
    return db_cuenta
