const previsualizar = document.getElementById('previsualizar');
const fecha = document.getElementById('fecha_vir');
const titulo = document.getElementById('titulo_vir');
const duracion = document.getElementById('duracion_vir');
const submit = document.getElementById('submit_vir');

document.getElementById('encabezado_form').addEventListener('submit',(e)=>{
    if (fecha.value == '' || titulo.value == '' || duracion.value == ''){
        alert("Todos los campos deben estar llenos");
        return;
    }
    if (isNaN(parseInt(duracion.value))){
        alert("La duración debe ser un número");
        return;
    }
    if(!confirm('¿Deseas terminar?')){
        e.preventDefault();
    }
})

document.getElementById('archivo_form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const archivo = document.getElementById('archivo');
    const datos_formulario = new FormData();
    if (archivo.files.length > 0) {
        datos_formulario.append('archivo', archivo.files[0]);
        try {
            const respuesta = await fetch('/crear_registros/cargar_excel', {
                method: 'POST',
                body: datos_formulario
            });
            const resultado = await respuesta.json()
            if (resultado.exito) {
                const datos = JSON.parse(resultado.datos);
                document.getElementById('total_encontrados').innerHTML = `${datos.length}`;
                previsualizar.innerHTML = `${datos.map(dato => `
                    <tr>
                        <td>${dato.cedula}</td>
                        <td>${dato.nombre}</td>
                    </tr>
                    `).join('')}`;
                fecha.disabled = false;
                titulo.disabled = false;
                duracion.disabled = false;
                submit.disabled = false;
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
})