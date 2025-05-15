const cuerpo = document.getElementById('cuerpo_tabla_asistentes');
const total_resultados = document.getElementById('total_resultados');

function hacer_tabla(datos){
    total_resultados.innerHTML = `Resultados: ${datos.length}`;
    if (datos.length > 0){
        cuerpo.innerHTML = `${datos.map(dato=>`
            <tr>
                <td>${dato.cedula_em}</td>
                <td>${dato.nombre_em}</td>
                <td><a class="btn btn-secondary" href="/consultar_registros/detalles/empleado/${dato.id_empleado}">Ver empleado</a></td>
            </tr>
            `).join('')}`;
    }
    else{
        cuerpo.innerHTML = `<tr><td colspan="3">Sin resultados</td></tr>`;
    }
}

async function hacer_busqueda(busqueda) {
    try{
        const respuesta = await fetch(`/consultar_registros/busqueda_de_asistencias?segun=empleado&id=${id_evento}&busqueda=${busqueda}`);
        const resultados = await respuesta.json();
        if (resultados.exito){
            hacer_tabla(resultados.datos);
        }
        else{
            alert(resultados.mensaje);
        }
    }
    catch(error){
        alert("Ha ocurrido un error en la petición a la base de datos");
    }
}

document.getElementById('buscar_asistentes').addEventListener('submit',function(e){
    e.preventDefault();
    const busqueda = document.getElementById('busqueda').value;
    hacer_busqueda(busqueda);
});

hacer_busqueda('');