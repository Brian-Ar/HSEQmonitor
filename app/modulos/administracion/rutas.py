from app.modulos.administracion import administracion_bp
from flask import render_template, jsonify, request
from app.utilidades.recursos import login_requerido,admin_requerido, seleccionar_usuarios, empl_sin_usuarios, edicion_actualizacion, eliminacion_us

# @administracion_bp.route('/')
# @login_requerido
# @admin_requerido
# def admin():
#     return render_template('admin/admin.html')

####################
# SECCION USUARIOS #
####################

@administracion_bp.route('/usuarios')
@login_requerido
@admin_requerido
def usuarios():
    return render_template('admin/usuarios.html')

@administracion_bp.route('/cargar_usuarios')
@login_requerido
@admin_requerido
def cargar_usuarios():
    resultados = seleccionar_usuarios()
    return jsonify(resultados)

@administracion_bp.route('/buscar_empleado')
@login_requerido
@admin_requerido
def buscar_empleado():
    try:
        busqueda = request.args.get('busqueda')
        if not busqueda:
            return jsonify({"exito":True,"datos":[]})
        resultado = empl_sin_usuarios(busqueda)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros de búsqueda"})
    
@administracion_bp.route('/confirmar_form_usuario', methods=['POST'])
@login_requerido
@admin_requerido
def confirmar_form_usuario():
    try:
        datos = request.get_json()
        id_persona = datos['id_persona']
        cedula = datos['cedula']
        nombre = datos['nombre']
        correo = datos['correo']
        tipo = datos['tipo']
        if not id_persona or not cedula or not nombre or not tipo:
            return jsonify({"exito":False,"mensaje":"Ningún campo con * puede estar vacío"})
        if tipo != 'Regular' and tipo != 'Administrador':
            return jsonify({"exito":False,"mensaje":"Tipo de usuario incorrecto"})
        resultado = edicion_actualizacion(id_persona,cedula,nombre,correo,tipo)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener los parámetros"})


@administracion_bp.route('/eliminar_usuario', methods=['POST'])
@login_requerido
@admin_requerido
def eliminar_usuario():
    try:
        datos = request.get_json()
        id_us = int(datos["id_us"])
        resultado = eliminacion_us(id_us)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener los parámetros"})
    
