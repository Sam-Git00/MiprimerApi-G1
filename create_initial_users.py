"""
Script para crear usuarios iniciales del sistema.
"""

import sys

from sqlalchemy.orm import Session

from database.connection import SessionLocal, create_tables
from src.controller.auth_controller import create_user
from src.schemas.auth import UserCreate


def create_initial_users():
    """
    Crea usuarios iniciales para el sistema.
    """
    # Crear tablas si no existen
    create_tables()

    db = SessionLocal()
    try:
        # Usuario administrador
        admin_user = UserCreate(
            username="admin",
            email="admin@banco.com",
            nombre_completo="Administrador del Sistema",
            password="admin123",
            rol="admin",
        )

        # Usuario empleado
        empleado_user = UserCreate(
            username="empleado_test",
            email="empleado.test@banco.com",
            nombre_completo="Empleado Test",
            password="empleado123",
            rol="empleado",
        )

        # Usuario cuenta
        cuenta_user = UserCreate(
            username="cuenta_test",
            email="cuenta.test@banco.com",
            nombre_completo="Cuenta Test",
            password="cuenta123",
            rol="cuenta",
        )

        # Usuario regular
        usuario_user = UserCreate(
            username="usuario_test",
            email="usuario@banco.com",
            nombre_completo="Usuario de Prueba",
            password="usuario123",
            rol="usuario",
        )

        users_to_create = [admin_user, empleado_user, cuenta_user, usuario_user]

        for user_data in users_to_create:
            try:
                create_user(db, user_data)
                print(f"Usuario creado: {user_data.username} ({user_data.rol})")
            except ValueError as e:
                print(f"Usuario {user_data.username} ya existe: {e}")
        users_to_create = [admin_user, empleado_user, cuenta_user, usuario_user]

        for user_data in users_to_create:
            try:
                create_user(db, user_data)
                print(f"Usuario creado: {user_data.username} ({user_data.rol})")
            except ValueError as e:
                print(f"Usuario {user_data.username} ya existe: {e}")

        print("\nUsuarios iniciales creados exitosamente!")
        print("\nCredenciales de acceso:")
        print("\nAdmin: admin / admin123")
        print("\nEmpleado: empleado_test / empleado123")
        print("\nCuenta: cuenta_test / cuenta123")
        print("\nUsuario: usuario_test / usuario123")

    except Exception as e:
        print(f"Error creando usuarios: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_users()
