from app.modulos.cargar_registros.eventos_temp import eventos_temp_bp
from app.utilidades.recursos import login_requerido, cargar_detalles_evento_temp, cargar_asis_temp, eliminar_asistente_temporal, hacer_busqueda_empleado, agregar_asistente_temporal, editar_evento_temporal, confirmar_evento_temporal
from flask import render_template,redirect,url_for,flash,jsonify, request

@eventos_temp_bp.route('/<int:id_ev_temp>')
@login_requerido
def evento_temp(id_ev_temp):
    if not id_ev_temp:
        flash("Error al obtener el id del evento","error")
        return redirect(url_for('cargar_registros.formato_fisico'))
    resultados = cargar_detalles_evento_temp(id_ev_temp)
    if not resultados["exito"]:
        flash(resultados["mensaje"],"error")
        return redirect(url_for('cargar_registros.formato_fisico'))
    return render_template('cargar_registros/ver_form_temp.html', resultados=resultados["datos"])

@eventos_temp_bp.route('/cargar_tabla_asis_temp')
@login_requerido
def cargar_tabla_asis_temp():
    try:
        id = int(request.args.get('id_ev_temp'))
        resultados = cargar_asis_temp(id)
        return jsonify(resultados)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener el id del evento temporal"})
    
@eventos_temp_bp.route('/eliminar_asis_temp', methods=['POST'])
@login_requerido
def eliminar_asis_temp():
    try:
        datos = request.get_json()
        id_evento= int(datos['id_evento'])
        id_emp = int(datos['id_emp'])
        resultado = eliminar_asistente_temporal(id_evento,id_emp)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener al obtener los parámetros requeridos"})
    
@eventos_temp_bp.route('/buscar_empleado')
@login_requerido
def buscar_empleado():
    try:
        busqueda = request.args.get('busqueda')
        if not busqueda:
            return jsonify({"exito":True,"datos":[]})
        resultado = hacer_busqueda_empleado(busqueda)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros de búsqueda"})
    
@eventos_temp_bp.route('/agregar_asis_temp',methods=['POST'])
@login_requerido
def agregar_asis_temp():
    try:
        datos = request.get_json()
        id_evento = int(datos['id_evento'])
        id_emp = int(datos['id_emp'])
        resultado = agregar_asistente_temporal(id_evento,id_emp)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener al obtener los parámetros requeridos"})

@eventos_temp_bp.route('/editar_evento_temp',methods=['POST'])
@login_requerido
def editar_encabezado_ev_temp():
    try:
        datos = request.get_json()
        id_evento = datos['id_evento']
        fecha = datos['fecha']
        titulo=datos['titulo']
        duracion = int(datos['duracion'])
        if not id_evento or not fecha or not titulo or not duracion:
            return jsonify({"exito":False,"mensaje":"Ningún campo puede quedar vacío"})
        resultados = editar_evento_temporal(id_evento,fecha,titulo,duracion)
        return jsonify(resultados)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener al obtener los parámetros requeridos"})
    

@eventos_temp_bp.route('/confirmar_evento_temp', methods=['POST'])
@login_requerido
def confirmar_evento_temp():
    try:
        id_evento = request.form['id_evento']
        if not id_evento:
            flash("Error al seleccionar el id del evento","error")
            return redirect(url_for('cargar_registros.formato_fisico'))
        resultado = confirmar_evento_temporal(id_evento)
        if not resultado['exito']:
            flash(resultado['mensaje'],"error")
            return redirect(url_for('cargar_registros.formato_fisico'))
        return redirect(url_for('consultar_registros.consultar_registros'))
    except:
        flash("Error al obtener los parámetros","error")
        return redirect(url_for('cargar_registros.formato_fisico'))