import os
import json
import uuid
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
from multiprocessing import Process

class Usuario:
    """Clase que representa un usuario."""
    def __init__(self, nickname, clave, email, tipo="user", zona_horaria="UTC"):
        self.id_user = str(uuid.uuid4())
        self.nickname = nickname
        self.clave = clave
        self.email = email
        self.token = None
        self.token_expiracion = None
        self.estado = True
        self.fecha_creacion = datetime.now().isoformat()
        self.pertenece = False
        self.pertenece_a = ""
        self.tipo = tipo
        self.zona_horaria = zona_horaria  # Nuevo campo para zona horaria

    def to_dict(self):
        """Convierte el usuario a un diccionario."""
        return {
            "id_user": self.id_user,
            "nickname": self.nickname,
            "clave": self.clave,
            "email": self.email,
            "token": self.token,
            "token_expiracion": self.token_expiracion,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion,
            "pertenece": self.pertenece,
            "pertenece_a": self.pertenece_a,
            "tipo": self.tipo,
            "zona_horaria": self.zona_horaria  # Nuevo campo para zona horaria
        }

class GestorUsuarios:
    """Clase para gestionar usuarios."""
    def __init__(self, archivo="usuarios.json"):
        self.usuarios = []
        self.archivo = archivo
        self.cargar_usuarios()
        if not self.usuarios:
            self.crear_admin()

    def crear_admin(self):
        """Crea un usuario administrador por defecto si no existen usuarios."""
        admin = Usuario("ADMIN333", "SUBETEAMIMOTOPIBON#333", "admin@admin.com", "admin", "UTC")
        self.usuarios.append(admin)
        self.guardar_usuarios()

    def agregar_usuario(self, nickname, clave, email, tipo="user", zona_horaria="UTC"):
        """Agrega un nuevo usuario."""
        usuario = Usuario(nickname, clave, email, tipo, zona_horaria)
        self.usuarios.append(usuario)
        self.guardar_usuarios()

    def modificar_usuario(self, id_user, **kwargs):
        """Modifica un usuario existente."""
        for usuario in self.usuarios:
            if usuario.id_user == id_user:
                for key, value in kwargs.items():
                    setattr(usuario, key, value)
                self.guardar_usuarios()
                return True
        return False

    def eliminar_usuario(self, id_user):
        """Elimina un usuario dado su ID."""
        self.usuarios = [u for u in self.usuarios if u.id_user != id_user]
        self.guardar_usuarios()

    def listar_usuarios(self):
        """Lista todos los usuarios."""
        for usuario in self.usuarios:
            print(f"ID: {usuario.id_user}, Nickname: {usuario.nickname}, Email: {usuario.email}, Tipo: {usuario.tipo}, Zona Horaria: {usuario.zona_horaria}")

    def guardar_usuarios(self):
        """Guarda los usuarios en un archivo JSON."""
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump([usuario.to_dict() for usuario in self.usuarios], f, ensure_ascii=False, indent=4)

    def cargar_usuarios(self):
        """Carga los usuarios desde un archivo JSON."""
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                usuarios = json.load(f)
                for usuario_dict in usuarios:
                    usuario = Usuario(
                        usuario_dict['nickname'],
                        usuario_dict['clave'],
                        usuario_dict.get('email', 'email@example.com'),  # Obtener email, valor predeterminado 'email@example.com'
                        usuario_dict['tipo'],
                        usuario_dict.get('zona_horaria', 'UTC')  # Obtener zona horaria, valor predeterminado 'UTC'
                    )
                    usuario.id_user = usuario_dict['id_user']
                    usuario.token = usuario_dict.get('token')
                    usuario.token_expiracion = usuario_dict.get('token_expiracion')
                    usuario.estado = usuario_dict['estado']
                    usuario.fecha_creacion = usuario_dict['fecha_creacion']
                    usuario.pertenece = usuario_dict['pertenece']
                    usuario.pertenece_a = usuario_dict['pertenece_a']
                    self.usuarios.append(usuario)

    def enviar_token(self, usuario):
        """Genera y envía un token al email del usuario."""
        token = str(uuid.uuid4())
        usuario.token = token
        usuario.token_expiracion = (datetime.now() + timedelta(days=1)).isoformat()
        self.guardar_usuarios()

        # Enviar email con el token
        msg = MIMEText(f"Su token de acceso es: {token}")
        msg['Subject'] = 'Token de acceso'
        msg['From'] = 'noreply@tareas.com'
        msg['To'] = usuario.email

        # Configurar tu servidor SMTP aquí
        smtp_server = '127.0.0.1'
        smtp_port = 1025
        smtp_user = None
        smtp_password = None

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())

    def validar_token(self, nickname, token):
        """Valida el token del usuario."""
        for usuario in self.usuarios:
            if usuario.nickname == nickname:
                if usuario.token == token and datetime.now() < parser.parse(usuario.token_expiracion):
                    return True
        return False

