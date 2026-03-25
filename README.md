# Peluquería Agenda — Sistema de Gestión

Sistema web para gestionar citas, clientes y estilistas de una peluquería.  
Desarrollado con Django 4.x + Django REST Framework + PostgreSQL (Supabase) + Bootstrap 5.

**SENA — Análisis y Desarrollo de Software (228185) — Grupo 9**  
Integrantes: Martinez Escobar Juan Angel · Castañeda Portela Juan José · Munar Trujillo Farid

---

## Tecnologías

- Python 3.10+
- Django 4.2
- Django REST Framework 3.14
- PostgreSQL (Supabase)
- Bootstrap 5.3 + Bootstrap Icons
- python-decouple (variables de entorno)

---

## Requisitos previos

- Python 3.10 o superior instalado
- Una base de datos PostgreSQL en [Supabase](https://supabase.com) (o local)
- Git

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd peluqueria_agenda
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y completa los valores:

```bash
cp .env.example .env
```

Edita `.env` con tus datos:

```env
SECRET_KEY=una-clave-secreta-larga-y-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Datos de tu base de datos en Supabase
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=tu-password-de-supabase
DB_HOST=db.xxxxxxxxxxxx.supabase.co
DB_PORT=5432
```

> ⚠️ El archivo `.env` **nunca** debe subirse a GitHub. Ya está en `.gitignore`.

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional, para el admin)

```bash
python manage.py createsuperuser
```

### 7. Correr el servidor

```bash
python manage.py runserver
```

Abre el navegador en: [http://localhost:8000](http://localhost:8000)

---

## Estructura del proyecto

```
peluqueria_agenda/
├── agenda/
│   ├── models.py          # Modelos: Cliente, Estilista, Servicio, Cita
│   ├── serializers.py     # Serializers DRF con validaciones personalizadas
│   ├── views.py           # ViewSets API + Vistas HTML
│   ├── urls.py            # Rutas API y HTML
│   ├── forms.py           # Formularios Django
│   └── templates/agenda/  # Templates HTML con Bootstrap
├── peluqueria_agenda/
│   ├── settings.py        # Configuración del proyecto
│   └── urls.py
├── .env.example           # Plantilla de variables de entorno
├── requirements.txt
└── README.md
```

---

## API REST — Endpoints

Base URL: `http://localhost:8000/api/`

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/registro/` | Registrar usuario y obtener token | No |
| POST | `/api/auth/login/` | Login y obtener token | No |
| POST | `/api/auth/logout/` | Cerrar sesión (elimina token) | Sí |

**Registro:**
```json
POST /api/auth/registro/
{
  "username": "admin",
  "password": "mipassword123"
}
```

**Login:**
```json
POST /api/auth/login/
{
  "username": "admin",
  "password": "mipassword123"
}
// Respuesta: { "token": "abc123..." }
```

**Usar el token en peticiones protegidas:**
```
Authorization: Token abc123...
```

### Recursos

| Método | Endpoint | Descripción | Auth requerida |
|--------|----------|-------------|----------------|
| GET | `/api/clientes/` | Listar clientes | No |
| POST | `/api/clientes/` | Crear cliente | Sí |
| GET | `/api/clientes/{id}/` | Ver cliente | No |
| PUT/PATCH | `/api/clientes/{id}/` | Editar cliente | Sí |
| DELETE | `/api/clientes/{id}/` | Eliminar cliente | Sí |
| GET | `/api/estilistas/` | Listar estilistas | No |
| POST | `/api/estilistas/` | Crear estilista | Sí |
| GET | `/api/citas/` | Listar citas | Sí |
| POST | `/api/citas/` | Crear cita | Sí |
| PUT/PATCH | `/api/citas/{id}/` | Editar cita | Sí |
| DELETE | `/api/citas/{id}/` | Eliminar cita | Sí |
| GET | `/api/servicios/` | Listar servicios | No |

---

## Vistas HTML

| URL | Vista |
|-----|-------|
| `/` | Dashboard con citas próximas y estadísticas |
| `/clientes/` | Lista de clientes |
| `/clientes/nuevo/` | Crear cliente |
| `/estilistas/` | Lista de estilistas |
| `/estilistas/nuevo/` | Crear estilista |
| `/citas/nueva/` | Crear cita |

---

## Modelos

### Cliente
- `nombre`, `email` (único), `telefono`
- Propiedad `total_visitas`: cuenta citas completadas
- Clientes con más de 10 visitas obtienen 10% de descuento automático

### Estilista
- `nombre`, `especialidad`, `telefono`

### Servicio
- `nombre`, `duracion_minutos`, `precio_base`

### Cita
- Relaciona `Cliente`, `Estilista` y `Servicio`
- `fecha_hora_inicio`, `fecha_hora_fin`
- `estado`: pendiente / completada / cancelada
- `precio_final` y `descuento_aplicado` se calculan automáticamente al completar

---

## Reglas de negocio

1. **Sin solapamiento de citas**: No se pueden agendar dos citas al mismo tiempo para el mismo estilista. Validado en el serializer y en el formulario.

2. **Descuento por fidelidad**: Al completar una cita, si el cliente tiene más de 10 visitas completadas, se aplica automáticamente un 10% de descuento sobre el precio del servicio.

---

## Validaciones personalizadas (Serializers)

- `validate_email` en `ClienteSerializer`: verifica que el email no esté duplicado.
- `validate_telefono` en `EstilistaSerializer`: verifica que el teléfono tenga entre 7 y 15 dígitos numéricos.
- `validate` en `CitaSerializer`: verifica que el estilista no tenga otra cita en el mismo horario.

---

## Correr los tests

```bash
pytest
```

Los tests usan SQLite automáticamente (variable `TESTING=True` en pytest.ini).
