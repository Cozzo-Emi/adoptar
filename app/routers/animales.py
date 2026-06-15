from fastapi import APIRouter, Depends, HTTPException, Query, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional
from math import ceil

from app.database import get_db

from app.models.usuario import Usuario
from app.models.animal import Animal

from app.schemas.animal import (
    AnimalCreate,
    AnimalResponse,
    AnimalUpdate
)
from app.schemas.pagination import PaginatedResponse, PaginationMeta

from app.services.animales import (
    create_animal,
    get_animals,
    get_animal_by_id,
    update_animal,
    delete_animal
)

from app.services.cloudinary_service import upload_image
from app.core.deps import solo_admin


router = APIRouter(prefix="/animals", tags=["Animals"])


@router.get("/", response_model=PaginatedResponse[AnimalResponse])
def list_animals(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    especie: str | None = Query(None),
    estado: str | None = Query(None),
    nombre: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Obtiene animales activos con paginación y filtros opcionales."""
    data = get_animals(
        db,
        page=page,
        size=size,
        especie=especie,
        estado=estado,
        nombre=nombre,
    )
    return PaginatedResponse(
        items=data["items"],
        pagination=PaginationMeta(
            page=page,
            size=size,
            total=data["total"],
            pages=ceil(data["total"] / size) if data["total"] > 0 else 0,
        ),
    )


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
        image_url = upload_image(imagen)

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
    nombre: Optional[str] = Form(None),
    especie: Optional[str] = Form(None),
    raza: Optional[str] = Form(None),
    edad: Optional[int] = Form(None),
    descripcion: Optional[str] = Form(None),
    imagen: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin: Usuario = Depends(solo_admin)
):
    """Actualiza un animal existente (admin). Acepta imagen opcional."""
    animal = get_animal_by_id(db, animal_id)

    if not animal or not animal.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal no encontrado"
        )

    update_data = AnimalUpdate()
    if nombre is not None:
        update_data.nombre = nombre
    if especie is not None:
        update_data.especie = especie
    if raza is not None:
        update_data.raza = raza
    if edad is not None:
        update_data.edad = edad
    if descripcion is not None:
        update_data.descripcion = descripcion
    if imagen:
        update_data.imagen = upload_image(imagen)

    return update_animal(db, animal, update_data)


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