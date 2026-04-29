from sqlalchemy.orm import Session
from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate


def create_animal(db: Session, data: AnimalCreate) -> Animal:
    """Crea un nuevo animal en estado disponible."""
    animal = Animal(**data.model_dump())
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


def get_animals(db: Session) -> list[Animal]:
    """Obtiene todos los animales activos."""
    return db.query(Animal).filter(Animal.is_active.is_(True)).all()


def get_animal_by_id(db: Session, animal_id: int) -> Animal | None:
    """Busca un animal por su ID."""
    return db.query(Animal).filter(Animal.id == animal_id).first()


def update_animal(db: Session, animal: Animal, data: AnimalUpdate) -> Animal:
    """Actualiza campos de un animal. Solo modifica los campos enviados en el payload."""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(animal, field, value)
    db.commit()
    db.refresh(animal)
    return animal


def delete_animal(db: Session, animal: Animal) -> None:
    """ desactiva el animal sin eliminarlo de la base de datos."""
    animal.is_active = False
    db.commit()