from sqlalchemy.orm import Session, selectinload

from app.models.solicitud import Solicitud, RequestStatus
from app.models.animal import Animal, AnimalStatus


def create_solicitud(db: Session, user_id: int, animal: Animal) -> Solicitud:
    """Crea una solicitud si el animal está disponible y sin conflictos."""

    if animal.estado != AnimalStatus.disponible:
        raise ValueError("El animal no está disponible")

    duplicate = db.query(Solicitud).filter(
        Solicitud.id_usuario == user_id,
        Solicitud.id_animal == animal.id
    ).first()

    if duplicate:
        raise ValueError("Ya enviaste una solicitud para este animal")

    existing = db.query(Solicitud).filter(
        Solicitud.id_animal == animal.id,
        Solicitud.estado == RequestStatus.pendiente
    ).first()

    if existing:
        raise ValueError("Ya existe una solicitud pendiente para este animal")

    solicitud = Solicitud(
        id_usuario=user_id,
        id_animal=animal.id,
        estado=RequestStatus.pendiente
    )

    db.add(solicitud)
    db.commit()
    db.refresh(solicitud)

    return solicitud


def _base_query(db: Session):
    return db.query(Solicitud).options(
        selectinload(Solicitud.usuario),
        selectinload(Solicitud.animal),
    )


def get_solicitudes_by_user(db: Session, user_id: int) -> list[Solicitud]:
    """Devuelve las solicitudes de un usuario."""
    return _base_query(db).filter(Solicitud.id_usuario == user_id).all()


def get_all_solicitudes(db: Session) -> list[Solicitud]:
    """Devuelve todas las solicitudes (admin)."""
    return _base_query(db).all()


def get_solicitud_by_id(db: Session, solicitud_id: int) -> Solicitud | None:
    """Busca una solicitud por ID."""
    return _base_query(db).filter(Solicitud.id == solicitud_id).first()


def update_solicitud_estado(
    db: Session,
    solicitud: Solicitud,
    new_status: RequestStatus
) -> Solicitud:
    """Actualiza el estado y, si se aprueba, marca el animal como adoptado."""

    if solicitud.estado != RequestStatus.pendiente:
        raise ValueError("Solo se pueden modificar solicitudes pendientes")

    solicitud.estado = new_status

    if new_status == RequestStatus.aprobada:
        animal = db.query(Animal).filter(Animal.id == solicitud.id_animal).first()
        if animal:
            animal.estado = AnimalStatus.adoptado

    db.commit()
    db.refresh(solicitud)

    return solicitud