from flask import Blueprint

eventos_temp_bp = Blueprint("eventos_temp",__name__)

from app.modulos.cargar_registros.eventos_temp import rutas