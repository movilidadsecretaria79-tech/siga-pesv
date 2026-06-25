# SIGA-PESV
Sistema Integral de Gestión de Auditorías PESV
**Alcaldía de Villavicencio — Secretaría de Movilidad — Dirección de Planeación y Prospectiva**

Aplicativo web para planear y ejecutar las auditorías/verificaciones del Plan
Estratégico de Seguridad Vial (PESV) a las empresas obligadas del municipio,
conforme a la metodología de la **Resolución 40595 de 2022** del Ministerio
de Transporte (24 pasos del PESV).

---

## 1. Qué incluye el aplicativo

| Módulo | Para qué sirve |
|---|---|
| **Programa anual de verificación** | Crear el programa anual, el cronograma de visitas, seleccionar empresas, criterios de evaluación (pasos/componentes del PESV), equipo auditor e instrumentos de inspección. |
| **Empresas** | Ficha completa de cada empresa/organización auditada: datos generales, nivel PESV (Básico/Estándar/Avanzado), líder del PESV, vehículos y conductores. |
| **Catálogo PESV** | Los 24 pasos oficiales (4 fases PHVA) y los 28 componentes verificables en los que se apoyan el programa anual y las auditorías. Editable desde el panel de administración. |
| **Verificación de requisitos** | Por cada empresa y cada componente del PESV: cargar la **documentación soporte** vigente (PESV, política, designación de líder, comité, diagnóstico, matrices, procedimientos, etc.) y la **evidencia de ejecución** (documentos y/o fotografías) que demuestre su implementación real. |
| **Gestión de conductores** | Por cada conductor de cada empresa: licencia de conducción, examen médico ocupacional, verificación de comparendos, evaluación de competencias para movilidad segura, control de jornada/fatiga y seguimiento a reincidentes — con alertas automáticas de vencimiento. |
| **Vehículos** | Placa, propiedad, SOAT y revisión técnico-mecánica con alertas de vencimiento. |
| **Auditorías** | Ejecución de la visita: lista de verificación (checklist) por componente, registro de **conformidades, no conformidades, observaciones y recomendaciones**, y **plan de mejoramiento** con responsable y fecha de cumplimiento. |
| **Informe de auditoría (PDF)** | Genera automáticamente el informe descargable en PDF con empresa, fecha, duración, equipo auditor, pasos auditados, hallazgos y plan de mejoramiento. |
| **Matriz de seguimiento** | Tablero con todas las auditorías y todas las acciones del plan de mejoramiento, con alertas de vencimiento y exportación a Excel. |
| **Panel de control (Inicio)** | KPIs: empresas activas, auditorías en proceso/cerradas, no conformidades abiertas, acciones vencidas, vehículos con SOAT/RTM vencido, conductores con alertas, próximas visitas programadas. |

