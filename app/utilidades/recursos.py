from functools import wraps
from flask import session,redirect,url_for
from app.utilidades.db import obten_conexion
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd

# Decorador para proteger rutas

def login_requerido(f):
    @wraps(f)
    def comprobar(*args,**kwargs):
        if not session.get("id_usuario"):
            return redirect(url_for('principal.login'))
        return f(*args,**kwargs)
    return comprobar

# Decorador para proteger rutas del admin

def admin_requerido(f):
    @wraps(f)
    def comprobar(*args,**kwargs):
        if session.get('tipo_us') == 'Administrador':
            return f(*args,**kwargs)
        return redirect(url_for('principal.dashboard'))
    return comprobar

# Función para autentificar

def autentificar(cedula,contra):
    conn = obten_conexion()
    if conn is None:
        return {"exito":False,"mensaje":"Error al conectar con la base de datos","tipo":"error"}
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_empleado FROM empleados WHERE cedula_em = %s',[cedula])
        empleado = cursor.fetchone()
        if empleado:
            cursor.execute('SELECT * FROM usuarios WHERE id_usuario = %s',[empleado['id_empleado']])
            usuario = cursor.fetchone() 
            if usuario and check_password_hash(usuario['contra_us'],contra):
                session['id_usuario'] = usuario['id_usuario']
                session['tipo_us'] = usuario['tipo_us']
                return {"exito":True}             
        return {"exito":False,"mensaje":"Usuario o contraseña incorrecta","tipo":"advertencia"}

# Hace una busqueda de evento

