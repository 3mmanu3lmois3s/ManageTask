from flask import Flask, request, jsonify, render_template, session
from flasgger import Swagger, swag_from
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError
from ManageTask import ListaDeTareas, GestorUsuarios

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Usa una clave real en producción
app.config['WTF_CSRF_TIME_LIMIT'] = 1800  # 30 minutos expresados en segundos

# Configuración de CORS para permitir solicitudes desde el origen esperado
CORS(app, supports_credentials=True, resources={r"*": {"origins": "http://127.0.0.1:5577", "methods": ["GET", "POST", "PUT", "DELETE"], "allow_headers": ["Content-Type", "X-CSRFToken"]}})

# Inicialización de CSRF Protection
csrf = CSRFProtect(app)
csrf.init_app(app)

swagger = Swagger(app)

lista_de_tareas = ListaDeTareas()
gestor_usuarios = GestorUsuarios()

@app.route("/csrf-token", methods=["GET"])
def csrf_token():
    # Generar el token CSRF una sola vez
    csrf_token = generate_csrf()
    response = jsonify({'csrfToken': csrf_token})
    response.headers['X-CSRFToken'] = csrf_token
    return response

@app.after_request
def after_request(response):
    # Configuración de headers para CORS y CSRF
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CSRFToken')
    return response

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify(error=str(e.description)), 400

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify(error=str(e)), 400

@app.route("/login", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nickname': {'type': 'string'},
                    'clave': {'type': 'string'},
                    'token': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Login exitoso'},
        401: {'description': 'Usuario o clave incorrecta'}
    }
})
def login_usuario():
    data = request.get_json()
    nickname = data.get("nickname")
    clave = data.get("clave")
    token = data.get("token")

    if not token:
        usuario = next((u for u in gestor_usuarios.usuarios if u.nickname == nickname and u.clave == clave), None)
        if usuario:
            gestor_usuarios.enviar_token(usuario)
            return jsonify({
                "message": "Token enviado al email registrado."
            }), 200
        return jsonify({"message": "Usuario o clave incorrecta"}), 401
    else:
        if gestor_usuarios.validar_token(nickname, token):
            session['user'] = nickname  # Guardar el usuario en la sesión
            return jsonify({
                "message": "Login exitoso",
                "id_usuario": next(u.id_user for u in gestor_usuarios.usuarios if u.nickname == nickname),
                "nickname": nickname,
                "tipo": next(u.tipo for u in gestor_usuarios.usuarios if u.nickname == nickname)
            }), 200
        return jsonify({"message": "Token inválido o expirado"}), 401

@app.route("/logout", methods=["POST"])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nickname': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Logout exitoso'},
        401: {'description': 'Usuario no encontrado'}
    }
})
def logout_usuario():
    data = request.get_json()
    nickname = data.get("nickname")
    session.pop('user', None)  # Eliminar usuario de la sesión
    for usuario in gestor_usuarios.usuarios:
        if usuario.nickname == nickname:
            usuario.token = None
            usuario.token_expiracion = None
            gestor_usuarios.guardar_usuarios()
            return jsonify({"message": "Logout exitoso"}), 200
    return jsonify({"message": "Usuario no encontrado"}), 401

def verificar_token(func):
    def wrapper(*args, **kwargs):
        data = request.get_json()
        nickname = data.get("nickname")
        token = data.get("token")
        if gestor_usuarios.validar_token(nickname, token):
            return func(*args, **kwargs)
        return jsonify({"message": "Token inválido o expirado"}), 401
    wrapper.__name__ = func.__name__
    return wrapper

@swag_from({
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tipo_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Lista de tareas'}
    }
})
@app.route("/tareas", methods=["GET"])
@verificar_token
def obtener_tareas():
    data = request.get_json()
    id_usuario = request.args.get("id_usuario")
    tipo_usuario = request.args.get("tipo_usuario")
    lista_de_tareas.cargar_tareas()
    tareas = [tarea.to_dict() for tarea in lista_de_tareas.tareas if tarea.estado != 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con)]
    return jsonify(tareas)

