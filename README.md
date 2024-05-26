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
