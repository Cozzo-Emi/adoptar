from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db

from app.models.usuario import Usuario
from app.models.animal import Animal

from app.schemas.animal import (
    AnimalCreate,
    AnimalResponse,
    AnimalUpdate
)

from app.services.animales import (
    create_animal,
    get_animals,
    get_animal_by_id,
    update_animal,
    delete_animal
)

from app.services.cloudinary_service import upload_image
from app.core.dependencies import solo_admin


router = APIRouter(prefix="/animals", tags=["Animals"])


@router.get("/", response_model=list[AnimalResponse])
def list_animals(db: Session = Depends(get_db)):
    """Obtiene todos los animales activos."""
    return get_animals(db)


@router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    """Obtiene un animal por ID."""
    animal = get_animal_by_id(db, animal_id)

    if not animal or not animal.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado"
        )

    return animal


@router.post("/", response_model=AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal_endpoint(
    nombre: str = Form(...),
    especie: str = Form(...),
    raza: Optional[str] = Form(None),
    edad: Optional[int] = Form(None),
    descripcion: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Crea un animal con imagen opcional (admin)."""

    image_url: Optional[str] = None

    if imagen:
        try:
            image_url = upload_image(imagen)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    animal_data = AnimalCreate(
        nombre=nombre,
        especie=especie,
        raza=raza,
        edad=edad,
        descripcion=descripcion,
        imagen=image_url
    )

    return create_animal(db, animal_data)


@router.patch("/{animal_id}", response_model=AnimalResponse)
def update_animal_endpoint(
    animal_id: int,
    data: AnimalUpdate,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Actualiza un animal existente (admin)."""
    animal = get_animal_by_id(db, animal_id)

    if not animal or not animal.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado"
        )

    return update_animal(db, animal, data)


@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal_endpoint(
    animal_id: int,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Realiza un borrado lógico de un animal (admin)."""
    animal = get_animal_by_id(db, animal_id)

    if not animal or not animal.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado"
        )

    delete_animal(db, animal)

    return None