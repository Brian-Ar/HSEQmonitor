from app.modulos.gestion import gestion_bp
from flask import render_template, jsonify, request, redirect, url_for, flash
from app.utilidades.recursos import login_requerido, hacer_busqueda_empleado, empl_desde_excel, crear_empleado_manual, conf_edi_empl, conf_eli_empl, transformar, seleccionar_conflictos, seleccionar_conflicto_especifico

@gestion_bp.route('/')
@login_requerido
def gestion():
    return render_template('gestion/gestion.html')

#####################
# SECCION EMPLEADOS #
#####################

@gestion_bp.route('/empleados')
@login_requerido
def empleados():
    return render_template('/gestion/empleados.html')

@gestion_bp.route('/cargar_empleados')
@login_requerido
def cargar_empleados():
    resultado = hacer_busqueda_empleado('')
    if resultado["datos"]:
        resultado["datos"] = transformar(resultado["datos"])    
    return jsonify(resultado)

@gestion_bp.route('/cargar_archivo_empl', methods=['POST'])
@login_requerido
def cargar_archivo_empl():
    if 'archivo' not in request.files:
        return jsonify({'exito':False,"mensaje":"Sin archivo seleccionado"})
    archivo = request.files['archivo']
    if archivo.filename == '':
        return jsonify({'exito':False,"mensaje":"Sin archivo seleccionado"})
    resultado=empl_desde_excel(archivo)
    return jsonify(resultado)

@gestion_bp.route('/empleado_manual', methods=['POST'])
@login_requerido
def empleado_manual():
    try:
        datos = request.get_json()
        cedula = datos['cedula']
        nombre = datos['nombre']
        if not cedula or not nombre:
            return jsonify({"exito":False,"mensaje":"Ningún campo puede estar vacío"})
        resultado = crear_empleado_manual(cedula,nombre)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error al obtener los parámetros solicitados"})
 
@gestion_bp.route('/edicion_empl', methods=['POST'])
@login_requerido
def edicion_empl():
    try:
        datos = request.get_json()
        id_emp = int(datos['id_emp'])
        cedula = datos['cedula']
        nombre = datos['nombre']
        if not id_emp or not cedula or not nombre:
            return jsonify({"exito":False,"mensaje":"Ningún campo puede estar vacío"})
        resultado = conf_edi_empl(id_emp,cedula,nombre)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error obteniendo los parámetros"})

@gestion_bp.route('/eliminar_empl', methods = ['POST'])
@login_requerido
def eliminar_empl():
    try:
        datos = request.get_json()
        id_emp = int(datos['id_emp'])
        if not id_emp:
            return jsonify({"exito":False,"mensaje":"Error con el id del empleado"})
        resultado = conf_eli_empl(id_emp)
        return jsonify(resultado)
    except:
        return jsonify({"exito":False,"mensaje":"Error inesperado con los parámetros"})
    
######################
# SECCION CONFLICTOS #
######################

@gestion_bp.route('/conflictos')
@gestion_bp.route('/conflictos/<int:id_ev>')
@login_requerido
def conflictos(id_ev=None):
    if id_ev is None:
        resultados = seleccionar_conflictos()
        if resultados["exito"]:
            return render_template ('/gestion/conflictos.html', eventos = resultados["eventos"])
        flash(resultados["mensaje"],"error")
        return redirect(url_for('gestion.gestion'))
    resultados = seleccionar_conflicto_especifico(id_ev)
    if not resultados["exito"]:
        flash(resultados["mensaje"],"error")
        return redirect(url_for('gestion.conflictos'))
    if not resultados["evento"] or not resultados["conflictos"]:
        flash("Este evento no existe o no tiene conflictos","advertencia")
        return redirect(url_for('gestion.conflictos'))
    return render_template('gestion/conflictos_detalle.html',evento=resultados["evento"],conflictos=resultados["conflictos"],total=len(resultados["conflictos"]))