def hacer_busqueda_evento(busqueda):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM eventos WHERE titulo_ev LIKE %s OR fecha_ev LIKE %s OR duracion_ev LIKE %s ORDER BY fecha_ev DESC",[f"%{busqueda}%",f"%{busqueda}%",f"%{busqueda}%"])
            datos_brutos=cursor.fetchall()
            datos= []
            for fila in datos_brutos:
                fila["fecha_ev"] = fila["fecha_ev"].isoformat()
                fila["conflictos"] = cursor.execute("SELECT * FROM asis_no_iden WHERE id_evento = %s",[fila["id_evento"]])
                datos.append(fila)
            if not datos:
                return {"exito": True, "datos": []}
            return {"exito": True, "datos": datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al buscar evento"}
    finally:
        if conn:
            conn.close()

# Hace una busqueda de empleado

def hacer_busqueda_empleado(busqueda):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM empleados WHERE cedula_em LIKE %s OR nombre_em LIKE %s ORDER BY id_empleado DESC", [f"%{busqueda}%", f"%{busqueda}%"])
            datos = cursor.fetchall()
            if not datos:
                return {"exito": True, "datos": []}
            return {"exito": True, "datos": datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al buscar empleado"}
    finally:
        if conn:
            conn.close()

# Seleccionar un empleado por id(cedula)

def seleccionar_empleado(id_em):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM empleados WHERE id_empleado = %s",[id_em])
            empleado = cursor.fetchone()
            if not empleado:
                return {"exito":True,"datos":[]}
            return {"exito":True,"datos":empleado}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar empleado"}
    finally:
        if conn:
            conn.close()

# Selecciona un empleado por id de evento

def seleccionar_evento(id_evento):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM eventos WHERE id_evento = %s",[id_evento])
            evento = cursor.fetchone()
            conflictos = cursor.execute("SELECT * FROM asis_no_iden WHERE id_evento = %s",[id_evento])
            if not evento:
                return {"exito":True,"datos":[],"conflictos":conflictos}
            return {"exito":True,"datos":evento,"conflictos":conflictos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar evento"}
    finally:
        if conn:
            conn.close()

# Hace una busqueda de asistencias segun (empleado, evento), id y la busqueda propiamente

def hacer_busqueda_de_asistencias(segun,id,busqueda):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            suma=0
            if segun == 'evento':
                inf = busqueda[0]
                sup = busqueda[1]
                if not inf and not sup:
                    inf = '1000-01-01'
                    sup = '9999-12-31'
                elif not inf and sup:
                    inf = '1000-01-01'
                elif inf and not sup:
                    sup='9999-12-31'
                cursor.execute("SELECT la.id_evento, ev.fecha_ev, ev.titulo_ev, ev.duracion_ev FROM lista_asis la JOIN eventos ev ON la.id_evento = ev.id_evento WHERE la.id_empleado = %s AND (ev.fecha_ev >= %s AND ev.fecha_ev <= %s)",[id,inf,sup])
                datos_brutos = cursor.fetchall()
                datos=[]
                for fila in datos_brutos:
                    fila["fecha_ev"] = fila["fecha_ev"].isoformat()
                    suma+=fila["duracion_ev"]
                    datos.append(fila)
            elif segun == 'empleado':
                cursor.execute('SELECT la.id_empleado, em.cedula_em ,em.nombre_em FROM lista_asis la JOIN empleados em ON la.id_empleado = em.id_empleado WHERE la.id_evento = %s AND (em.cedula_em LIKE %s OR em.nombre_em LIKE %s)',[id,f"%{busqueda}%",f"%{busqueda}%"])
                datos= cursor.fetchall()
            if not datos:
                return {"exito":True,"datos":[],"total_horas":0}
            return {"exito":True, "datos":datos,"total_horas":suma}     
    except:
        return {"exito":False,"mensaje":"Error inesperado al hacer la busqueda"}
    finally:
        if conn:
            conn.close()
            
# Se crea un evento temporal

def crear_evento_temporal(datos):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO eventos_temp (t_ev_temp, f_ev_temp, d_ev_temp) VALUES (%s,%s,%s)",[datos['titulo'],datos['fecha'],datos['duracion']])
            conn.commit()
        return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al crear el evento temporal"}
    finally:
        if conn:
            conn.close()
           
# Carga los eventos temporales

def cargar_eventos_temporales():
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM eventos_temp")
            datos_brutos = cursor.fetchall()
            datos = []
            for fila in datos_brutos:
                fila["f_ev_temp"] = fila["f_ev_temp"].isoformat()
                datos.append(fila)
            return {"exito":True,"datos":datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al cargar los eventos temporales"}
    finally:
        if conn:
            conn.close()

# Elimina un evento temporal y sus asistentes asociados

def eliminar_evento_temporal(id):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM lista_asis_temp WHERE id_evento_temp = %s",[id])
            cursor.execute("DELETE FROM eventos_temp WHERE id_evento_temp = %s",[id])
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al eliminar el evento temporal"}
    finally:
        if conn:
            conn.close()

# Carga los detalles de un evento temporal

def cargar_detalles_evento_temp(id):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM eventos_temp WHERE id_evento_temp = %s",[id])
            datos = cursor.fetchone()
            if not datos:
                return {"exito":False,"mensaje":"Evento temporal no encontrado"}
            return {"exito":True,"datos":datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al cargar el evento temporal"}
    finally:
        if conn:
            conn.close()

# Carga los asistentes del evento temporal

def cargar_asis_temp(id):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT lat.id_empleado, em.cedula_em, em.nombre_em FROM lista_asis_temp lat JOIN empleados em ON lat.id_empleado = em.id_empleado WHERE lat.id_evento_temp = %s",[id])
            datos = cursor.fetchall()
            return {"exito":True,"datos":datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al cargar el evento temporal"}
    finally:
        if conn:
            conn.close()

# Elimina un asistente del evento temporal

def eliminar_asistente_temporal(id_evento,id_emp):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM lista_asis_temp WHERE id_evento_temp = %s AND id_empleado = %s",[id_evento,id_emp])
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al eliminar al asistente del evento"}
    finally:
        if conn:
            conn.close()

# Agrega un asistente al evento temporal

def agregar_asistente_temporal(id_evento,id_emp):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute('SELECT * FROM lista_asis_temp WHERE id_evento_temp = %s AND id_empleado = %s',[id_evento,id_emp]):
                return {"exito":False,"mensaje":"Este empleado ya ha sido agregado"}
            cursor.execute('INSERT INTO lista_asis_temp (id_evento_temp,id_empleado) VALUES (%s,%s)',[id_evento,id_emp])
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al agregar al asistente al evento"}
    finally:
        if conn:
            conn.close()

# Edita el encabezado de un evento temporal

def editar_evento_temporal(id_ev,fecha,titulo,duracion):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("UPDATE eventos_temp SET t_ev_temp = %s, f_ev_temp = %s, d_ev_temp = %s WHERE id_evento_temp = %s",[titulo,fecha,duracion,id_ev])
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al editar el evento"}
    finally:
        if conn:
            conn.close()

# Da por finalizado el evento temporal y guarda todo

def confirmar_evento_temporal(id_ev):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM eventos_temp WHERE id_evento_temp = %s',[id_ev])
            evento_temp = cursor.fetchone()
            cursor.execute('INSERT INTO eventos (titulo_ev,fecha_ev,duracion_ev) VALUES (%s,%s,%s)',[evento_temp['t_ev_temp'],evento_temp['f_ev_temp'],evento_temp['d_ev_temp']])
            nuevo_id = cursor.lastrowid
            cursor.execute('SELECT id_empleado FROM lista_asis_temp WHERE id_evento_temp = %s',[id_ev])
            asistentes = cursor.fetchall()
            for asistente in asistentes:
                cursor.execute("INSERT INTO lista_asis (id_evento,id_empleado) VALUES (%s,%s)",[nuevo_id,asistente["id_empleado"]])
            cursor.execute('DELETE FROM lista_asis_temp WHERE id_evento_temp = %s',[id_ev])
            cursor.execute('DELETE FROM eventos_temp WHERE id_evento_temp = %s',[id_ev])
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al finalizar el evento"}
    finally:
        if conn:
            conn.close()

# Procesa el excel con asistencias 

def hacer_tabla_json(archivo):
    try:
        df = pd.read_excel(archivo,sheet_name=0)

        seleccion = df.iloc[:,[2,3]]
        seleccion.columns = ["nombre","cedula"]

        respuesta = seleccion.to_json(orient='records', force_ascii=False)

        return {"exito":True,"datos": respuesta}
    except:
        return {"exito":False,"mensaje":"Error inesperado al crear la tabla"}  

# Crea un evento con las asistencias del excel 

def confirmar_cargar_asis_excel(datos,fecha,titulo,duracion):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO eventos (fecha_ev,titulo_ev,duracion_ev) VALUES (%s,%s,%s)",[fecha,titulo,duracion])
            id_evento = cursor.lastrowid
            for dato in datos:
                if cursor.execute('SELECT * FROM empleados WHERE cedula_em = %s',[dato['cedula']]):
                    empl = cursor.fetchone()
                    cursor.execute('INSERT INTO lista_asis (id_evento,id_empleado) VALUES (%s,%s)',[id_evento,empl['id_empleado']])
                else:
                    cursor.execute("INSERT INTO asis_no_iden (id_evento,nombre_ingresado,cedula_ingresada) VALUES (%s,%s,%s)",[id_evento,dato['nombre'],dato['cedula']])
            conn.commit()
            session.pop('tabla_temporal')
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al guardar los datos"}
    finally:
        if conn:
            conn.close()

# Selecciona los datos de un usuario

def seleccionar_usuarios():
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute('SELECT us.id_usuario, em.cedula_em,em.nombre_em, us.correo_us, us.tipo_us FROM usuarios us JOIN empleados em ON us.id_usuario = em.id_empleado')
            datos=cursor.fetchall()
            return {"exito":True,"datos":datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar los usuarios"}
    finally:
        if conn:
            conn.close()

# Selecciona los empleados que no son usuarios

def empl_sin_usuarios(busqueda):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT em.id_empleado, em.cedula_em, em.nombre_em FROM empleados em LEFT JOIN usuarios us ON em.id_empleado = us.id_usuario WHERE us.id_usuario IS NULL AND (em.cedula_em LIKE %s OR em.nombre_em LIKE %s)", [f"%{busqueda}%", f"%{busqueda}%"])
            datos = cursor.fetchall()
            if not datos:
                return {"exito": True, "datos": []}
            return {"exito": True, "datos": datos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al buscar empleado"}
    finally:
        if conn:
            conn.close()

# Edita o crea un usuario según sea el caso

def edicion_actualizacion(id_persona,cedula,nombre,correo,tipo):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute('SELECT * FROM usuarios WHERE id_usuario = %s',[id_persona]):
                if cursor.execute('SELECT * FROM empleados WHERE cedula_em = %s and id_empleado <> %s',[cedula,id_persona]):
                    return {"exito":False,"mensaje":"Esta cédula ya está asignada a otro empleado"}
                cursor.execute('UPDATE usuarios SET correo_us = %s, tipo_us = %s WHERE id_usuario = %s',[correo,tipo, id_persona])
                cursor.execute('UPDATE empleados SET cedula_em = %s, nombre_em = %s WHERE id_empleado = %s',[cedula,nombre,id_persona])
            elif cursor.execute('SELECT * FROM empleados WHERE id_empleado = %s',[id_persona]):
                if cursor.execute('SELECT * FROM empleados WHERE cedula_em = %s and id_empleado <> %s',[cedula,id_persona]):
                    return {"exito":False,"mensaje":"Esta cédula ya está asignada a otro empleado"}
                cursor.execute('INSERT INTO usuarios (id_usuario,contra_us,correo_us,tipo_us) VALUES (%s,%s,%s,%s)',[id_persona,generate_password_hash(cedula),correo,tipo])
                cursor.execute('UPDATE empleados SET cedula_em = %s, nombre_em = %s WHERE id_empleado = %s',[cedula,nombre,id_persona])
            else:
                return {"exito":False,"mensaje":"Empleado o usuario inexistente"}
            conn.commit()
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al actualizar o agregar usuario"}
    finally:
        if conn:
            conn.close()

# Elimina un usuario

def eliminacion_us(id_us):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute('SELECT * FROM usuarios WHERE id_usuario = %s',[id_us]):
                cursor.execute('DELETE FROM usuarios WHERE id_usuario = %s',[id_us])
                conn.commit()
                return {"exito":True}
            return {"exito":False,"mensaje":"Usuario no encontrado"}
    except:
        return {"exito":False,"mensaje":"Error inesperado al eliminar el usuario"}
    finally:
        if conn:
            conn.close()

# Carga empleados desde un excel

def empl_desde_excel(archivo):
    try:
        df = pd.read_excel(archivo,header=None)

        encontrado = False

        for index, value in enumerate(df.iloc[:,0]):
            if value == 'CC':
                df = df.iloc[index:]
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
                encontrado = True
                break

        if not encontrado:
            return {"exito":False,"mensaje":"Error con el formato del archivo"}

        for index,value in enumerate(df.iloc[:,4]):
            if pd.isna(value):
                df = df.iloc[:index]

        df = df.iloc[:,0:2]
            
        empleados = df.to_dict(orient="records")
        
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}

        with conn.cursor() as cursor:
            for empleado in empleados:
                if not cursor.execute("SELECT * FROM empleados WHERE cedula_em = %s",[empleado["CC"]]):
                    cursor.execute("INSERT INTO empleados (cedula_em, nombre_em) VALUES (%s,%s)",[empleado["CC"],empleado["NOMBRE"]])
                    conn.commit()
                    resolver_conflictos(empleado["CC"])
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al cargar o procesar el archivo"}
    finally:
        if conn:
            conn.close()

# Crea un empleado manual

def crear_empleado_manual(cedula,nombre):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute("SELECT * FROM empleados WHERE cedula_em = %s",[cedula]):
                return {"exito":False,"mensaje":"Este empleado ya existe"}
            cursor.execute("INSERT INTO empleados (cedula_em,nombre_em) VALUES (%s,%s)",[cedula, nombre])
            conn.commit()
            resolver_conflictos(cedula)
            return {"exito":True}
    except:
        return {"exito":False,"mensaje":"Error inesperado al crear el empleado"}
    finally:
        if conn:
            conn.close()
            
def conf_edi_empl(id_emp,cedula,nombre):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute('SELECT * FROM empleados WHERE id_empleado = %s',[id_emp]):
                if cursor.execute('SELECT * FROM empleados WHERE cedula_em = %s AND id_empleado <> %s',[cedula,id_emp]):
                    return {"exito":False,"mensaje":"Esta cédula ya pertenece a otro empleado"}
                cursor.execute('UPDATE empleados SET cedula_em = %s, nombre_em = %s WHERE id_empleado = %s',[cedula,nombre,id_emp])
                conn.commit()
                return {"exito":True}
            return {"exito":False,"mensaje":"Este empleado no existe"}
    except:
        return {"exito":False,"mensaje":"Error inesperado al editar el empleado"}
    finally:
        if conn:
            conn.close()
     
def conf_eli_empl(id_emp):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar a la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute('SELECT * FROM empleados WHERE id_empleado = %s',[id_emp]):
                cursor.execute('DELETE FROM lista_asis_temp WHERE id_empleado = %s',[id_emp])
                cursor.execute('DELETE FROM lista_asis WHERE id_empleado = %s',[id_emp])
                cursor.execute('DELETE FROM usuarios WHERE id_usuario = %s',[id_emp])
                cursor.execute('DELETE FROM empleados WHERE id_empleado = %s',[id_emp])
                conn.commit()
                return {"exito":True}
            return {"exito":False,"mensaje":"Empleado no encontrado"}
    except:
        return {"exito":False,"mensaje":"Error inesperado al eliminar al empleado"}
    finally:
        if conn:
            conn.close()
            
def transformar(lista):
    conn = obten_conexion()
    if conn is None:
        return []
    with conn.cursor() as cursor:
        for empleado in lista:
            if cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s",[empleado["id_empleado"]]):
                empleado["es_usuario"] = True
            else:
                empleado["es_usuario"] = False
        return lista
    
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
            if not eventos:
                return {"exito":True,"eventos":[]}
            return {"exito":True,"eventos":eventos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar los eventos"}
    finally:
        if conn:
            conn.close()
            
def seleccionar_conflicto_especifico(id_ev):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectarse con la base de datos"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM eventos WHERE id_evento = %s",[id_ev])
            evento = cursor.fetchone()
            cursor.execute("SELECT * FROM asis_no_iden WHERE id_evento = %s",[id_ev])
            conflictos = cursor.fetchall()
            return {"exito":True,"evento":evento,"conflictos":conflictos}
    except:
        return {"exito":False,"mensaje":"Error inesperado al seleccionar el evento"}
    finally:
        if conn:
            conn.close()


def resolver_conflictos(cedula):
    try:
        conn = obten_conexion()
        if conn is None:
            return {"exito":False,"mensaje":"Error al conectar con la base de datos"}
        with conn.cursor() as cursor:
            if cursor.execute("SELECT id_empleado FROM empleados WHERE cedula_em = %s",[cedula]):
                resultado = cursor.fetchone()
                id_empleado = resultado["id_empleado"]
                if cursor.execute("SELECT * FROM asis_no_iden WHERE cedula_ingresada = %s",[cedula]):
                    conflictos = cursor.fetchall()
                    for conf in conflictos:
                        cursor.execute("INSERT INTO lista_asis (id_evento,id_empleado) VALUES (%s,%s)",[conf["id_evento"],id_empleado])
                        cursor.execute("DELETE FROM asis_no_iden WHERE id_asis_no_iden = %s",[conf["id_asis_no_iden"]])
                    conn.commit()
                return {"exito":True}
            return {"exito":False,"mensaje":"Empleado no encontrado"}    
    except:
        return {"exito":False,"mensaje":"Error inesperado al resolver los conflictos"}
    finally:
        if conn:
            conn.close()
            
