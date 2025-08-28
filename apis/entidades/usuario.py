from pydantic import BaseModel, Field

class Usuario(BaseModel):
    nombreUsuario: str = Field(..., examples=["admin"], description="Nombre de usuario")
    contrasena: str = Field(..., examples=["admin123"], description="Contraseña del usuario")

class UsuarioLogin(BaseModel):
    nombreUsuario: str = Field(..., examples=["admin"])
    contrasena: str = Field(..., examples=["admin123"])

class TokenRespuesta(BaseModel):
    token: str = Field(..., examples=["eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."])
    tipoToken: str = Field(default="Bearer", examples=["Bearer"])
    mensaje: str = Field(..., examples=["Login exitoso"])
