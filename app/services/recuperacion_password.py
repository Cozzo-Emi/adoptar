import secrets
import hashlib
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.models.recuperacion_password import RecuperacionPassword
from app.core.security import hash_password

TOKEN_EXPIRE_MINUTES = 30


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _is_expired(expires_at: datetime) -> bool:
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at < datetime.now(timezone.utc)


def solicitar_recuperacion(db: Session, email: str) -> str | None:
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return None

    anterior = db.query(RecuperacionPassword).filter(
        RecuperacionPassword.usuario_id == usuario.id
    ).first()
    if anterior:
        db.delete(anterior)
        db.flush()

    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)

    recuperacion = RecuperacionPassword(
        usuario_id=usuario.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
    )
    db.add(recuperacion)
    db.commit()

    return token


def restablecer_password(db: Session, token: str, nueva_password: str) -> bool:
    token_hash = _hash_token(token)

    recuperacion = db.query(RecuperacionPassword).filter(
        RecuperacionPassword.token_hash == token_hash
    ).first()

    if not recuperacion or _is_expired(recuperacion.expires_at):
        return False

    usuario = recuperacion.usuario
    usuario.password_hash = hash_password(nueva_password)
    db.delete(recuperacion)
    db.commit()

    return True
