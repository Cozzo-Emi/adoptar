from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, CambiarRolRequest
from app.services.usuarios import cambiar_rol
from app.core.deps import solo_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


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
