from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.solicitud import RequestStatus

class SolicitudCreate(BaseModel):
    id_animal: int

class SolicitudUpdate(BaseModel):
    estado: RequestStatus

class SolicitudResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    estado: RequestStatus
    id_usuario: int
    id_animal: int
    created_at: datetime
    updated_at: datetime | None = None