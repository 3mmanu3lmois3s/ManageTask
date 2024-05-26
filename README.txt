## Sistema de consola ManageTask con seguridad incluida e interfaz API extendida

El sistema ManageTask es un gestor de tareas multiusuario
incluye persistencia en 2 archivos json, uno para guardar los usuarios 
y otro para guardar las tareas, a futuro si se quisiera escalar se usaria una base de datos,
ademas es un sistema totalmente escalable pensado para seguir creciendo en la web
o en mobile, porque implementa un API REST securizada con un mecanismo de doble autenticación , cors y token
csrf. Tambien implementa documentación SWAGGER para la documentación de la API y diagramas de secuencia en notación mermaids para verse en github.


## Instrucciones para poder ejecutar la app

1) pip install -r requirements.txt

En el archivo requirements.txt se incluye las librerías necesarias para:

Flask: El framework principal para crear la API.
Flasgger: Para la documentación de la API.
Aiosmtpd: Para el servidor SMTP asíncrono.
Python-dateutil: Para el manejo de fechas.
Flask-CORS: Para habilitar CORS en la aplicación.
Flask-WTF: Para la protección CSRF.
Instalando el requirements.txt asegura que todas las dependencias necesarias estén disponibles.


2) luego ejecutar el archivo python ManageTask.py  

Este archivo tiene lo necesario para levantar la aplicación desde la consola y desde el API. Usted decide que quiere probar.

3) Tome en cuenta que la primera vez se crea un usuario ADMIN con un Password por defecto:  ADMIN333 y  SUBETEAMIMOTOPIBON#333 dentro del archivo Usuarios.json

3) Luego puede probar las opciones desde la consola o directamente en el navegador entrar a la doc del api en swagger:  http://127.0.0.1:5000/apidocs

## PRUEBAS DEL API desde CURL:

Prueba desde CMD WINDOWS con CURL:

1) Primero solicitar el csrf-token:

curl -c cookies.txt -X GET "http://127.0.0.1:5000/csrf-token"

2) luego setearlo en la sesión de 	CMD:

CSRF_TOKEN="IjFmNWMxYzA4MGU3MzJhNjgzZWVkNDg5MzgxNTc0MGRiMTc3MDkxZmIi.ZlL9tA.gPP4PaP59TsxrA3hIxiFCyMZ0Sc"

3) luego logarse con el token el usuario y la clave

curl -b cookies.txt -c cookies.txt -X POST "http://127.0.0.1:5000/login" ^
-H "Content-Type: application/json" ^
-H "X-CSRFToken: %CSRF_TOKEN%" ^
-d "{\"nickname\": \"ADMIN333\", \"clave\": \"SUBETEAMIMOTOPIBON#333\"}"


3) Luego agrego una tarea:

curl -b cookies.txt -c cookies.txt -X POST "http://127.0.0.1:5000/tareas" -H "Content-Type: application/json" -H "X-CSRFToken: %CSRF_TOKEN%" -d "{\"descripcion\": \"Descripción de la tarea\", \"tipo\": true, \"id_usuario\": \"3d2f2d3b-39f2-4fd2-b3ae-316193792209\", \"compartida\": false, \"compartida_con\": \"\", \"dependiente\": false, \"dependiente_de\": \"\", \"nickname\": \"ADMIN333\", \"token\": \"4075d677-3591-4394-98fd-ecbdd3c33413\"}"
{"message":"Tarea agregada correctamente"}

4) Luego se ven todas las tareas