@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'descripcion': {'type': 'string'},
                    'tipo': {'type': 'boolean'},
                    'id_usuario': {'type': 'string'},
                    'compartida': {'type': 'boolean'},
                    'compartida_con': {'type': 'string'},
                    'dependiente': {'type': 'boolean'},
                    'dependiente_de': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Tarea agregada correctamente'},
        400: {'description': 'Descripción e ID de usuario son requeridos'}
    }
})
@app.route("/tareas", methods=["POST"])
@verificar_token
def agregar_tarea():
    data = request.get_json()
    descripcion = data.get("descripcion")
    tipo = data.get("tipo", False)
    id_usuario = data.get("id_usuario")
    compartida = data.get("compartida", False)
    compartida_con = data.get("compartida_con", "")
    dependiente = data.get("dependiente", False)
    dependiente_de = data.get("dependiente_de", "")
    if descripcion and id_usuario:
        lista_de_tareas.cargar_tareas()
        lista_de_tareas.agregar_tarea(descripcion, tipo, id_usuario, compartida, compartida_con, dependiente, dependiente_de)
        return jsonify({"message": "Tarea agregada correctamente"}), 201
    return jsonify({"message": "Descripción e ID de usuario son requeridos"}), 400

@swag_from({
    'parameters': [
        {
            'name': 'id_sec2',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_usuario': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Tarea marcada como completada'},
        404: {'description': 'Tarea no encontrada'},
        400: {'description': 'ID de usuario es requerido'}
    }
})
@app.route("/tareas/<int:id_sec2>", methods=["PUT"])
@verificar_token
def marcar_tarea_completada(id_sec2):
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    if id_usuario:
        try:
            lista_de_tareas.cargar_tareas()
            lista_de_tareas.marcar_tarea_completada(id_sec2, id_usuario)
            return jsonify({"message": "Tarea marcada como completada"}), 200
        except StopIteration:
            return jsonify({"message": "Tarea no encontrada"}), 404
    return jsonify({"message": "ID de usuario es requerido"}), 400

@swag_from({
    'parameters': [
        {
            'name': 'id_sec2',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_usuario': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Tarea eliminada correctamente'},
        404: {'description': 'Tarea no encontrada'},
        400: {'description': 'ID de usuario es requerido'}
    }
})
@app.route("/tareas/<int:id_sec2>", methods=["DELETE"])
@verificar_token
def eliminar_tarea(id_sec2):
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    if id_usuario:
        try:
            lista_de_tareas.cargar_tareas()
            lista_de_tareas.eliminar_tarea(id_sec2, id_usuario)
            return jsonify({"message": "Tarea eliminada correctamente"}), 200
        except StopIteration:
            return jsonify({"message": "Tarea no encontrada"}), 404
    return jsonify({"message": "ID de usuario es requerido"}), 400

@swag_from({
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tipo_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Lista de tareas eliminadas'}
    }
})
@app.route("/tareas_eliminadas", methods=["GET"])
@verificar_token
def obtener_tareas_eliminadas():
    id_usuario = request.args.get("id_usuario")
    tipo_usuario = request.args.get("tipo_usuario")
    lista_de_tareas.cargar_tareas()
    tareas = [tarea.to_dict() for tarea in lista_de_tareas.tareas if tarea.estado == 'e' and (tipo_usuario == "admin" or tarea.id_usuario == id_usuario or id_usuario in tarea.compartida_con)]
    return jsonify(tareas)

@swag_from({
    'responses': {
        200: {'description': 'Lista de usuarios'}
    }
})
@app.route("/usuarios", methods=["GET"])
@verificar_token
def obtener_usuarios():
    return jsonify([usuario.to_dict() for usuario in gestor_usuarios.usuarios])

