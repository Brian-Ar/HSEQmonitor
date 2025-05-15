const agregados = document.getElementById('cuerpotabla_agregados');
const tabla_busqueda = document.getElementById('cuerpotabla_busqueda');
const fecha = document.getElementById('fecha');
let fecha_original = fecha.value;
const titulo = document.getElementById('titulo');
let titulo_original = titulo.value;
const duracion = document.getElementById('duracion');
let duracion_original = duracion.value;
const submit = document.getElementById("submit")

document.getElementById('btn_edicion').addEventListener('click', (e) => {
    titulo.disabled = !titulo.disabled;
    fecha.disabled = !fecha.disabled;
    duracion.disabled = !duracion.disabled;
    submit.disabled = !submit.disabled;

    if (submit.disabled) {
        e.target.innerHTML = `Editar`;
        fecha.value = fecha_original;
        titulo.value = titulo_original;
        duracion.value = duracion_original;
    }
    else {
        e.target.innerHTML = `Cancelar`;
    }
})

document.getElementById('edicion_form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const nueva_fecha = fecha.value;
    const nuevo_titulo = titulo.value;
    const nueva_duracion = parseInt(duracion.value);
    if (nueva_fecha == '' || nuevo_titulo == '' || nueva_duracion == '') {
        alert('Los campos no pueden estar vacios');
        return;
    }
    if (isNaN(nueva_duracion)) {
        alert('La duracion debe ser un número');
        return;
    }
    try {
        const respuesta = await fetch('/crear_registros/evento_temp/editar_evento_temp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_evento: id_ev_temp,
                fecha: nueva_fecha,
                titulo: nuevo_titulo,
                duracion: nueva_duracion
            })
        })
        const resultados = await respuesta.json()
        if (resultados.exito){
            fecha_original = nueva_fecha;
            titulo_original = nuevo_titulo;
            duracion_original = nueva_duracion;
            document.getElementById('btn_edicion').click();
        }
        else{
            alert(resultados.mensaje);
        }

    }
    catch (error) {
        alert('Ha ocurrido un error con la petición de edición');
    }
})

async function hacer_tabla() {
    try {
        const respuesta = await fetch(`/crear_registros/evento_temp/cargar_tabla_asis_temp?id_ev_temp=${id_ev_temp}`);
        const resultado = await respuesta.json();
        if (resultado.exito) {
            const datos = resultado.datos;
            if (datos.length > 0) {
                agregados.innerHTML = `${datos.map(dato => `
                    <tr>
                        <td>${dato.cedula_em}</td>
                        <td>${dato.nombre_em}</td>
                        <td><form id="${dato.id_empleado}" class="eliminacion"><input type="submit" value="-"></form></td>
                    </tr>
                    `).join('')}`;
                const elim_form = document.querySelectorAll('.eliminacion');
                elim_form.forEach(form => {
                    form.addEventListener('submit', function (e) {
                        e.preventDefault();
                        eliminar_asis_temp(e.target.id);
                    });
                })
            }
            else {
                agregados.innerHTML = `<tr><td colspan="3">Sin resultados</td></tr>`;
            }
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert('Ha ocurrido un error en la petición al cargar los asistentes');
    }
}

async function eliminar_asis_temp(id_emp) {
    try {
        const respuesta = await fetch('/crear_registros/evento_temp/eliminar_asis_temp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_evento: id_ev_temp,
                id_emp: id_emp
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito) {
            hacer_tabla();
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error en la petición de eliminar asistente temporal");
    }
}

document.getElementById('busqueda').addEventListener('input', async function (e) {
    try {
        const respuesta = await fetch(`/crear_registros/evento_temp/buscar_empleado?busqueda=${encodeURIComponent(e.target.value)}`);
        const resultado = await respuesta.json();
        if (resultado.exito) {
            const datos = resultado.datos;
            if (datos.length > 0) {
                tabla_busqueda.innerHTML = `${datos.map(dato => `
                    <tr>
                        <td>${dato.cedula_em}</td>
                        <td>${dato.nombre_em}</td>
                        <td><form id="${dato.id_empleado}" class="agregacion"><input type="submit" value="+"></form></td>
                    </tr>
                    `).join('')}`;
                const agr_form = document.querySelectorAll('.agregacion');
                agr_form.forEach(form => {
                    form.addEventListener('submit', function (e) {
                        e.preventDefault();
                        agregar_asis_temp(e.target.id);
                    });
                });
            }
            else {
                tabla_busqueda.innerHTML = `<tr><td colspan="3">Sin coincidencias</td></tr>`;
            }
        }
        else {
            tabla_busqueda.innerHTML = `<tr><td colspan="3">${resultado.mensaje}</td></tr>`;
        }

    }
    catch (error) {
        tabla_busqueda.innerHTML = `<tr><td colspan="3">Ha ocurrido un error al hacer la petición de busqueda del empleado</td></tr>`;
    }
})

async function agregar_asis_temp(id_emp) {
    try {
        const respuesta = await fetch('/crear_registros/evento_temp/agregar_asis_temp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_evento: id_ev_temp,
                id_emp: id_emp
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito) {
            hacer_tabla();
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error en la petición de agregar asistente temporal");
    }
}

document.getElementById('terminar_form').addEventListener('submit',(e)=>{
    if (!confirm('¿Deseas dar por finalizado este evento?')){
        e.preventDefault();
    }
})

hacer_tabla()