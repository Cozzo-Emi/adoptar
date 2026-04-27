from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

from app.models.usuario import UserRole


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rol: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None