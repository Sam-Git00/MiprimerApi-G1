from fastapi import APIRouter, HTTPException, Header
from entidades.usuario import UsuarioLogin, TokenRespuesta
from negocio.auth_negocio import AuthNegocio

router = APIRouter(prefix="/auth", tags=["Autenticación"])
auth_negocio = AuthNegocio()

@router.post(
    "/login",
    response_model=TokenRespuesta,
    summary="Iniciar sesión",
    description="Autentica un usuario y retorna un token de acceso",
    responses={
        200: {"description": "Login exitoso"},
        401: {"description": "Credenciales inválidas"}
    }
)
def login(credenciales: UsuarioLogin) -> TokenRespuesta:
    return auth_negocio.login(credenciales)

@router.post(
    "/logout",
    summary="Cerrar sesión",
    description="Invalida el token de acceso del usuario",
    responses={
        200: {"description": "Logout exitoso"},
        401: {"description": "Token inválido"}
    }
)
def logout(authorization: str = Header(..., description="Bearer token")) -> dict:
    # Extraer token del header Authorization
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    token = authorization.replace("Bearer ", "")
    return auth_negocio.logout(token)

@router.get(
    "/validar",
    summary="Validar token",
    description="Valida si un token de acceso es válido",
    responses={
        200: {"description": "Token válido"},
        401: {"description": "Token inválido"}
    }
)
def validar_token(authorization: str = Header(..., description="Bearer token")) -> dict:
    # Extraer token del header Authorization
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Formato de token inválido")
    
    token = authorization.replace("Bearer ", "")
    if auth_negocio.validar_token(token):
        return {"mensaje": "Token válido", "estado": "activo"}
    else:
        raise HTTPException(status_code=401, detail="Token inválido")
