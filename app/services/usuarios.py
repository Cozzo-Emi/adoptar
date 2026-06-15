from sqlalchemy.orm import Session
from app.models.usuario import Usuario, UserRole
from app.models.solicitud import Solicitud
from app.models.recuperacion_password import RecuperacionPassword


def get_all_users(db: Session) -> list[Usuario]:
    """Devuelve todos los usuarios (admin)."""
    return db.query(Usuario).all()


def cambiar_rol(db: Session, user_id: int, nuevo_rol: UserRole) -> Usuario | None:
    """Cambia el rol de un usuario. Retorna None si no existe."""
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None
    user.rol = nuevo_rol
    db.commit()
    db.refresh(user)
    return user


def delete_usuario(db: Session, user_id: int) -> Usuario | None:
    """Elimina un usuario físicamente. Retorna None si no existe."""
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        return None
    db.query(Solicitud).filter(Solicitud.id_usuario == user_id).delete()
    db.query(RecuperacionPassword).filter(
        RecuperacionPassword.usuario_id == user_id
    ).delete()
    db.delete(user)
    db.commit()
    return user
