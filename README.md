# Entrega 2 - DDS

## Configuración del proyecto

Sigue estos pasos para configurar y ejecutar la aplicación:

### 1. Clonar el repositorio
```bash
git clone https://github.com/Mazulini/Tarea-2-Diseno-de-Software
cd App web
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv venv
.\venv\Scripts\Activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

### 3. Instalar dependencias
Instala las dependencias listadas en `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos
1. **Crea la base de datos en PostgreSQL**:
   - Ejecuta el script SQL proporcionado en el repositorio (por ejemplo, `database.sql`):
     ```bash
     psql -U postgres -d gestion_rutas -f "Base de Datos/Estructura.sql"
     ```
   - Esto creará la base de datos `gestion_rutas` con las tablas necesarias.

2. **Poblar la base de datos**:
   - Para añadir datos de ejemplo, ejecuta:
     ```bash
     psql -U postgres -d gestion_rutas -f "Base de Datos/datos.sql"
     ```

3. **Actualizar secuencias de IDs**:
   - Ejecuta los siguientes comandos en `psql` para actualizar el último ID presente en la base de datos, para que sea posible seguir con la serialización al registrar nuevos usuarios:
     ```sql
      SELECT setval(pg_get_serial_sequence('usuario', 'id'), (SELECT MAX(id) FROM usuario));
      SELECT setval(pg_get_serial_sequence('cliente', 'id'), (SELECT MAX(id) FROM cliente));
      SELECT setval(pg_get_serial_sequence('conductor', 'id'), (SELECT MAX(id) FROM conductor));
      SELECT setval(pg_get_serial_sequence('admin', 'id'), (SELECT MAX(id) FROM admin));
      SELECT setval(pg_get_serial_sequence('paquete', 'id'), (SELECT MAX(id) FROM paquete));
      SELECT setval(pg_get_serial_sequence('envio', 'id'), (SELECT MAX(id) FROM envio));
      SELECT setval(pg_get_serial_sequence('ruta', 'id'), (SELECT MAX(id) FROM ruta));
      SELECT setval(pg_get_serial_sequence('reporte', 'id'), (SELECT MAX(id) FROM reporte));
     ```

4. **Configura las credenciales en `appweb/settings.py`**:
   - Asegúrate de que la configuración de `DATABASES` sea:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'gestion_rutas',
             'USER': 'postgres',
             'PASSWORD': 'TU_CONTRASEÑA',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

### 5. Configurar usuarios para login
Ejecuta los siguientes comandos en la shell de Django para establecer contraseñas para los usuarios predefinidos:

```bash
python manage.py shell
```

1. **Usuario administrador** (`pablo.admin@example.com`):
   ```python
   from apps.accounts.models import Usuario
   from django.contrib.auth.hashers import make_password

   usuario = Usuario.objects.get(correo='pablo.admin@example.com')
   usuario.contrasena = make_password('1234')
   usuario.save()
   ```

2. **Usuario conductor** (`pedro.ramirez@example.com`):
   ```python
   from apps.accounts.models import Usuario
   from django.contrib.auth.hashers import make_password

   usuario = Usuario.objects.get(correo='pedro.ramirez@example.com')
   usuario.contrasena = make_password('1234')
   usuario.save()
   ```

Estos usuarios te permitirán iniciar sesión en:
- **Administrador**: `http://127.0.0.1:8000/accounts/login` con `pablo.admin@example.com` y contraseña `1234`.
- **Conductor**: `http://127.0.0.1:8000/accounts/login` con `pedro.ramirez@example.com` y contraseña `1234`.

### 6. Ejecutar la aplicación
Inicia el servidor de desarrollo (asegurate de estar en /App web/):
```bash
python manage.py runserver
```

- Accede a la aplicación en `http://127.0.0.1:8000/` debería redirigir automáticamente al login.


## Notas adicionales
- **Entorno virtual**: Siempre activa el entorno virtual (`.\venv\Scripts\Activate`) antes de ejecutar `python manage.py runserver`.
- **Base de datos**: Asegúrate de que PostgreSQL esté corriendo antes de iniciar la aplicación.