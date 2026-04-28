from fastapi import FastAPI
from app.routers import auth, animales
from app.database import Base, engine

# Crear tablas (solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AdoptAR API",
    description="API para gestión de adopción de mascotas",
    version="1.0.0"
)

# Routers
app.include_router(auth.router)
app.include_router(animales.router)
@app.get("/", tags=["Root"])
def root():
    """Endpoint base para verificar que la API está funcionando."""
    return {"message": "AdoptAR API running 🚀"}