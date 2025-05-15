from app.modulos.cargar_registros import cargar_registros_bp
from app.utilidades.recursos import login_requerido, crear_evento_temporal, cargar_eventos_temporales, eliminar_evento_temporal, hacer_tabla_json, confirmar_cargar_asis_excel
from flask import render_template, jsonify, request, session, json, flash, redirect,url_for

# Carga la plantilla principal de cargar registros

@cargar_registros_bp.route('/')
@login_requerido
def cargar_registros():
    return render_template('cargar_registros/cargar_registros.html')

##################
# FORMÁTO FÍSICO #
##################

# Plantilla del formáto físico

# @cargar_registros_bp.route('/formato_fisico')
# @login_requerido
# def formato_fisico():
#     return render_template('cargar_registros/formato_fisico.html')

# Carga los evento temporales

@cargar_registros_bp.route('/cargar_eventos_temp')
@login_requerido
def cargar_eventos_temp():
    resultados = cargar_eventos_temporales()
    return jsonify(resultados)

# Crea un formato físico (evento temporal)

@cargar_registros_bp.route('/crear_formato_fisico',methods=["POST"])
@login_requerido
def crear_formato_fisico():
    try:
        datos = request.get_json()
        if not datos['titulo'] or not datos['fecha'] or not datos['duracion']:
            return jsonify({"exito":False,"mensaje":"Ningún campo puede estar vacío"})
        resultado = crear_evento_temporal(datos)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros ingresados"})
    
# Elimina un evento temporal

@cargar_registros_bp.route('/eliminar_evento_temp', methods=["POST"])
@login_requerido
def eliminar_evento_temp():
    try:
        datos = request.get_json()
        id = int(datos["id_evento"])
        resultados = eliminar_evento_temporal(id)
        return jsonify(resultados)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros ingresados"})

###################
# FORMÁTO VIRTUAL #
###################

# @cargar_registros_bp.route('/formato_virtual')
# @login_requerido
# def formato_virtual():
#     return render_template('cargar_registros/formato_virtual.html')

@cargar_registros_bp.route('/cargar_excel', methods=["POST"])
@login_requerido
def cargar_excel():
    if 'archivo' not in request.files:
        return jsonify({'exito':False,"mensaje":"Sin archivo seleccionado"})
    archivo = request.files['archivo']
    resultado=hacer_tabla_json(archivo)
    if resultado["exito"]:
        session["tabla_temporal"]=resultado["datos"]
    return jsonify(resultado)

@cargar_registros_bp.route('/confirmar_carga_asis', methods=['POST'])
@login_requerido
def confirmar_carga_asis():
    try:
        datos = json.loads(session["tabla_temporal"])
        fecha = request.form['fecha_vir']
        titulo = request.form['titulo_vir']
        duracion = int(request.form['duracion_vir'])
        if not fecha or not titulo or not duracion:
            flash("Ningún campo puede estar vacío","advertencia")
            return redirect(url_for('cargar_registros.cargar_registros'))
        resultados = confirmar_cargar_asis_excel(datos,fecha, titulo, duracion)
        if not resultados["exito"]:
            flash(resultados["mensaje"],"error")
            return redirect(url_for('cargar_registros.cargar_registros'))
        flash("Datos cargados con exito","exito")
        return redirect(url_for('cargar_registros.cargar_registros'))
    except:
        flash("Error obteniendo los parámetros","error")
        return redirect(url_for('cargar_registros.cargar_registros'))
    