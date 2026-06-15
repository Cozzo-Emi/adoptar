from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.animal import Animal, AnimalStatus
from app.models.solicitud import Solicitud, RequestStatus
from app.models.usuario import Usuario

router = APIRouter(tags=["Stats"])


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    disponibles = db.query(Animal).filter(
        Animal.estado == AnimalStatus.disponible,
        Animal.is_active.is_(True),
    ).count()

    adoptados = db.query(Animal).filter(
        Animal.estado == AnimalStatus.adoptado,
    ).count()

    procesadas = db.query(Solicitud).filter(
        Solicitud.estado.in_([RequestStatus.aprobada, RequestStatus.rechazada]),
    ).count()

    total_animales = db.query(Animal).filter(
        Animal.is_active.is_(True)
    ).count()

    total_usuarios = db.query(Usuario).count()

    return {
        "disponibles": disponibles,
        "adoptados": adoptados,
        "procesadas": procesadas,
        "total_animales": total_animales,
        "total_usuarios": total_usuarios,
    }