## Diagrama de Secuencia: Proceso de Login con CSRF

```mermaid
sequenceDiagram
    participant Usuario
    participant Cliente
    participant Servidor

    Usuario->>Cliente: Solicita token CSRF
    Cliente->>Servidor: GET /csrf-token
    Servidor->>Cliente: Devuelve CSRF token
    Cliente->>Usuario: Muestra CSRF token

    Usuario->>Cliente: Envía credenciales y CSRF token
    Cliente->>Servidor: POST /login
    Servidor->>Servidor: Valida CSRF token
    Servidor->>Servidor: Valida credenciales
    Servidor->>Servidor: Genera y envía token de sesión por correo
    Servidor->>Cliente: Responde con mensaje de éxito

    Usuario->>Correo: Recibe token de sesión
    Usuario->>Cliente: Envía credenciales, CSRF token y token de sesión
    Cliente->>Servidor: POST /login (con token de sesión)
    Servidor->>Servidor: Valida CSRF token
    Servidor->>Servidor: Valida token de sesión
    Servidor->>Cliente: Responde con mensaje de login exitoso y datos del usuario
    Cliente->>Usuario: Muestra mensaje de login exitoso

# Checklist de Requerimientos y Funcionalidades

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