class Tarea:
    secuencia_id = 0

    def __init__(self, descripcion, tipo, id_usuario, compartida, compartida_con, dependiente, dependiente_de):
        self.id = str(uuid.uuid4())
        self.descripcion = descripcion
        self.estado = 'p'  # 'p' para pendiente, 'c' para completada, 'e' para eliminada
        self.fecha_inicio = datetime.now().isoformat()
        self.fecha_fin = None
        self.id_usuario = id_usuario
        self.tipo = tipo
        self.id_sec = None
        self.id_sec2 = None
        self.compartida = compartida
        self.compartida_con = compartida_con
        self.dependiente = dependiente
        self.dependiente_de = dependiente_de
        self.completada_por = None
        self.b = False

    def to_dict(self):
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "id_usuario": self.id_usuario,
            "tipo": self.tipo,
            "id_sec": self.id_sec,
            "id_sec2": self.id_sec2,
            "compartida": self.compartida,
            "compartida_con": self.compartida_con,
            "dependiente": self.dependiente,
            "dependiente_de": self.dependiente_de,
            "completada_por": self.completada_por,
            "b": self.b
        }

    def __str__(self):
        estados = {'p': 'Pendiente', 'c': 'Completada', 'e': 'Eliminada'}
        return f"{self.descripcion} - {estados.get(self.estado, 'Desconocido')}"

