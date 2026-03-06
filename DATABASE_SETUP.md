# Configuración de Base de Datos y Backend para DSS

## Requisitos Previos

- MySQL Server 5.7 o superior
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

## Paso 1: Instalación de MySQL

### En Windows
1. Descarga MySQL desde: https://dev.mysql.com/downloads/mysql/
2. Ejecuta el instalador y sigue los pasos
3. Asegúrate de tener MySQL Server corriendo

### En Linux/Mac
```bash
# Linux (Debian/Ubuntu)
sudo apt-get install mysql-server

# Mac
brew install mysql
```

## Paso 2: Crear la Base de Datos

1. Abre MySQL desde la terminal o MySQL Workbench:
```bash
mysql -u root -p
```

2. Ejecuta el script SQL:
```sql
source database.sql
```

O importa el archivo `database.sql` a través de cualquier cliente MySQL (Workbench, phpMyAdmin, etc.)

## Paso 3: Configurar el Backend

1. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

2. **Crea un archivo `.env` en el directorio raíz:**
```bash
cp .env.example .env
```

3. **Edita el archivo `.env` con tus credenciales de MySQL:**
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=dss_project
```

## Paso 4: Ejecutar el Backend

```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## Estructura de la Base de Datos

### Tablas principales:

1. **users** - Almacena información de usuarios
   - id, username, email, password, full_name, university
   - created_at, updated_at

2. **projects** - Almacena proyectos/prácticas
   - id, user_id, title, description, category, status
   - created_at, updated_at

3. **document_validations** - Almacena validaciones de DNI/NIE
   - id, user_id, document_type, document_number, is_valid
   - validated_at

4. **comments** - Almacena comentarios en proyectos
   - id, project_id, user_id, comment_text
   - created_at, updated_at

5. **project_files** - Almacena archivos de proyectos
   - id, project_id, file_name, file_path, file_type, file_size
   - uploaded_at

6. **notifications** - Almacena notificaciones para usuarios
   - id, user_id, title, message, notification_type, is_read
   - created_at

7. **activity_logs** - Almacena logs de actividades
   - id, user_id, action, resource_type, resource_id, ip_address
   - created_at

## Endpoints disponibles

### Usuarios
- `GET /api/users` - Obtener todos los usuarios
- `GET /api/users/<id>` - Obtener usuario específico
- `POST /api/users` - Crear nuevo usuario

### Proyectos
- `GET /api/projects` - Obtener todos los proyectos
- `GET /api/projects/<id>` - Obtener proyecto específico
- `POST /api/projects` - Crear nuevo proyecto
- `PUT /api/projects/<id>` - Actualizar proyecto

### Validación de Documentos
- `POST /api/validate-document` - Validar DNI/NIE
- `GET /api/documents/<user_id>` - Obtener documentos validados de un usuario

### Estadísticas
- `GET /api/statistics` - Obtener estadísticas generales

### Salud
- `GET /api/health` - Verificar estado de la API

## Testing con curl

```bash
# Obtener todos los usuarios
curl http://localhost:5000/api/users

# Crear un nuevo usuario
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","email":"test@test.com","password":"hashed_pass","full_name":"Test User", "university":"Universidad Test"}'

# Validar un documento
curl -X POST http://localhost:5000/api/validate-document \
  -H "Content-Type: application/json" \
  -d '{"document_type":"DNI","document_number":"12345678Z","user_id":1}'

# Obtener estadísticas
curl http://localhost:5000/api/statistics
```

## Integración con la Web (HTML)

Para llamar a la API desde tu HTML/JavaScript:

```javascript
// Ejemplo: Obtener proyectos
fetch('http://localhost:5000/api/projects')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Ejemplo: Validar documento
fetch('http://localhost:5000/api/validate-document', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document_type: 'DNI',
    document_number: '12345678Z',
    user_id: 1
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Troubleshooting

### Error: "Connection refused"
- Verifica que MySQL esté corriendo
- Comprueba que las credenciales en `.env` son correctas

### Error: "Unknown database"
- Asegúrate de haber ejecutado `database.sql`
- Verifica el nombre de la base de datos

### Error: "Module not found"
- Ejecuta `pip install -r requirements.txt`
- Asegúrate de estar en el entorno correcto

## Próximos pasos

1. Integrar la API con el HTML (index.html)
2. Crear un panel de administración
3. Implementar autenticación y autorización
4. Añadir más endpoints según necesites
5. Deployar en un servidor real