from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuario import Usuario, UserRole
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioLogin,
    RecuperarRequest,
    RestablecerRequest,
)
from app.core.security import hash_password, verify_password, create_access_token
from app.services.recuperacion_password import (
    solicitar_recuperacion,
    restablecer_password,
)
from app.services.email_service import send_recovery_email

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UsuarioResponse)
def register(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario como adoptante."""

    new_user = Usuario(
        nombre=user_data.nombre,
        email=user_data.email,
        telefono=user_data.telefono,
        password_hash=hash_password(user_data.password),
        rol=UserRole.adoptante
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT."""
    
    user = db.query(Usuario).filter(Usuario.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "sub": str(user.id),
        "rol": user.rol.value
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/recuperar")
def solicitar_recuperacion_endpoint(
    body: RecuperarRequest,
    db: Session = Depends(get_db),
):
    """Envía un token de recuperación al email del usuario."""
    token = solicitar_recuperacion(db, body.email)
    if token:
        send_recovery_email(body.email, token)

    return {"message": "Revisa tu bandeja de entrada si tu cuenta está asociada."}


@router.post("/restablecer")
def restablecer_password_endpoint(
    body: RestablecerRequest,
    db: Session = Depends(get_db),
):
    """Restablece la contraseña usando un token de recuperación."""
    ok = restablecer_password(db, body.token, body.password)
    if not ok:
        raise HTTPException(status_code=400, detail="Token no existe")
    return {"message": "Contraseña restablecida correctamente."}