class ListaDeTareas:
    def __init__(self, archivo="tareas.json"):
        self.tareas = []
        self.archivo = archivo
        self.cargar_tareas()

    def cargar_tareas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r', encoding='utf-8') as f:
                tareas = json.load(f)
                self.tareas = []
                max_id_sec = -1
                for tarea_dict in tareas:
                    tarea = Tarea(
                        tarea_dict['descripcion'],
                        tarea_dict['tipo'],
                        tarea_dict['id_usuario'],
                        tarea_dict['compartida'],
                        tarea_dict['compartida_con'],
                        tarea_dict['dependiente'],
                        tarea_dict['dependiente_de']
                    )
                    tarea.id = tarea_dict['id']
                    tarea.estado = tarea_dict['estado']
                    tarea.fecha_inicio = tarea_dict['fecha_inicio']
                    tarea.fecha_fin = tarea_dict['fecha_fin']
                    tarea.id_sec = tarea_dict['id_sec']
                    tarea.id_sec2 = tarea_dict['id_sec2']
                    tarea.completada_por = tarea_dict['completada_por']
                    tarea.b = tarea_dict['b']
                    self.tareas.append(tarea)
                    if tarea.id_sec > max_id_sec:
                        max_id_sec = tarea.id_sec
                Tarea.secuencia_id = max_id_sec + 1

    def guardar_tareas(self):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump([tarea.to_dict() for tarea in self.tareas], f, ensure_ascii=False, indent=4)

    def agregar_tarea(self, descripcion, tipo, id_usuario, compartida, compartida_con, dependiente, dependiente_de):
        tarea = Tarea(descripcion, tipo, id_usuario, compartida, compartida_con, dependiente, dependiente_de)
        if self.tareas:
            tarea.id_sec = max(t.id_sec for t in self.tareas) + 1
        else:
            tarea.id_sec = 0
        tarea.id_sec2 = tarea.id_sec
        self.tareas.append(tarea)
        self.guardar_tareas()

    def mostrar_tareas(self, id_usuario, tipo_usuario):
        """Muestra todas las tareas pendientes del día actual para el usuario dado."""
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        mañana = hoy + timedelta(days=1)
        for tarea in self.tareas:
            tarea_inicio = parser.parse(tarea.fecha_inicio)
            if tarea.estado != 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con) and hoy <= tarea_inicio < mañana:
                print(f"{tarea.id_sec2}. {tarea}")

    def mostrar_tareas_eliminadas(self, id_usuario, tipo_usuario):
        """Muestra todas las tareas eliminadas del día actual para el usuario dado."""
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        mañana = hoy + timedelta(days=1)
        for tarea in self.tareas:
            tarea_fin = parser.parse(tarea.fecha_fin) if tarea.fecha_fin else None
            if tarea.estado == 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con) and tarea_fin and hoy <= tarea_fin < mañana:
                print(f"{tarea.id_sec}. {tarea}")

    def filtrar_tareas(self, id_usuario, tipo_usuario, dia, mes, semana, year):
        """Filtra las tareas según el parámetro opcional proporcionado."""
        if sum(x is not None for x in [dia, mes, semana, year]) > 1:
            raise ValueError("Error: Solo se puede proporcionar un parámetro opcional.")

        self.cargar_tareas()  # Recargar tareas desde el archivo

        if dia:
            try:
                filtro_fecha = datetime.strptime(dia, '%d/%m/%Y')
                inicio = filtro_fecha
                fin = inicio + timedelta(days=1)
            except ValueError:
                raise ValueError("Error: Formato de día inválido. Debe ser 'dd/mm/yyyy'.")
        elif mes:
            try:
                filtro_fecha = datetime.strptime(mes, '%m')
                inicio = datetime(datetime.now().year, filtro_fecha.month, 1)
                fin = inicio + relativedelta(months=1)
            except ValueError:
                raise ValueError("Error: Formato de mes inválido. Debe ser 'mm'.")
        elif semana:
            try:
                semana = int(semana)
                año_actual = datetime.now().year
                inicio = datetime.strptime(f'{año_actual}-W{semana}-1', "%Y-W%W-%w")
                fin = inicio + timedelta(weeks=1)
            except ValueError:
                raise ValueError("Error: Formato de semana inválido. Debe ser un número entero.")
        elif year:
            try:
                filtro_fecha = datetime.strptime(year, '%Y')
                inicio = datetime(filtro_fecha.year, 1, 1)
                fin = inicio + relativedelta(years=1)
            except ValueError:
                raise ValueError("Error: Formato de año inválido. Debe ser 'yyyy'.")
        else:
            raise ValueError("Error: Debe proporcionar un parámetro opcional.")

        tareas_filtradas = []
        for tarea in self.tareas:
            tarea_inicio = parser.parse(tarea.fecha_inicio)
            if tarea.estado != 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con) and inicio <= tarea_inicio < fin:
                tareas_filtradas.append(tarea)

        if not tareas_filtradas:
            print("No hay tareas para el filtro especificado.")
        else:
            for tarea in tareas_filtradas:
                print(f"{tarea.id_sec2}. {tarea}")

        return tareas_filtradas  # Añadido para devolver las tareas filtradas

    def filtrar_tareas_eliminadas(self, id_usuario, tipo_usuario, dia=None, mes=None, semana=None, year=None):
        """Filtra las tareas eliminadas según el parámetro opcional proporcionado."""
        if sum(x is not None for x in [dia, mes, semana, year]) > 1:
            raise ValueError("Error: Solo se puede proporcionar un parámetro opcional.")

        self.cargar_tareas()  # Recargar tareas desde el archivo

        if dia:
            try:
                filtro_fecha = datetime.strptime(dia, '%d/%m/%Y')
                inicio = filtro_fecha
                fin = inicio + timedelta(days=1)
            except ValueError:
                raise ValueError("Error: Formato de día inválido. Debe ser 'dd/mm/yyyy'.")
        elif mes:
            try:
                filtro_fecha = datetime.strptime(mes, '%m')
                inicio = datetime(datetime.now().year, filtro_fecha.month, 1)
                fin = inicio + relativedelta(months=1)
            except ValueError:
                raise ValueError("Error: Formato de mes inválido. Debe ser 'mm'.")
        elif semana:
            try:
                filtro_fecha = datetime.now() + relativedelta(weeks=+int(semana))
                inicio = filtro_fecha - timedelta(days=filtro_fecha.weekday())
                fin = inicio + timedelta(weeks=1)
            except ValueError:
                raise ValueError("Error: Formato de semana inválido. Debe ser un número entero.")
        elif year:
            try:
                filtro_fecha = datetime.strptime(year, '%Y')
                inicio = datetime(filtro_fecha.year, 1, 1)
                fin = inicio + relativedelta(years=1)
            except ValueError:
                raise ValueError("Error: Formato de año inválido. Debe ser 'yyyy'.")
        else:
            raise ValueError("Error: Debe proporcionar un parámetro opcional.")

        tareas_filtradas = []
        for tarea in self.tareas:
            tarea_fin = parser.parse(tarea.fecha_fin) if tarea.fecha_fin else None
            if tarea.estado == 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con) and tarea_fin and inicio <= tarea_fin < fin:
                tareas_filtradas.append(tarea)

        if not tareas_filtradas:
            print("No hay tareas eliminadas para el filtro especificado.")
        else:
            for tarea in tareas_filtradas:
                print(f"{tarea.id_sec}. {tarea}")

        return tareas_filtradas  # Añadido para devolver las tareas filtradas


    def marcar_tarea_completada(self, id_sec2, id_usuario):
        """Marca una tarea como completada dado su id_sec2."""
        try:
            tarea = next(tarea for tarea in self.tareas if tarea.id_sec2 == id_sec2)
            if not tarea.b:
                tarea.b = True
                tarea.estado = 'c'
                tarea.fecha_fin = datetime.now().isoformat()
                tarea.completada_por = id_usuario
                tarea.b = False
                self.guardar_tareas()
                print("*********************************************")
                print("** Tarea completada.                       **")
                print("*********************************************")
            else:
                print("*********************************************")
                print("** La tarea está siendo utilizada.         **")
                print("*********************************************")
        except StopIteration:
            print("Error: Tarea no encontrada.")

    def eliminar_tarea(self, id_sec2, id_usuario):
        """Marca una tarea como eliminada dado su id_sec2 y ajusta las secuencias, solo si el usuario es el creador."""
        try:
            tarea = next(tarea for tarea in self.tareas if tarea.id_sec2 == id_sec2)
            if not tarea.b:
                tarea.b = True
                if tarea.id_usuario == id_usuario:
                    tarea.estado = 'e'
                    tarea.fecha_fin = datetime.now().isoformat()
                    tarea.id_sec2 = -tarea.id_sec2
                    tarea.b = False
                    self.guardar_tareas()
                    print("*********************************************")
                    print("** Tarea eliminada.                        **")
                    print("*********************************************")
                else:
                    tarea.b = False
                    print("*********************************************")
                    print("** No tiene permisos para eliminar esta    **")
                    print("** tarea.                                  **")
                    print("*********************************************")
            else:
                print("*********************************************")
                print("** La tarea está siendo utilizada.         **")
                print("*********************************************")
        except StopIteration:
            print("Error: Tarea no encontrada.")

    def limpiar_sistema(self):
        """Limpia el sistema eliminando todas las tareas."""
        self.tareas = []
        Tarea.secuencia_id = 0
        self.guardar_tareas()
        print("*********************************************")
        print("** Sistema limpiado. Todas las tareas      **")
        print("** han sido eliminadas.                    **")
        print("*********************************************")

