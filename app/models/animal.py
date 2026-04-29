from datetime import datetime, timezone
import enum
from sqlalchemy import String, Integer, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class AnimalStatus(str, enum.Enum):
    disponible = "disponible"
    en_proceso = "en_proceso"
    adoptado = "adoptado"


class Animal(Base):
    __tablename__ = "animal"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    especie: Mapped[str] = mapped_column(String(100))
    raza: Mapped[str | None] = mapped_column(String(100))
    edad: Mapped[int | None] = mapped_column(Integer)
    descripcion: Mapped[str | None] = mapped_column(String(500))
    imagen: Mapped[str | None] = mapped_column(String(500))
    estado: Mapped[AnimalStatus] = mapped_column(
        Enum(AnimalStatus, name="animal_status"),
        default=AnimalStatus.disponible
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        onupdate=lambda: datetime.now(timezone.utc)
    )
    solicitudes = relationship("Solicitud", back_populates="animal")