# 🐾 AdoptAR

**API REST para gestión de adopción de mascotas**

AdoptAR conecta refugios y rescatistas con personas interesadas en adoptar mascotas. Centraliza la publicación de animales disponibles y el seguimiento de solicitudes de adopción, reemplazando la gestión dispersa en redes sociales y canales informales.

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Base de datos | PostgreSQL |
| Autenticación | JWT (python-jose) |
| Archivos | Cloudinary |
| Documentación | Swagger UI (automático) |

---

## Estructura del proyecto

```
AdoptAR/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada, instancia FastAPI
│   ├── database.py          # Conexión a PostgreSQL
│   │
│   ├── core/                # Configuración centralizada
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de entorno (pydantic-settings)
│   │   ├── security.py      # (hash, verify, token)
│   │   └── deps.py          # Dependencies 
│   │
│   ├── models/              # Tablas de la base de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── animal.py
│   │   └── solicitud.py
│   │
│   ├── schemas/             # Validación de datos entrada/salida (Pydantic)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── animal.py
│   │   └── solicitud.py
│   │
│   ├── routers/             # Endpoints  por módulo
│   │   ├── __init__.py
│   │   ├── auth.py          
│   │   ├── animales.py     
│   │   └── solicitudes.py  
│   │
│   └── services/            # Lógica de negocio
│       ├── __init__.py
│       ├── animales.py      
│       ├── solicitudes.py  
│       └── cloudinary_service.py 
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          #  pytest 
│   ├── test_auth.py
│   ├── test_animales.py
│   └── test_solicitudes.py
│
├── venv/                    
├── .env                     
├── pytest.ini
├── requirements.txt
└── README.md

```

---

## Modelo de datos

### Usuario
| Campo | Tipo | Restricción |
|---|---|---|
| id | SERIAL | PK |
| nombre | VARCHAR(100) | |
| email | VARCHAR(100) | UNIQUE |
| telefono | VARCHAR(20) | |
| contraseña | TEXT | hash bcrypt |
| rol | ENUM | `admin`, `adoptante` |

### Animal
| Campo | Tipo | Restricción |
|---|---|---|
| id | SERIAL | PK |
| nombre | VARCHAR(100) | |
| especie | VARCHAR(100) | |
| raza | VARCHAR(100) | NULL |
| edad | INTEGER | |
| descripcion | VARCHAR(500) | NULL |
| imagen | VARCHAR(500) | NULL |
| estado | ENUM | `disponible`, `en_proceso`, `adoptado`, `inactivo` |

### Solicitud
| Campo | Tipo | Restricción |
|---|---|---|
| id | SERIAL | PK |
| estado | ENUM | `pendiente`, `aprobada`, `rechazada` |
| fecha | TIMESTAMP | |
| id_usuario | INTEGER | FK → usuario.id |
| id_animal | INTEGER | FK → animal.id |

> Un mismo usuario no puede tener dos solicitudes activas para el mismo animal: `UNIQUE(id_usuario, id_animal)`

---

## Endpoints

### Autenticación
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/auth/registro` | Público | Crea una cuenta nueva |
| POST | `/auth/login` | Público | Inicia sesión, devuelve token JWT |

### Animales
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| GET | `/animales` | Público | Lista todos los animales disponibles |
| GET | `/animales/{id}` | Público | Detalle de un animal específico |
| POST | `/animales` | Admin | Crea un animal nuevo |
| PUT | `/animales/{id}` | Admin | Modifica un animal existente |
| DELETE | `/animales/{id}` | Admin | Baja lógica de un animal |

### Solicitudes
| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/solicitudes` | Adoptante | Envía una solicitud de adopción |
| GET | `/solicitudes` | Admin | Lista todas las solicitudes |
| GET | `/solicitudes/mias` | Adoptante | Lista las solicitudes del usuario autenticado |
| PUT | `/solicitudes/{id}` | Admin | Aprueba o rechaza una solicitud |



## Autor

**Emiliano Cozzolino**
Tecnicatura Superior en Desarrollo de Software — Cursada de Backend 2026
