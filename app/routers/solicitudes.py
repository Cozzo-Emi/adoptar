from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.usuario import Usuario
from app.models.animal import Animal

from app.schemas.solicitud import SolicitudCreate, SolicitudResponse, SolicitudUpdate

from app.services.solicitudes import (
    create_solicitud,
    get_all_solicitudes,
    get_solicitudes_by_user,
    get_solicitud_by_id,
    update_solicitud_estado
)

from app.core.dependencies import get_current_user, solo_admin


router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("/", response_model=SolicitudResponse, status_code=status.HTTP_201_CREATED)
def crear_solicitud(
    data: SolicitudCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Crea una solicitud de adopción (adoptante)."""

    animal = db.query(Animal).filter(Animal.id == data.id_animal).first()

    if not animal or not animal.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado"
        )

    try:
        return create_solicitud(db, current_user.id, animal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SolicitudResponse])
def listar_solicitudes(
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Devuelve todas las solicitudes (admin)."""
    return get_all_solicitudes(db)


@router.get("/mias", response_model=list[SolicitudResponse])
def mis_solicitudes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Devuelve las solicitudes del usuario autenticado."""
    return get_solicitudes_by_user(db, current_user.id)


@router.put("/{solicitud_id}", response_model=SolicitudResponse)
def actualizar_estado_solicitud(
    solicitud_id: int,
    data: SolicitudUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Aprueba o rechaza una solicitud (admin)."""

    solicitud = get_solicitud_by_id(db, solicitud_id)

    if not solicitud:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitud no encontrada"
        )

    try:
        return update_solicitud_estado(db, solicitud, data.estado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))