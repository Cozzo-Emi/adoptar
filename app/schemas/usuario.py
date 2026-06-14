from pydantic import BaseModel, EmailStr, ConfigDict, Field
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

class CambiarRolRequest(BaseModel):
    rol: UserRole


class RecuperarRequest(BaseModel):
    email: EmailStr


class RestablecerRequest(BaseModel):
    token: str
    password: str = Field(min_length=8)


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rol: UserRole
    created_at: datetime
    updated_at: Optional[datetime] = None