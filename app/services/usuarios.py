from sqlalchemy.orm import Session
from app.models.usuario import Usuario, UserRole


def cambiar_rol(db: Session, user_id: int, nuevo_rol: UserRole) -> Usuario | None:
    """Cambia el rol de un usuario. Retorna None si no existe."""
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None
    user.rol = nuevo_rol
    db.commit()
    db.refresh(user)
    return user
