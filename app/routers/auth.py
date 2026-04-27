from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario, UserRole
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UsuarioResponse)
def register(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario como adoptante."""
    
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")

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