from flask import Blueprint

administracion_bp = Blueprint("administracion",__name__)

from app.modulos.administracion import rutas