El catálogo de los 24 pasos se cargó con los nombres oficiales de la
Resolución 40595 de 2022 (verificados en línea al construir el sistema). El
listado completo de **componentes verificables** (la "Verificación de
requisitos") se construyó a partir de los puntos que usted describió
(PESV vigente, política, líder, comité, diagnóstico, objetivos, programas de
riesgo crítico, plan anual de trabajo, competencias, emergencias viales,
investigación de siniestros, desplazamientos laborales, inspección y
mantenimiento de vehículos, indicadores, estadística de siniestros,
auditorías previas, gestión de contratistas y actualización del PESV), y se
completó con los pasos que la norma exige pero usted no detalló explícitamente
(archivo y retención documental, mecanismos de comunicación y participación,
responsabilidad y comportamiento seguro, vías seguras) para dejar **cubiertos
los 24 pasos**. Todo esto se puede ajustar libremente desde el panel de
administración (`/admin/`) sin tocar código.

> **Pendiente de su parte:** me indicó que subiría el logo de la Secretaría y
> la rúbrica de evaluación, pero los archivos no llegaron a guardarse en esta
> sesión (la carpeta de subida quedó vacía). Cuando los tenga a mano:
> - **Logo:** colóquelo en `static/img/logo_secretaria_movilidad.png`
>   (cualquier imagen PNG con fondo transparente se ve bien en la barra
>   superior y en el login). Si no hay archivo, el sistema simplemente
>   oculta el espacio del logo y muestra el nombre del sistema en texto.
> - **Rúbrica:** envíemela en cualquier momento y ajusto los componentes,
>   preguntas de verificación o calificaciones del catálogo PESV para que
>   coincidan exactamente con ella.

---

## 2. Ejecutar el aplicativo en su computador (local)

Requisitos: Python 3.11 o superior.

```bash
# 1. Crear entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la base de datos (SQLite, no requiere instalar nada adicional)
python manage.py migrate

# 4. Cargar el catálogo oficial de los 24 pasos del PESV y sus componentes
python manage.py cargar_catalogo_pesv

# 5. Crear el usuario administrador
python manage.py createsuperuser

# 6. Iniciar el servidor local
python manage.py runserver
```

Abra su navegador en **http://127.0.0.1:8000/** e ingrese con el usuario
administrador que creó en el paso 5.

El archivo de base de datos queda en `db.sqlite3` y los documentos/fotos
cargados en la carpeta `media/`. Para "reiniciar" el aplicativo basta con
borrar `db.sqlite3` (y `media/` si quiere borrar también los archivos) y
repetir los pasos 3 a 5.

### Crear más usuarios (auditores)
Ingrese a `/admin/` con el usuario administrador → **Usuarios** → *Añadir
usuario*. Asigne el **rol** "Auditor / Verificador" o "Líder de equipo
auditor". Marque "Acceso al sitio de administración" (`is_staff`) si quiere
que esa persona también use el panel de administración para tareas
avanzadas (editar catálogo, etc.).

---

## 3. Llevarlo a un servidor (producción)

El aplicativo está preparado para pasar de SQLite (local) a **PostgreSQL**
(servidor) sin cambiar una sola línea de código, solo variables de entorno.

### 3.0 La forma más sencilla: Render.com (un clic con "Blueprint")

El proyecto incluye un archivo `render.yaml` que le dice a Render exactamente
qué crear (la base de datos PostgreSQL y el servicio web), para que no tenga
que configurar nada a mano.

1. Cree una cuenta gratuita en **GitHub** (github.com) si no tiene una, y
   suba esta carpeta del proyecto a un repositorio nuevo (con **GitHub
   Desktop**, una aplicación con botones, sin necesidad de comandos).
2. En Render, vaya a **New → Blueprint** y seleccione ese repositorio.
   Render va a leer el archivo `render.yaml` y le va a mostrar lo que va a
   crear: una base de datos PostgreSQL y el servicio web.
3. Le va a pedir un solo valor manual: **DJANGO_SUPERUSER_PASSWORD** —
   escriba ahí la contraseña que quiere para el usuario `admin` en este
   servidor (elija una segura, distinta a la de su computador local).
4. Haga clic en **Apply / Deploy**. Render va a instalar todo, crear la base
   de datos, cargar el catálogo de los 24 pasos del PESV y crear el usuario
   administrador automáticamente. Esto tarda unos minutos.
5. Cuando termine, Render le da una dirección como
   `https://siga-pesv.onrender.com` — ahí ya puede entrar con usuario
   `admin` y la contraseña que definió en el paso 3.

> Nota: el plan gratuito de Render "duerme" el servicio si nadie lo usa por
> un rato (la primera carga tras un período de inactividad puede tardar
> 30-60 segundos) y la base de datos gratuita tiene límites de almacenamiento
> y tiempo. Es ideal para probar el aplicativo con el equipo de la
> Secretaría; para uso en producción real, se recomienda pasar a un plan de
> pago de Render o a un servidor propio (ver sección 3.1).

### 3.1 Forma manual / servidor propio (VPS): variables de entorno de producción

Cree un archivo `.env` (o configúrelas en su proveedor de hosting) con:

```
PESV_ENV=production
SECRET_KEY=<genere una clave larga y aleatoria>
DEBUG=False
ALLOWED_HOSTS=pesv.movilidadvillavicencio.gov.co,otra.ip.del.servidor
CSRF_TRUSTED_ORIGINS=https://pesv.movilidadvillavicencio.gov.co

DB_NAME=pesv_db
DB_USER=pesv_user
DB_PASSWORD=<clave segura>
DB_HOST=localhost
DB_PORT=5432
```

Instale además el conector de PostgreSQL:
```bash
pip install psycopg2-binary
```

### 3.2 Pasos típicos en un servidor Ubuntu

```bash
sudo apt update && sudo apt install python3-venv postgresql nginx -y
sudo -u postgres createuser pesv_user --pwprompt
sudo -u postgres createdb pesv_db -O pesv_user

# Dentro de la carpeta del proyecto:
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt psycopg2-binary

export $(cat .env | xargs)     # cargar variables de entorno
python manage.py migrate
python manage.py cargar_catalogo_pesv
python manage.py createsuperuser
python manage.py collectstatic --noinput

# Servir con Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Para producción real, ponga Gunicorn detrás de **Nginx** (proxy inverso) y
configúrelo como servicio de `systemd` para que arranque automáticamente y
se reinicie si falla. Con gusto preparo esos archivos de configuración
(`nginx.conf`, `pesv.service`) cuando me indique el dominio/IP del servidor
que va a usar.

### 3.3 Copias de seguridad
- **Base de datos:** `pg_dump pesv_db > respaldo_$(date +%F).sql`
- **Documentos y evidencias cargadas:** respaldar la carpeta `media/`
  periódicamente (contiene todos los PDF, fotos y soportes subidos).

---

## 4. Estructura del proyecto

```
pesv_app/
├── accounts/      Usuarios y roles (Admin, Auditor, Líder de equipo, Empresa[futuro])
├── empresas/      Empresas, vehículos y conductores
├── pesv/          Catálogo de los 24 pasos, componentes verificables e instrumentos
├── documentos/    Documentos soporte y evidencias de ejecución (doc/foto)
├── programa/      Programa anual de verificación y cronograma de visitas
├── auditorias/    Ejecución de auditorías, checklist, hallazgos, plan de mejoramiento, informe PDF
├── seguimiento/   Panel de control y matriz de seguimiento (con exportación a Excel)
├── config/        Configuración del proyecto (settings, urls)
├── templates/      Plantillas compartidas (base, login)
├── static/        CSS, imágenes (coloque aquí el logo institucional)
└── media/         Documentos y evidencias cargados por los usuarios (se crea solo)
```

## 5. Hacia la fase futura: empresas auto-gestionando su evidencia
El modelo de datos ya contempla un rol `EMPRESA` y un campo `empresa` en el
usuario, de modo que en una fase posterior cada empresa auditada pueda tener
su propio usuario y cargar directamente su documentación y evidencias (hoy
restringido a uso interno del equipo auditor de la Secretaría, como se
definió). El cambio que se requeriría más adelante es principalmente de
permisos/visibilidad por empresa, no de estructura de datos.

---

## 6. Soporte
Este aplicativo fue construido a la medida de los requerimientos descritos
para la Secretaría de Movilidad de Villavicencio. Cualquier ajuste al
catálogo PESV, a las preguntas de verificación, a los roles o a los formatos
del informe se puede hacer fácilmente — incluyendo una vez se compartan el
logo institucional y la rúbrica de evaluación.
