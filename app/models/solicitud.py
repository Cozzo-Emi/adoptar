from datetime import datetime, timezone
import enum
from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class RequestStatus(str, enum.Enum):
    pendiente = "pendiente"
    aprobada = "aprobada"
    rechazada = "rechazada"


class Solicitud(Base):
    __tablename__ = "solicitud"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    estado: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, name="request_status")
    )
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    id_animal: Mapped[int] = mapped_column(ForeignKey("animal.id"))
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=lambda: datetime.now(timezone.utc)
    )
    usuario = relationship("Usuario", back_populates="solicitudes")
    animal = relationship("Animal", back_populates="solicitudes")

    __table_args__ = (
        UniqueConstraint("id_usuario", "id_animal", name="uq_usuario_animal"),
    )