from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, animales, solicitudes


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AdoptAR API",
    description="API para gestión de adopción de mascotas",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(animales.router)
app.include_router(solicitudes.router)


@app.get("/", tags=["Root"])
def root():
    """Endpoint base para verificar que la API está funcionando."""
    return {"message": "AdoptAR API running 🚀"}