def ejecutar_api():
    """Función para ejecutar la API Flask."""
    from app import app
    app.run(debug=False)

def mostrar_bienvenida():
    """Muestra un mensaje de bienvenida."""
    print("*********************************************")
    print("**                                         **")
    print("**         ¡Bienvenido al Gestor de        **")
    print("**                Tareas!                  **")
    print("**                                         **")
    print("*********************************************")

def mostrar_menu():
    """Muestra el menú principal."""
    print("\n*********************************************")
    print("**        Gestión de Tareas                **")
    print("*********************************************")
    print("** 1. Agregar una nueva tarea              **")
    print("** 2. Marcar una tarea como completada     **")
    print("** 3. Mostrar todas las tareas             **")
    print("** 4. Eliminar una tarea                   **")
    print("** 5. Iniciar API                          **")
    print("** 6. Detener API                          **")
    print("** 7. Estado del API                       **")
    print("** 8. Mostrar tareas eliminadas            **")
    print("** 9. Mostrar tareas filtradas             **")
    print("** 10. Mostrar tareas eliminadas filtradas **")
    print("** 11. Limpiar el sistema                  **")
    print("** 12. Salir                               **")
    print("*********************************************")

def mostrar_menu_admin():
    """Muestra el menú principal para el administrador."""
    print("\n*********************************************")
    print("**        Gestión de Tareas                **")
    print("*********************************************")
    print("** 1. Agregar una nueva tarea              **")
    print("** 2. Marcar una tarea como completada     **")
    print("** 3. Mostrar todas las tareas             **")
    print("** 4. Eliminar una tarea                   **")
    print("** 5. Iniciar API                          **")
    print("** 6. Detener API                          **")
    print("** 7. Estado del API                       **")
    print("** 8. Mostrar tareas eliminadas            **")
    print("** 9. Mostrar tareas filtradas             **")
    print("** 10. Mostrar tareas eliminadas filtradas **")
    print("** 11. Limpiar el sistema                  **")
    print("** 12. Salir                               **")
    print("*********************************************")