curl -b cookies.txt -c cookies.txt -X GET "http://127.0.0.1:5000/tareas?id_usuario=3d2f2d3b-39f2-4fd2-b3ae-316193792209&tipo_usuario=admin" -H "Content-Type: application/json" -H "X-CSRFToken: %CSRF_TOKEN%" -d "{\"nickname\": \"ADMIN333\", \"token\": \"4075d677-3591-4394-98fd-ecbdd3c33413\"}"
[{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"ver tv","estado":"c","fecha_fin":"2024-05-25T20:15:53.732037","fecha_inicio":"2024-05-25T16:04:22.797700","id":"90eeaf38-6cd2-4cad-a900-75f844bdcab4","id_sec":8,"id_sec2":8,"id_usuario":"059cc870-967c-41ab-9d0f-7f0581487cd5","tipo":true},{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"Acostarse","estado":"c","fecha_fin":"2024-05-25T21:43:16.804924","fecha_inicio":"2024-05-25T21:42:58.429914","id":"d6b6db91-54bc-4eef-8026-23a097bf93c7","id_sec":12,"id_sec2":12,"id_usuario":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","tipo":true},{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"arroparse","estado":"c","fecha_fin":"2024-05-25T23:17:02.894074","fecha_inicio":"2024-05-25T23:16:40.565044","id":"6b8b3169-2a01-4085-a1b2-6d69d53cd8f8","id_sec":14,"id_sec2":14,"id_usuario":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","tipo":false},{"b":false,"compartida":false,"compartida_con":"","completada_por":null,"dependiente":false,"dependiente_de":"","descripcion":"Descripci\u00f3n de la tarea","estado":"p","fecha_fin":null,"fecha_inicio":"2024-05-26T11:39:44.742078","id":"f0ead983-5f49-44e6-8648-5f163644c0f7","id_sec":15,"id_sec2":15,"id_usuario":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","tipo":true}]

5) Luego se ven todas las tareas filtradas por dia

curl -b cookies.txt -c cookies.txt -X GET "http://127.0.0.1:5000/tareas_filtradas?id_usuario=3d2f2d3b-39f2-4fd2-b3ae-316193792209&tipo_usuario=admin&dia=25/05/2024" -H "Content-Type: application/json" -H "X-CSRFToken: %CSRF_TOKEN%" -d "{\"nickname\": \"ADMIN333\", \"token\": \"4075d677-3591-4394-98fd-ecbdd3c33413\"}"
[{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"ver tv","estado":"c","fecha_fin":"2024-05-25T20:15:53.732037","fecha_inicio":"2024-05-25T16:04:22.797700","id":"90eeaf38-6cd2-4cad-a900-75f844bdcab4","id_sec":8,"id_sec2":8,"id_usuario":"059cc870-967c-41ab-9d0f-7f0581487cd5","tipo":true},{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"Acostarse","estado":"c","fecha_fin":"2024-05-25T21:43:16.804924","fecha_inicio":"2024-05-25T21:42:58.429914","id":"d6b6db91-54bc-4eef-8026-23a097bf93c7","id_sec":12,"id_sec2":12,"id_usuario":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","tipo":true},{"b":false,"compartida":false,"compartida_con":"","completada_por":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","dependiente":false,"dependiente_de":"","descripcion":"arroparse","estado":"c","fecha_fin":"2024-05-25T23:17:02.894074","fecha_inicio":"2024-05-25T23:16:40.565044","id":"6b8b3169-2a01-4085-a1b2-6d69d53cd8f8","id_sec":14,"id_sec2":14,"id_usuario":"3d2f2d3b-39f2-4fd2-b3ae-316193792209","tipo":false}]

6) Luego se eliminamos la tarea agregada

curl -b cookies.txt -c cookies.txt -X DELETE "http://127.0.0.1:5000/tareas/15" -H "Content-Type: application/json" -H "X-CSRFToken: %CSRF_TOKEN%" -d "{\"id_usuario\": \"3d2f2d3b-39f2-4fd2-b3ae-316193792209\", \"nickname\": \"ADMIN333\", \"token\": \"4075d677-3591-4394-98fd-ecbdd3c33413\"}"
{"message":"Tarea eliminada correctamente"}

7) Luego se ven las tareas eliminadas por filtro dia

curl -b cookies.txt -c cookies.txt -X GET "http://127.0.0.1:5000/tareas_eliminadas_filtradas?id_usuario=3d2f2d3b-39f2-4fd2-b3ae-316193792209&tipo_usuario=admin&dia=26/05/2024" -H "Content-Type: application/json" -H "X-CSRFToken: %CSRF_TOKEN%" -d "{\"nickname\": \"ADMIN333\", \"token\": \"4075d677-3591-4394-98fd-ecbdd3c33413\"}"


# Checklist de Requerimientos y Funcionalidades entregadas en esta versión 1.0.0

## Funcionalidades Generales

