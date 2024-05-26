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