def mostrar_menu_usuarios():
    """Muestra el menú de gestión de usuarios."""
    print("\n*********************************************")
    print("**        Gestión de Usuarios              **")
    print("*********************************************")
    print("** 1. Agregar un usuario                   **")
    print("** 2. Modificar un usuario                 **")
    print("** 3. Eliminar un usuario                  **")
    print("** 4. Listar todos los usuarios            **")
    print("** 5. Gestionar tareas                     **")
    print("*********************************************")

def gestionar_usuarios():
    """Función de menú para la gestión de usuarios."""
    gestor_usuarios = GestorUsuarios()

    while True:
        mostrar_menu_usuarios()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nickname = input("Ingrese el nickname del usuario: ")
            clave = input("Ingrese la clave del usuario: ")
            email = input("Ingrese el email del usuario: ")
            tipo = input("Ingrese el tipo del usuario (user/admin): ")
            zona_horaria = input("Ingrese la zona horaria del usuario (e.g., UTC, America/New_York): ")
            gestor_usuarios.agregar_usuario(nickname, clave, email, tipo, zona_horaria)
            print("*********************************************")
            print("** Usuario agregado exitosamente.          **")
            print("*********************************************")
        elif opcion == "2":
            id_user = input("Ingrese el ID del usuario a modificar: ")
            campo = input("Ingrese el campo a modificar (nickname, clave, email, estado, pertenece, pertenece_a, tipo, zona_horaria): ")
            valor = input(f"Ingrese el nuevo valor para {campo}: ")
            if campo == "estado" or campo == "pertenece":
                valor = valor.lower() == 'true'
            if gestor_usuarios.modificar_usuario(id_user, **{campo: valor}):
                print("*********************************************")
                print("** Usuario modificado exitosamente.         **")
                print("*********************************************")
            else:
                print("*********************************************")
                print("** Usuario no encontrado.                  **")
                print("*********************************************")
        elif opcion == "3":
            id_user = input("Ingrese el ID del usuario a eliminar: ")
            gestor_usuarios.eliminar_usuario(id_user)
            print("*********************************************")
            print("** Usuario eliminado.                      **")
            print("*********************************************")
        elif opcion == "4":
            print("*********************************************")
            print("**        Lista de Usuarios                **")
            print("*********************************************")
            gestor_usuarios.listar_usuarios()
            print("*********************************************")
            input("Presione Enter para volver al menú...")
        elif opcion == "5":
            break
        else:
            print("*********************************************")
            print("** Opción no válida, intente de nuevo.     **")
            print("*********************************************")