1. **Sistema de Usuarios**
    - [x] Crear usuarios con nickname, clave, email, tipo (admin/user), y zona horaria.
    - [x] Modificar usuarios existentes.
    - [x] Eliminar usuarios.
    - [x] Listar todos los usuarios.
    - [x] Enviar token de acceso por email.
    - [x] Validar tokens de acceso.

2. **Sistema de Tareas**
    - [x] Crear tareas con descripción, tipo, usuario asignado, compartida, dependiente.
    - [x] Listar todas las tareas pendientes y completadas.
    - [x] Marcar tareas como completadas.
    - [x] Eliminar tareas.
    - [x] Filtrar tareas por día, mes, semana y año.
    - [x] Filtrar tareas eliminadas por día, mes, semana y año.

3. **Persistencia de Datos**
    - [x] Guardar usuarios en archivo JSON.
    - [x] Cargar usuarios desde archivo JSON.
    - [x] Guardar tareas en archivo JSON.
    - [x] Cargar tareas desde archivo JSON.

## Funcionalidades de Consola

4. **Interfaz de Consola**
    - [x] Mostrar menú principal para usuarios.
    - [x] Mostrar menú principal para administradores.
    - [x] Gestionar usuarios (administrador).
    - [x] Añadir nueva tarea.
    - [x] Marcar tarea como completada.
    - [x] Mostrar todas las tareas.
    - [x] Eliminar una tarea.
    - [x] Mostrar tareas eliminadas.
    - [x] Filtrar tareas por día, mes, semana y año.
    - [x] Filtrar tareas eliminadas por día, mes, semana y año.
    - [x] Limpiar el sistema (administrador).

5. **Control de Errores y Validaciones**
    - [x] Validar formato de fecha en los filtros.
    - [x] Manejar errores al filtrar por múltiples parámetros.
    - [x] Mostrar mensajes de error y éxito en las operaciones.

## Funcionalidades de API Flask

6. **Endpoints de Usuario**
    - [x] `POST /login`: Iniciar sesión de usuario.
    - [x] `POST /logout`: Cerrar sesión de usuario.
    - [x] `GET /usuarios`: Obtener todos los usuarios.
    - [x] `POST /usuarios`: Agregar un nuevo usuario.
    - [x] `PUT /usuarios/<id_user>`: Modificar un usuario.
    - [x] `DELETE /usuarios/<id_user>`: Eliminar un usuario.

7. **Endpoints de Tareas**
    - [x] `GET /tareas`: Obtener todas las tareas.
    - [x] `POST /tareas`: Agregar una nueva tarea.
    - [x] `PUT /tareas/<int:id_sec2>`: Marcar una tarea como completada.
    - [x] `DELETE /tareas/<int:id_sec2>`: Eliminar una tarea.
    - [x] `GET /tareas_eliminadas`: Obtener todas las tareas eliminadas.
    - [x] `GET /tareas_filtradas`: Obtener tareas filtradas por día, mes, semana y año.
    - [x] `GET /tareas_eliminadas_filtradas`: Obtener tareas eliminadas filtradas por día, mes, semana y año.
    - [x] `POST /limpiar_sistema`: Limpiar el sistema (administrador).

8. **Documentación de la API**
    - [x] Documentar cada endpoint utilizando `flasgger`.
    - [x] Configurar y mostrar la interfaz de Swagger UI.

9. **Seguridad**
    - [x] Verificar token en cada operación que lo requiera.
    - [x] Manejar expiración de tokens.
    - [x] Implementar protección CSRF.
    - [x] Configurar CORS para permitir solicitudes desde el origen esperado.

## Tareas Adicionales
- [x] Ajustar el manejo de fechas para filtros.
- [x] Revisar y corregir errores en la lógica de negocio.
- [x] Asegurar que los filtros de búsqueda funcionen correctamente.
- [x] Documentar errores y manejar excepciones.
- [x] Integrar manejo de sesiones en las pruebas curl.
- [x] Implementar y validar el flujo de login con CSRF token.
- [x] Crear diagramas de secuencia para el proceso de login, uso general del API y la app de consola.

Firma del creador: 3mmanu3lmois3s | Emmanuel Moises Mellado Martinez - Curso IBM| BeJobs - tlf 617162287 
linkedin:
https://www.linkedin.com/in/emmanuelmellado/
Github (contenido privado): https://github.com/3mmanu3lmois3s