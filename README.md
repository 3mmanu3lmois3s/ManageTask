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

## Diagrama de Secuencia: Uso General del API

```mermaid
sequenceDiagram
    participant Usuario
    participant Cliente
    participant Servidor

    Usuario->>Cliente: Solicita token CSRF
    Cliente->>Servidor: GET /csrf-token
    Servidor->>Cliente: Devuelve CSRF token
    Cliente->>Usuario: Muestra CSRF token

    Usuario->>Cliente: Realiza solicitud API (Agregar Tarea, Ver Tareas, etc.)
    Cliente->>Servidor: Envío solicitud API con CSRF token y token de sesión
    Servidor->>Servidor: Valida CSRF token y token de sesión
    Servidor->>Servidor: Procesa solicitud (Agregar, Ver, Modificar, Eliminar)
    Servidor->>Cliente: Devuelve respuesta con datos solicitados o confirmación de operación
    Cliente->>Usuario: Muestra respuesta del servidor

## Diagrama de Secuencia: App de Consola

```mermaid
sequenceDiagram
    participant Usuario
    participant AppConsola

    Usuario->>AppConsola: Selecciona opción de login
    AppConsola->>Usuario: Solicita nickname y clave
    Usuario->>AppConsola: Ingresa nickname y clave
    AppConsola->>AppConsola: Valida credenciales
    AppConsola->>Usuario: Muestra mensaje de login exitoso

    Usuario->>AppConsola: Selecciona opción (Agregar, Ver, Modificar, Eliminar)
    alt Agregar Tarea
        AppConsola->>Usuario: Solicita detalles de la tarea
        Usuario->>AppConsola: Ingresa detalles de la tarea
        AppConsola->>AppConsola: Agrega tarea a la lista
        AppConsola->>Usuario: Muestra confirmación de tarea agregada
    end
    alt Ver Tareas
        AppConsola->>AppConsola: Carga lista de tareas
        AppConsola->>Usuario: Muestra lista de tareas
    end
    alt Modificar Tarea
        AppConsola->>Usuario: Solicita ID y nuevos detalles de la tarea
        Usuario->>AppConsola: Ingresa ID y nuevos detalles
        AppConsola->>AppConsola: Modifica tarea en la lista
        AppConsola->>Usuario: Muestra confirmación de tarea modificada
    end
    alt Eliminar Tarea
        AppConsola->>Usuario: Solicita ID de la tarea a eliminar
        Usuario->>AppConsola: Ingresa ID de la tarea
        AppConsola->>AppConsola: Elimina tarea de la lista
        AppConsola->>Usuario: Muestra confirmación de tarea eliminada
    end

