from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from app.models.animal import AnimalStatus


class AnimalBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(BaseModel):
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    edad: Optional[int] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    estado: Optional[AnimalStatus] = None
    is_active: Optional[bool] = None


class AnimalResponse(AnimalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estado: AnimalStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None