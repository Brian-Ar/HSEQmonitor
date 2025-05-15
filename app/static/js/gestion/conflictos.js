const tabla_busqueda = document.getElementById('cuerpotabla_busqueda');

document.getElementById('busqueda').addEventListener('input', async function (e) {
    try {
        const respuesta = await fetch(`/cargar_registros/evento_temp/buscar_empleado?busqueda=${encodeURIComponent(e.target.value)}`);
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