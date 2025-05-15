from flask import Flask, send_from_directory
from dotenv import load_dotenv
import os
from app.utilidades.recursos import login_requerido

load_dotenv()

def crear_app():
    app = Flask(__name__)

    from app.modulos.consultar_registros import consultar_registros_bp
    from app.modulos.cargar_registros import cargar_registros_bp
    from app.modulos.administracion import administracion_bp
    from app.modulos.gestion import gestion_bp
    from app.modulos.principal import principal

    app.register_blueprint(consultar_registros_bp,url_prefix="/consultar_registros")
    app.register_blueprint(cargar_registros_bp,url_prefix="/crear_registros")
    app.register_blueprint(administracion_bp,url_prefix="/administracion")
    app.register_blueprint(gestion_bp,url_prefix="/gestion")
    app.register_blueprint(principal)

    app.secret_key=os.environ.get("SECRET_KEY")
    
    @app.errorhandler(404)
    @login_requerido
    def pagina_no_encontrada(error):
        return "Oops Esta página no existe :("
    
    @app.errorhandler(405)
    @login_requerido
    def metodo_incorrecto(error):
        return "Oops Este método no es válido :("
    
    @app.route('/descargar/<nombre_archivo>')
    @login_requerido
    def descargar_archivo(nombre_archivo):
        return send_from_directory(os.path.join('static','archivos'),nombre_archivo,as_attachment=True)

    return app