from app.utilidades.db import obten_conexion

def seleccionar_conflictos():
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT id_evento FROM asis_no_iden")
            eventos = cursor.fetchall()
            for evento in eventos:
                cursor.execute('SELECT fecha_ev,titulo_ev,duracion_ev FROM eventos WHERE id_evento = %s',[evento['id_evento']])
                detalles = cursor.fetchone()
                evento.update(detalles)
                cursor.execute('SELECT COUNT(*) AS conflictos FROM asis_no_iden WHERE id_evento = %s',[evento['id_evento']])
                conflictos = cursor.fetchone()
                evento.update(conflictos)
            return {"exito":True,"eventos":eventos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar los eventos"}
    finally:
        if conn:
            conn.close()
