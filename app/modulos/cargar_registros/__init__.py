from flask import Blueprint
from app.modulos.cargar_registros.eventos_temp import eventos_temp_bp

cargar_registros_bp = Blueprint('cargar_registros',__name__)

cargar_registros_bp.register_blueprint(eventos_temp_bp,url_prefix='/evento_temp')

from app.modulos.cargar_registros import rutas