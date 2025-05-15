const cuerpo_empl = document.getElementById('cuerpo_tabla_empleados');
const cedula_crear = document.getElementById('cedula_crear');
const nombre_crear = document.getElementById('nombre_crear');
const id_emp_edi = document.getElementById('id_emp_edi');
const cedula_edi = document.getElementById('cedula_edi');
const nombre_edi = document.getElementById('nombre_edi');
const submit_edi = document.getElementById('submit_edi');


document.getElementById('empl_manual').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (cedula_crear.value == '' || nombre_crear.value == '') {
        alert('Ningún campo puede estar vacío');
        return;
    }
    if (confirm('¿Deseas añadir a este empleado?')) {
        try {
            const respuesta = await fetch('/gestion/empleado_manual', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    cedula: cedula_crear.value,
                    nombre: nombre_crear.value
                })
            });
            const resultado = await respuesta.json();
            if (resultado.exito) {
                cedula_crear.value = '';
                nombre_crear.value = '';
                cargar_tabla();
            }
            else {
                alert(resultado.mensaje);
            }
        }
        catch (error) {
            alert('Ha ocurrido un error con la petición de crear el empleado')
        }
    }
});

document.getElementById('act_empl_form').addEventListener('submit', async (e) => {
    e.preventDefault()
    if (confirm("¿Deseas cargar el archivo de empleados?")) {
        const archivo = document.getElementById('archivo');
        const datos_formulario = new FormData();
        if (archivo.files.length > 0) {
            datos_formulario.append('archivo', archivo.files[0]);
            try {
                const respuesta = await fetch('/gestion/cargar_archivo_empl', {
                    method: 'POST',
                    body: datos_formulario
                });
                const resultado = await respuesta.json()
                if (resultado.exito) {
                    cargar_tabla();
                }
                else {
                    alert(resultado.mensaje);
                }
            }
            catch (error) {
                alert("Error en la petición de cargar el archivo");
            }
        }
        else {
            alert("Seleccione un archivo");
        }
    }
});

document.getElementById('edicion_empleado').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (cedula_edi.value == '' || nombre_edi.value == '' || id_emp_edi.value == '') {
        alert('Ningún campo puede estar vacío');
        return;
    }
    if (confirm('¿Deseas editar la información de este empleado?')) {
        try {
            const respuesta = await fetch('/gestion/edicion_empl', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id_emp: id_emp_edi.value,
                    cedula: cedula_edi.value,
                    nombre: nombre_edi.value
                })
            });
            const resultado = await respuesta.json();
            if (resultado.exito) {
                cedula_edi.value = '';
                nombre_edi.value = '';
                id_emp_edi.value = '';
                cedula_edi.disabled = true;
                nombre_edi.disabled = true;
                submit_edi.disabled = true;
                cargar_tabla();
            }
            else {
                alert(resultado.mensaje);
            }
        }
        catch (error) {
            alert('Ha ocurrido un error con la petición de crear el empleado')
        }
    }
})

function preparar_emp(datos) {
    const datos_obj = JSON.parse(datos);
    cedula_edi.value = datos_obj.cedula_em;
    nombre_edi.value = datos_obj.nombre_em;
    id_emp_edi.value = datos_obj.id_empleado;
    cedula_edi.disabled = false;
    nombre_edi.disabled = false;
    submit_edi.disabled = false;
}

async function eliminar_emp(id_emp) {
    try {
        const respuesta = await fetch('/gestion/eliminar_empl',{
            method: 'POST',
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                id_emp:id_emp
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito){
            cargar_tabla();
        }
        else{
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error con la petición de eliminación");
    }
}

async function cargar_tabla() {
    try {
        const respuesta = await fetch('/gestion/cargar_empleados');
        const resultados = await respuesta.json();
        if (resultados.exito) {
            const datos = resultados.datos;
            document.getElementById('total_emp').innerHTML = `Total de empleados: ${datos.length}`;
            if (datos.length > 0) {
                cuerpo_empl.innerHTML = `${datos.map(dato => {
                    let cadena1 =`<tr><td>${dato.cedula_em}</td><td>${dato.nombre_em}</td>`;
                    let cadena2 = ``;
                    if (dato.es_usuario){
                        cadena2 = `<td colspan="2">Este empleado solo puede ser editado desde las opciones de administrador</td></tr>`;
                    }
                    else{
                        cadena2 =`<td><button data-datos='${JSON.stringify(dato)}' class="edicion">Editar</button></td>
                        <td><button id="${dato.id_empleado}" class="eliminacion">Eliminar</button></td></tr>`;
                    }
                    let result = cadena1+cadena2;
                    return result;
                }
                ).join('')}`;
                const edicion_btn = document.querySelectorAll('.edicion');
                edicion_btn.forEach(btn => {
                    btn.addEventListener('click', (e) => preparar_emp(e.target.dataset.datos));
                });
                const eliminar_btn = document.querySelectorAll(".eliminacion");
                eliminar_btn.forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        if (confirm("¿Deseas eliminar a este empleado?\nToda la información relacionada a este empleado sera eliminada\nEsta acción es irreversible")) {
                            eliminar_emp(e.target.id);
                        }
                    })
                });
            }
            else {
                cuerpo_empl.innerHTML = `<tr><td colspan="4">Sin resultados</td></tr>`;
            }
        }
        else {
            alert(resultados.mensaje);
        }
    }
    catch (errror) {
        alert("Ha ocurrido un error al hacer la petición de cargar los empleados");
    }

}

cargar_tabla();