const encabezado = document.getElementById(`encabezado_busqueda`);
const cuerpo = document.getElementById(`resultados_busqueda`);
const conteo = document.getElementById('conteo');

function mostrar_tabla(datos, tipo) {
    conteo.innerHTML = `Total de resultados: ${datos.length}`;
    if (tipo == 1) {
        encabezado.innerHTML = `
            <tr>
                <th>Fecha</th>
                <th>Título</th>
                <th>Duración</th>
                <th>Conflictos</th>
                <th>Acciones</th>
            </tr>
        `;
        if (datos.length > 0) {
            cuerpo.innerHTML = `${datos.map(dato => `
                <tr>
                    <td>${dato.fecha_ev}</td>
                    <td>${dato.titulo_ev}</td>
                    <td>${dato.duracion_ev}</td>
                    <td>${dato.conflictos}</td>
                    <td><a class="btn btn-secondary text-white" href="/consultar_registros/detalles/evento/${dato.id_evento}">Ver asistentes</a></td>
                </tr>
                `).join('')}`
        }
        else {
            cuerpo.innerHTML = `<tr><td class="text-center" colspan="5">Sin resultados</td></tr>`;
        }
    }
    else if (tipo == 2) {
        encabezado.innerHTML = `
            <tr>
                <th>Cédula</th>
                <th>Nombre</th>
                <th>Acciones</th>
            </tr>
        `;
        if (datos.length > 0) {
            cuerpo.innerHTML = `${datos.map(dato => `
                <tr>
                    <td>${dato.cedula_em}</td>
                    <td>${dato.nombre_em}</td>
                    <td><a class="btn btn-secondary text-white" href="/consultar_registros/detalles/empleado/${dato.id_empleado}">Ver asistencias</a></td>
                </tr>
                `).join('')}`
        }
        else {
            cuerpo.innerHTML = `<tr><td class="text-center" colspan="3">Sin resultados</td></tr>`;
        }
    }
}

async function hacer_busqueda(busqueda, tipo) {
    try {
        const respuesta = await fetch(`/consultar_registros/busqueda_registros_por_tipo?busqueda=${encodeURIComponent(busqueda)}&tipo=${tipo}`);
        const resultados = await respuesta.json();
        if (resultados.exito){
            mostrar_tabla(resultados.datos,tipo);
        }
        else{
            alert(resultados.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error en la petición a la base de datos");
    }
}

document.getElementById('formulario_busqueda').addEventListener('submit', function (e) {
    e.preventDefault();
    const busqueda = document.getElementById('busqueda').value;
    const tipo = document.querySelector('input[name="tipo"]:checked').value;
    hacer_busqueda(busqueda, tipo);
})

hacer_busqueda('', 1);