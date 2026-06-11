from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.core.error_handlers import register_error_handlers

from app.routers import auth
from app.routers import animales
from app.routers import solicitudes
from app.routers.stats import router as stats_router


app = FastAPI(
    title="AdoptAR API",
    description="API para la gestión de adopción de mascotas",
    version="1.0.0",
)





# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handlers globales
register_error_handlers(app)


# Routers
app.include_router(auth.router)
app.include_router(animales.router)
app.include_router(solicitudes.router)
app.include_router(stats_router)


@app.get("/", tags=["Root"])
def root():
    """Verifica que la API esté funcionando."""

    return {
        "message": "AdoptAR API running "
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check de la aplicación."""

    return {
        "status": "ok"
    }

