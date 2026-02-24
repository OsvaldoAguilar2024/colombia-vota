# 🗳️ Colombia Vota — Sistema de Gestión Electoral

Sistema web Django para gestionar **votantes, candidatos, puestos, mesas y encuestas** electorales de Colombia.

---

## 🚀 Deploy en Railway (10 minutos, GRATIS para demo)

### Paso 1 — Subir a GitHub
```bash
git init
git add .
git commit -m "feat: Colombia Vota sistema electoral"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/colombia-vota.git
git push -u origin main
```

### Paso 2 — Crear proyecto en Railway
1. Ve a **[railway.app](https://railway.app)** → Login con GitHub
2. Clic **"New Project"** → **"Deploy from GitHub repo"**
3. Selecciona tu repositorio `colombia-vota`
4. Railway detecta Django automáticamente ✅

### Paso 3 — Agregar base de datos PostgreSQL
1. En tu proyecto Railway → **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway inyecta `DATABASE_URL` automáticamente 🎉

### Paso 4 — Configurar variables de entorno
En Railway → tu servicio Django → pestaña **"Variables"**, agrega:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | Una clave larga aleatoria (genera en [djecrety.ir](https://djecrety.ir)) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `tuapp.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://tuapp.up.railway.app` |
| `DJANGO_SUPERUSER_USERNAME` | `admin` |
| `DJANGO_SUPERUSER_PASSWORD` | Tu contraseña segura |
| `DJANGO_SUPERUSER_EMAIL` | `tu@email.com` |

### Paso 5 — Crear administrador
En Railway → tu servicio → **"Settings"** → sección **"Deploy"** → cambia el Start Command temporalmente a:
```
python manage.py migrate && python manage.py cargar_datos_colombia && python manage.py crear_superusuario && python manage.py collectstatic --noinput && gunicorn config.wsgi --bind [::]:$PORT
```
Luego redeploy. Después de que corra, quita `crear_superusuario` del comando (ya no es necesario).

### Paso 6 — Generar dominio público
Railway → tu servicio → **"Settings"** → **"Networking"** → **"Generate Domain"**

¡Tu app estará en `https://tuapp.up.railway.app`! 🚀

---

## 💻 Instalación Local

```bash
# 1. Clonar
git clone https://github.com/TU_USUARIO/colombia-vota.git
cd colombia-vota

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate      # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Migraciones y datos iniciales
python manage.py migrate
python manage.py cargar_datos_colombia

# 5. Crear administrador
python manage.py createsuperuser

# 6. Arrancar
python manage.py runserver
```

Accede en: **http://127.0.0.1:8000**

---

## 🌐 Módulos del sistema

| Módulo | URL | Descripción |
|--------|-----|-------------|
| Dashboard | `/` | Estadísticas generales |
| Encuestador | `/encuestador/` | Registrar intención de voto |
| Estadísticas | `/encuestador/estadisticas/` | Resultados con drill-down |
| Votantes | `/votantes/` | CRUD de votantes |
| Candidatos | `/candidatos/` | CRUD de candidatos |
| Eventos | `/eventos/` | Presidencia, Congreso, Alcaldías, etc. |
| Partidos | `/partidos/` | Partidos políticos |
| Puestos/Mesas | `/puestos/` `/mesas/` | Infraestructura electoral |
| Consulta pública | `/consulta/` | Ciudadanos consultan su mesa (sin login) |
| Admin Django | `/admin/` | Panel de administración completo |

---

## ⚙️ Variables de entorno

Crea `.env` para desarrollo local (no lo subas a GitHub):
```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

---

## 💰 Costo en Railway

- **Trial gratuito**: $5 USD de créditos por 30 días (más que suficiente para un demo)
- **Plan Hobby**: $5 USD/mes (incluye $5 de créditos = prácticamente gratis para apps pequeñas)
- Tu URL quedará como: `https://colombia-vota-production.up.railway.app`
