import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


HTTP_ERROR_TYPES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    409: "conflict",
    422: "validation_error",
}


def build_error_response(
    error_type: str,
    message: str,
    details: Any = None,
) -> dict:
    """Construye una respuesta de error consistente."""

    return {
        "error": {
            "type": error_type,
            "message": message,
            "details": details,
        },
    }


async def handle_integrity_error(
    request: Request,
    exc: IntegrityError,
):
    """Maneja errores de integridad de base de datos."""

    logger.warning(
        "IntegrityError en %s %s: %s",
        request.method,
        request.url.path,
        exc.orig,
    )

    try:
        constraint_name = exc.orig.diag.constraint_name
    except AttributeError:
        constraint_name = None

    if constraint_name is None:
        orig_msg = str(exc.orig).lower()
        if "email" in orig_msg:
            constraint_name = "ix_usuario_email"

    if constraint_name == "ix_usuario_email":
        message = "Email ya registrado"
    else:
        message = "El recurso ya existe o viola una restricción de integridad."

    return JSONResponse(
        status_code=409,
        content=build_error_response(
            error_type="duplicate_resource",
            message=message,
        ),
    )


async def handle_value_error(
    request: Request,
    exc: ValueError,
):
    """Maneja errores de lógica de negocio."""
    return JSONResponse(
        status_code=400,
        content=build_error_response(
            error_type="bad_request",
            message=str(exc),
        ),
    )


async def handle_http_exception(
    request: Request,
    exc: HTTPException,
):
    """Maneja excepciones HTTP controladas."""

    if exc.status_code not in HTTP_ERROR_TYPES:
        logger.warning(
            "HTTPException con status code no mapeado: %s en %s %s",
            exc.status_code,
            request.method,
            request.url.path,
        )

    error_type = HTTP_ERROR_TYPES.get(
        exc.status_code,
        "http_error",
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(
            error_type=error_type,
            message=str(exc.detail),
        ),
    )


async def handle_validation_error(
    request: Request,
    exc: RequestValidationError,
):
    """Maneja errores de validación de FastAPI/Pydantic."""

    details = [
        {
            "field": ".".join(
                str(item)
                for item in error["loc"]
                if item != "body"
            ),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=build_error_response(
            error_type="validation_error",
            message="Datos inválidos.",
            details=details,
        ),
    )


async def handle_generic_exception(
    request: Request,
    exc: Exception,
):
    """Maneja errores inesperados."""

    logger.exception(
        "Error inesperado en %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content=build_error_response(
            error_type="internal_server_error",
            message="Ocurrió un error interno del servidor.",
        ),
    )


def register_error_handlers(app: FastAPI):
    """Registra todos los handlers globales de errores."""

    app.add_exception_handler(
        IntegrityError,
        handle_integrity_error,
    )

    app.add_exception_handler(
        HTTPException,
        handle_http_exception,
    )

    app.add_exception_handler(
        RequestValidationError,
        handle_validation_error,
    )

    app.add_exception_handler(
        ValueError,
        handle_value_error,
    )

    app.add_exception_handler(
        Exception,
        handle_generic_exception,
    )