@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nickname': {'type': 'string'},
                    'clave': {'type': 'string'},
                    'email': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'zona_horaria': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Usuario agregado correctamente'},
        400: {'description': 'Nickname, clave y email son requeridos'}
    }
})
@app.route("/usuarios", methods=["POST"])
@verificar_token
def agregar_usuario():
    data = request.get_json()
    nickname = data.get("nickname")
    clave = data.get("clave")
    email = data.get("email")
    tipo = data.get("tipo", "user")
    zona_horaria = data.get("zona_horaria", "UTC")
    if nickname and clave and email:
        gestor_usuarios.agregar_usuario(nickname, clave, email, tipo, zona_horaria)
        return jsonify({"message": "Usuario agregado correctamente"}), 201
    return jsonify({"message": "Nickname, clave y email son requeridos"}), 400

@swag_from({
    'parameters': [
        {
            'name': 'id_user',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object'
            }
        }
    ],
    'responses': {
        200: {'description': 'Usuario modificado correctamente'},
        404: {'description': 'Usuario no encontrado'}
    }
})
@app.route("/usuarios/<id_user>", methods=["PUT"])
@verificar_token
def modificar_usuario(id_user):
    data = request.get_json()
    if gestor_usuarios.modificar_usuario(id_user, **data):
        return jsonify({"message": "Usuario modificado correctamente"}), 200
    return jsonify({"message": "Usuario no encontrado"}), 404

@swag_from({
    'parameters': [
        {
            'name': 'id_user',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Usuario eliminado correctamente'}
    }
})
@app.route("/usuarios/<id_user>", methods=["DELETE"])
@verificar_token
def eliminar_usuario(id_user):
    gestor_usuarios.eliminar_usuario(id_user)
    return jsonify({"message": "Usuario eliminado correctamente"}), 200

@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_usuario': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Sistema limpiado correctamente'},
        403: {'description': 'Acceso denegado'}
    }
})
@app.route("/limpiar_sistema", methods=["POST"])
@verificar_token
def limpiar_sistema():
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    usuario = next((u for u in gestor_usuarios.usuarios if u.id_user == id_usuario), None)
    if usuario and usuario.tipo == "admin":
        lista_de_tareas.limpiar_sistema()
        return jsonify({"message": "Sistema limpiado correctamente"}), 200
    return jsonify({"message": "Acceso denegado"}), 403

@swag_from({
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tipo_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'dia',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'mes',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'semana',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'year',
            'in': 'query',
            'type': 'string'
        }
    ],
    'responses': {
        200: {'description': 'Lista de tareas filtradas'},
        400: {'description': 'Error en los parámetros'},
        500: {'description': 'Error al filtrar tareas'}
    }
})
@app.route("/tareas_filtradas", methods=["GET"])
@verificar_token
def obtener_tareas_filtradas():
    id_usuario = request.args.get("id_usuario")
    tipo_usuario = request.args.get("tipo_usuario")
    dia = request.args.get("dia")
    mes = request.args.get("mes")
    semana = request.args.get("semana")
    year = request.args.get("year")

    try:
        tareas = lista_de_tareas.filtrar_tareas(id_usuario, tipo_usuario, dia=dia, mes=mes, semana=semana, year=year)
        return jsonify([tarea.to_dict() for tarea in tareas])
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Error al filtrar tareas", "error": str(e)}), 500

@swag_from({
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'tipo_usuario',
            'in': 'query',
            'type': 'string',
            'required': True
        },
        {
            'name': 'dia',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'mes',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'semana',
            'in': 'query',
            'type': 'string'
        },
        {
            'name': 'year',
            'in': 'query',
            'type': 'string'
        }
    ],
    'responses': {
        200: {'description': 'Lista de tareas eliminadas filtradas'},
        400: {'description': 'Error en los parámetros'}
    }
})
@app.route("/tareas_eliminadas_filtradas", methods=["GET"])
@verificar_token
def obtener_tareas_eliminadas_filtradas():
    id_usuario = request.args.get("id_usuario")
    tipo_usuario = request.args.get("tipo_usuario")
    dia = request.args.get("dia")
    mes = request.args.get("mes")
    semana = request.args.get("semana")
    year = request.args.get("year")

    try:
        tareas = lista_de_tareas.filtrar_tareas_eliminadas(id_usuario, tipo_usuario, dia=dia, mes=mes, semana=semana, year=year)
        return jsonify([tarea.to_dict() for tarea in tareas])
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