def login():
    """Función de inicio de sesión."""
    gestor_usuarios = GestorUsuarios()
    while True:
        print("*********************************************")
        print("**          Iniciar Sesión                **")
        print("*********************************************")
        nickname = input("Usuario: ")
        clave = input("Clave: ")
        for usuario in gestor_usuarios.usuarios:
            if usuario.nickname == nickname and usuario.clave == clave:
                print("*********************************************")
                print(f"** Bienvenido {nickname}!                   **")
                print("*********************************************")
                if usuario.tipo == "admin":
                    gestionar_usuarios()
                menu_tareas(usuario.id_user, usuario.nickname, usuario.tipo)
                return
        print("*********************************************")
        print("** Usuario o clave incorrecta.             **")
        print("*********************************************")

def menu_tareas(id_usuario, nickname, tipo_usuario):
    """Función de menú para la interfaz de consola."""
    lista_de_tareas = ListaDeTareas()

    def iniciar_api():
        """Función para iniciar la API Flask en un proceso separado."""
        global api_process
        if api_process is None:
            api_process = Process(target=ejecutar_api)
            api_process.start()
            print("*********************************************")
            print("** API iniciada en http://127.0.0.1:5000   **")
            print("*********************************************")
        else:
            print("*********************************************")
            print("** La API ya está en ejecución.            **")
            print("*********************************************")

    def detener_api():
        """Función para detener la API Flask."""
        global api_process
        if api_process is not None:
            api_process.terminate()
            api_process.join()
            api_process = None
            print("*********************************************")
            print("** API detenida.                           **")
            print("*********************************************")
        else:
            print("*********************************************")
            print("** La API no está en ejecución.            **")
            print("*********************************************")
    
    def estado_api():
        """Función para mostrar el estado de la API."""
        global api_process
        estado = "activa" if api_process is not None else "inactiva"
        print("*********************************************")
        print(f"** Estado de la API: {estado}.              **")
        print("*********************************************")

    while True:
        print(f"\nUsuario: {nickname}")
        if tipo_usuario == "admin":
            mostrar_menu_admin()
        else:
            mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            descripcion = input("Descripción de la nueva tarea: ")
            tipo = input("¿Es una tarea importante? (True/False): ").lower() == 'true'
            compartida = input("¿La tarea es compartida? (True/False): ").lower() == 'true'
            compartida_con = input("IDs de usuarios con quienes se comparte (separados por coma): ") if compartida else ""
            dependiente = input("¿La tarea depende de otra? (True/False): ").lower() == 'true'
            dependiente_de = input("IDs de tareas de las que depende (separados por coma): ") if dependiente else ""
            lista_de_tareas.agregar_tarea(descripcion, tipo, id_usuario, compartida, compartida_con, dependiente, dependiente_de)
            print("*********************************************")
            print("** Tarea agregada exitosamente.            **")
            print("*********************************************")
        elif opcion == "2":
            try:
                id_sec2 = int(input("ID de la tarea a marcar como completada (id_sec2): "))
                lista_de_tareas.marcar_tarea_completada(id_sec2, id_usuario)
            except ValueError:
                print("*********************************************")
                print("** Error: Debe ingresar un número.         **")
                print("*********************************************")
        elif opcion == "3":
            print("*********************************************")
            print("**        Lista de Tareas                  **")
            print("*********************************************")
            lista_de_tareas.mostrar_tareas(id_usuario, tipo_usuario)
            print("*********************************************")
            input("Presione Enter para volver al menú...")
        elif opcion == "4":
            try:
                id_sec2 = int(input("ID de la tarea a eliminar (id_sec2): "))
                lista_de_tareas.eliminar_tarea(id_sec2, id_usuario)
            except ValueError:
                print("*********************************************")
                print("** Error: Debe ingresar un número.         **")
                print("*********************************************")
        elif opcion == "5":
            if tipo_usuario == "admin":
                iniciar_api()
            else:
                print("*********************************************")
                print("** Opción no permitida para usuarios.      **")
                print("*********************************************")
        elif opcion == "6":
            if tipo_usuario == "admin":
                detener_api()
            else:
                print("*********************************************")
                print("** Opción no permitida para usuarios.      **")
                print("*********************************************")
        elif opcion == "7":
            estado_api()
        elif opcion == "8":
            print("*********************************************")
            print("**      Tareas Eliminadas                  **")
            print("*********************************************")
            lista_de_tareas.mostrar_tareas_eliminadas(id_usuario, tipo_usuario)
            print("*********************************************")
            input("Presione Enter para volver al menú...")
        elif opcion == "9":
            dia = input("Ingrese el día (dd/mm/yyyy) [deje en blanco para omitir]: ")
            mes = input("Ingrese el mes (mm) [deje en blanco para omitir]: ")
            semana = input("Ingrese la semana (número entero) [deje en blanco para omitir]: ")
            year = input("Ingrese el año (yyyy) [deje en blanco para omitir]: ")
            try:
                lista_de_tareas.filtrar_tareas(id_usuario, tipo_usuario, dia=dia if dia else None, mes=mes if mes else None, semana=semana if semana else None, year=year if year else None)
            except ValueError as e:
                print(f"*********************************************\n** {e} **\n*********************************************")
            input("Presione Enter para volver al menú...")
        elif opcion == "10":
            dia = input("Ingrese el día (dd/mm/yyyy) [deje en blanco para omitir]: ")
            mes = input("Ingrese el mes (mm) [deje en blanco para omitir]: ")
            semana = input("Ingrese la semana (número entero) [deje en blanco para omitir]: ")
            year = input("Ingrese el año (yyyy) [deje en blanco para omitir]: ")
            try:
                lista_de_tareas.filtrar_tareas_eliminadas(id_usuario, tipo_usuario, dia=dia if dia else None, mes=mes if mes else None, semana=semana if semana else None, year=year if year else None)
            except ValueError as e:
                print(f"*********************************************\n** {e} **\n*********************************************")
            input("Presione Enter para volver al menú...")
        elif opcion == "11" and tipo_usuario == "admin":
            lista_de_tareas.limpiar_sistema()
        elif opcion == "12" and tipo_usuario == "admin":
            detener_api()
            break
        elif opcion == "11" and tipo_usuario != "admin":
            print("*********************************************")
            print("** Opción no válida, intente de nuevo.     **")
            print("*********************************************")
        elif opcion == "12":
            break
        else:
            print("*********************************************")
            print("** Opción no válida, intente de nuevo.     **")
            print("*********************************************")

if __name__ == "__main__":
    api_process = None
    login()
