from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, CambiarRolRequest
from app.services.usuarios import get_all_users, cambiar_rol, delete_usuario
from app.core.deps import solo_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioResponse])
def list_usuarios(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin),
):
    """Devuelve todos los usuarios (admin)."""
    return get_all_users(db)


@router.patch("/{user_id}/rol", response_model=UsuarioResponse)
def change_user_role(
    user_id: int,
    body: CambiarRolRequest,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin),
):
    """Cambia el rol de un usuario (admin)."""
    user = cambiar_rol(db, user_id, body.rol)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin),
):
    """Elimina un usuario físicamente (admin)."""
    user = delete_usuario(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return None
