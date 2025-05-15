from app.modulos.principal import principal
from app.utilidades.recursos import autentificar, login_requerido
from flask import render_template, request, redirect, url_for, flash, session

@principal.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        cedula = request.form["cedula"]
        contra = request.form["contra"]
        respuesta = autentificar(cedula,contra)
        if respuesta["exito"]:
            return redirect(url_for('principal.dashboard'))
        else:
            flash(respuesta["mensaje"],respuesta["tipo"])
            return redirect(url_for('principal.login'))
    if session.get('id_usuario'):
        return redirect(url_for('principal.dashboard'))
    return render_template("principal/login.html")

@principal.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('principal.login'))

@principal.route('/dashboard')
@login_requerido
def dashboard():
    return render_template("principal/dashboard.html")

@principal.route('/ley50')
@login_requerido
def ley50():
    return render_template("principal/ley50.html")

@principal.route('/gestion')
@login_requerido
def gestion():
    return render_template("principal/ley50.html")

@principal.route('/administracion')
@login_requerido
def administracion():
    return render_template("principal/ley50.html")