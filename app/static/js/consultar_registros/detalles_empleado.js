const cuerpo = document.getElementById('cuerpo_tabla_asistencias');
const horas = document.getElementById('espacio_horas');
const total_resultados = document.getElementById('total_resultados');

function hacer_tabla(datos,total_horas){
    total_resultados.innerHTML = `Total de resultados: ${datos.length}`;
    horas.innerHTML = `Total de horas: ${total_horas}`;
    if (datos.length > 0){
        cuerpo.innerHTML = `${datos.map(dato=>`
            <tr>
                <td>${dato.fecha_ev}</td>
                <td>${dato.titulo_ev}</td>
                <td>${dato.duracion_ev}</td>
                <td><a class="btn btn-secondary" href="/consultar_registros/detalles/evento/${dato.id_evento}">Ver evento</a></td>
            </tr>
            `).join('')}`;
    }
    else{
        cuerpo.innerHTML = `<tr><td class="text-center" colspan="4">Sin resultados</td></tr>`;
    }
}

async function hacer_busqueda(inf,sup) {
    try{
        const respuesta = await fetch(`/consultar_registros/busqueda_de_asistencias?segun=evento&id=${id_em}&inf=${inf}&sup=${sup}`);
        const resultados = await respuesta.json();
        if (resultados.exito){
            hacer_tabla(resultados.datos,resultados.total_horas);
        }
        else{
            alert(resultados.mensaje);
        }
    }
    catch(error){
        alert("Ha ocurrido un error en la petición a la base de datos");
    }
}

document.getElementById('filtro_fechas').addEventListener('submit',function(e){
    e.preventDefault();
    const inf = document.getElementById('inf').value;
    const sup = document.getElementById('sup').value;
    hacer_busqueda(inf,sup);
});

hacer_busqueda('','');