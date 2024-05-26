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
