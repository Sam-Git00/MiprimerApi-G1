from sqlalchemy.orm import Session
from src.entities.cheques import Cheques

# Crear Cheque
def create_cheque(db: Session, cheque: Cheques):
    new_cheque = Cheques(
        idCliente=str(cheque.idCliente),
        idCuenta=str(cheque.idCuenta),
        fechaEmision=cheque.fechaEmision,
        monto=cheque.monto,
        motivo=cheque.motivo,
    )
    db.add(new_cheque)
    db.commit()
    db.refresh(new_cheque)
    return new_cheque


# Obtener un cheque por ID
def get_cheque(db: Session, cheque_id: str):
    return db.query(Cheques).filter(Cheques.idCheque == cheque_id).first()


# Listar todos los cheques
def get_cheques(db: Session):
    return db.query(Cheques).all()


# Actualizar un cheque
def update_cheque(db: Session, cheque_id: str, cheque: Cheques):
    db_cheque = db.query(Cheques).filter(Cheques.idCheque == cheque_id).first()
    if db_cheque:
        db_cheque.idCliente = str(cheque.idCliente)
        db_cheque.idCuenta = str(cheque.idCuenta)
        db_cheque.fechaEmision = cheque.fechaEmision
        db_cheque.monto = cheque.monto
        db_cheque.estado = cheque.estado
        db_cheque.motivo = cheque.motivo
        db.commit()
        db.refresh(db_cheque)
    return db_cheque


# Eliminar un cheque
def delete_cheque(db: Session, cheque_id: str):
    db_cheque = db.query(Cheques).filter(Cheques.idCheque == cheque_id).first()
    if db_cheque:
        db.delete(db_cheque)
        db.commit()
    return db_cheque
