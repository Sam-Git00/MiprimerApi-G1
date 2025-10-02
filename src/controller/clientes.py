from sqlalchemy.orm import Session
from src.entities.clientes import Clientes


# Crear Cliente
def create_cliente(db: Session, cliente: Clientes):
    new_cliente = Clientes(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        documento=cliente.documento,
        direccion=cliente.direccion,
        telefono=cliente.telefono,
        email=cliente.email,
        fechaNacimiento=cliente.fechaNacimiento,
    )
    db.add(new_cliente)
    db.commit()
    db.refresh(new_cliente)
    return new_cliente


# Obtener Cliente por ID
def get_cliente(db: Session, cliente_id: str):
    return db.query(Clientes).filter(Clientes.idCliente == cliente_id).first()


# Listar todos los Clientes
def get_clientes(db: Session):
    return db.query(Clientes).all()


# Actualizar Cliente
def update_cliente(db: Session, cliente_id: str, cliente: Clientes):
    db_cliente = db.query(Clientes).filter(Clientes.idCliente == cliente_id).first()
    if db_cliente:
        db_cliente.nombre = cliente.nombre
        db_cliente.apellido = cliente.apellido
        db_cliente.documento = cliente.documento
        db_cliente.direccion = cliente.direccion
        db_cliente.telefono = cliente.telefono
        db_cliente.email = cliente.email
        db_cliente.fechaNacimiento = cliente.fechaNacimiento
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


# Eliminar Cliente
def delete_cliente(db: Session, cliente_id: str):
    db_cliente = db.query(Clientes).filter(Clientes.idCliente == cliente_id).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente
