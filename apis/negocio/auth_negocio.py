from fastapi import HTTPException
from entidades.usuario import Usuario, UsuarioLogin, TokenRespuesta
import json
import os
import secrets

class AuthNegocio:
    def __init__(self):
        self.archivo_datos = "datos/usuarios.json"
        self.tokens_activos = set()
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.usuarios_db = [Usuario(**usuario) for usuario in datos]
        else:
            self.usuarios_db = []
    
    def _guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        os.makedirs(os.path.dirname(self.archivo_datos), exist_ok=True)
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            datos = [usuario.dict() for usuario in self.usuarios_db]
            json.dump(datos, f, ensure_ascii=False, indent=2)
    
    def login(self, credenciales: UsuarioLogin) -> TokenRespuesta:
        """Autentica un usuario y genera un token"""
        for usuario in self.usuarios_db:
            if (usuario.nombreUsuario == credenciales.nombreUsuario and 
                usuario.contrasena == credenciales.contrasena):
                
                # Generar token simple (en producción usar JWT)
                token = secrets.token_urlsafe(32)
                self.tokens_activos.add(token)
                
                return TokenRespuesta(
                    token=token,
                    mensaje=f"Login exitoso para {credenciales.nombreUsuario}"
                )
        
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    def validar_token(self, token: str) -> bool:
        """Valida si un token es válido"""
        return token in self.tokens_activos
    
    def logout(self, token: str) -> dict:
        """Cierra sesión invalidando el token"""
        if token in self.tokens_activos:
            self.tokens_activos.remove(token)
            return {"mensaje": "Logout exitoso"}
        raise HTTPException(status_code=401, detail="Token inválido")
