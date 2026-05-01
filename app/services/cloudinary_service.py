import cloudinary
import cloudinary.uploader

from fastapi import UploadFile

from app.core.config import settings


# Configuración de Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


def upload_image(file: UploadFile) -> str:
    """
    Sube una imagen a Cloudinary y devuelve la URL pública.
    """

    result = cloudinary.uploader.upload(file.file)
    return result["secure_url"]