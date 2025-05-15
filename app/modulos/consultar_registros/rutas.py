from app.modulos.consultar_registros import consultar_registros_bp
from flask import render_template, request, jsonify, redirect, url_for, flash
from app.utilidades.recursos import login_requerido, hacer_busqueda_evento, hacer_busqueda_empleado, seleccionar_empleado, seleccionar_evento, hacer_busqueda_de_asistencias

# La ruta principal

@consultar_registros_bp.route('/')
@login_requerido
def consultar_registros():
    return render_template('consultar_registros/consultar_registros.html')

# Ejecuta una busqueda

@consultar_registros_bp.route('/busqueda_registros_por_tipo')
@login_requerido
def busqueda_registros_por_tipo():
    try:
        busqueda = request.args.get('busqueda')
        tipo = int(request.args.get('tipo'))
        if tipo == 1:
            resultado = hacer_busqueda_evento(busqueda)
        elif tipo == 2:
            resultado = hacer_busqueda_empleado(busqueda)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros de búsqueda"})
    
# Carga los detalles de un empleado o un evento según sea el caso
    
@consultar_registros_bp.route('/detalles/<string:tipo>/<int:id>')
@login_requerido
def detalles_empleado(tipo,id):
    try:
        if tipo == 'empleado':
            seleccion = seleccionar_empleado(id)
            template = 'consultar_registros/detalles_empleado.html'
            conflictos = 0
        elif tipo == 'evento':
            seleccion = seleccionar_evento(id)
            template = 'consultar_registros/detalles_evento.html'
            conflictos =seleccion["conflictos"]
        if not seleccion["exito"]:
            flash(seleccion["mensaje"],"error")
            return redirect(url_for('consultar_registros.consultar_registros'))
        if not seleccion["datos"]:
            flash("No se han encontrado los datos solicitados","advertencia")
            return redirect(url_for('consultar_registros.consultar_registros'))
        return render_template(template, resultados=seleccion["datos"],conflictos= conflictos)
    except:
        flash('Error al obtener los parámetros de búsqueda','error')
        return redirect(url_for('consultar_registros.consultar_registros'))

@consultar_registros_bp.route('/busqueda_de_asistencias')
@login_requerido
def busqueda_de_asistencias():
    try:
        segun = request.args.get('segun')
        id= int(request.args.get('id'))
        if segun == 'evento':
            clave = request.args.get('inf'), request.args.get('sup')
        elif segun == 'empleado':
            clave = request.args.get('busqueda')
        else:
            return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros de búsqueda"})
        resultados = hacer_busqueda_de_asistencias(segun,id,clave)
        return jsonify(resultados)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado al obtener los parámetros de búsqueda"})