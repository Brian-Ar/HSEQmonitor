const cuerpo = document.getElementById('cuerpotabla');
const fecha_doc = document.getElementById('fecha_fis');
const titulo_doc = document.getElementById('titulo_fis');
const duracion_doc = document.getElementById('duracion_fis');

document.getElementById('crear_evento_form').addEventListener('submit', function (e) {
    e.preventDefault();
    const duracion_int = parseInt(duracion_doc.value);
    if (fecha_doc.value === '' || titulo_doc.value === '' || duracion_int === '') {
        alert('Rellene todos los campos');
        return;
    }
    if (isNaN(duracion_int)) {
        alert('La duración debe ser un número');
        return;
    }
    crear_evento(titulo_doc.value, fecha_doc.value, duracion_int);
    fecha_doc.value = ``;
    titulo_doc.value = ``;
    duracion_doc.value = ``;
})

async function crear_evento(titulo, fecha, duracion) {
    try {
        const respuesta = await fetch('/crear_registros/crear_formato_fisico', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                titulo: titulo,
                fecha: fecha,
                duracion: duracion
            })
        });
        const resultados = await respuesta.json();
        if (resultados.exito) {
            cargar_eventos_temp();
        }
        else {
            alert(resultados.mensaje);
        }
    }
    catch (error) {
        alert('Ha ocurrido un error en la petición al crear el evento');
    }
}

async function cargar_eventos_temp() {
    try {
        const respuesta = await fetch('/crear_registros/cargar_eventos_temp');
        const resultados = await respuesta.json();
        if (resultados.exito) {
            const datos = resultados.datos;
            if (datos.length > 0) {
                cuerpo.innerHTML = `${datos.map(dato => `
                    <tr>
                        <td>${dato.f_ev_temp}</td>
                        <td>${dato.t_ev_temp}</td>
                        <td>${dato.d_ev_temp}</td>
                        <td><a class="btn btn-secondary" href="/crear_registros/evento_temp/${dato.id_evento_temp}">Opciones</a></td>
                        <td><form id="${dato.id_evento_temp}" class="eliminacion"><input class="btn btn-danger" type="submit" value="Eliminar"></form></td>
                    </tr>
                    `).join('')}`;

                const eliminacion_forms = document.querySelectorAll(".eliminacion");
                eliminacion_forms.forEach(form => {
                    form.addEventListener('submit', function (e) {
                        e.preventDefault();
                        if (confirm('¿Deseas eliminar este evento? Esta acción no se puede deshacer')) {
                            eliminar_evento_temp(e.target.id);
                        }
                    });
                });
            }
            else {
                cuerpo.innerHTML = `<tr><td class="text-center" colspan="5">Sin resultados</td></tr>`;
            }
        }
        else {
            alert(resultados.mensaje);
        }
    }
    catch (error) {
        alert('Ha ocurrido un error en la petición al cargar los eventos');
    }
}

async function eliminar_evento_temp(id) {
    try {
        const respuesta = await fetch('/crear_registros/eliminar_evento_temp', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_evento: id
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito) {
            cargar_eventos_temp();
        }
        else {
            alert(resultado.mensaje);
        }

    }
    catch (error) {
        alert("Ha ocurrido un error en la petición al eliminar el evento");
    }
}

cargar_eventos_temp()