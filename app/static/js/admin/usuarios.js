const cuerpo_usuarios = document.getElementById('cuerpo_tabla_usuarios');
const cuerpo_busqueda = document.getElementById('lista-busqueda');

const id_persona = document.getElementById('id_persona');
const cedula = document.getElementById('cedula');
const nombre = document.getElementById('nombre');
const correo = document.getElementById('correo');
const tipo = document.getElementById('tipo');
const submit = document.getElementById('submit');
const sect1 = document.getElementById('sec-ver-us');
const sect2 = document.getElementById('sec-crear-us');

const modal = document.querySelector('[data-modal]');
const closeModal = document.querySelector('[data-close-modal]');

const titulo_edi_form = document.getElementById('titulo-form-editar');

modal.addEventListener('click', (e) => {
  if (e.target === modal) {
    cerrar_y_limpiar();
  }
});

function cerrar_y_limpiar() {
    modal.close();
    modal.style.display = 'none';
    id_persona.value = '';
    cedula.value = '';
    nombre.value = '';
    correo.value = '';
    tipo.value = '';
    cedula.disabled = true;
    nombre.disabled = true;
    correo.disabled = true;
    tipo.disabled = true;
    submit.disabled = true;
}

closeModal.addEventListener('click', () => cerrar_y_limpiar());

document.getElementById('busqueda').addEventListener('input', async (e) => {
    try {
        const respuesta = await fetch(`/administracion/buscar_empleado?busqueda=${encodeURIComponent(e.target.value)}`)
        const resultado = await respuesta.json()
        if (resultado.exito) {
            const datos = resultado.datos;
            if (datos.length > 0) {
                cuerpo_busqueda.innerHTML = `${datos.map(dato => `
                    <li class="list-group-item">
                        <span class="mb-1">${dato.cedula_em} - ${dato.nombre_em}</span>
                        <button class="btn btn-success text-white agregacion" data-datos='${JSON.stringify({ id_usuario: dato.id_empleado, cedula_em: dato.cedula_em, nombre_em: dato.nombre_em, correo_us: "", tipo_us: "Regular" })}'>Crear</button>
                    </li>
                    `).join('')}`;
                const btn_agr = document.querySelectorAll('.agregacion');
                btn_agr.forEach(btn => {
                    btn.addEventListener("click", (e) => {
                        const datos_user = JSON.parse(e.target.dataset.datos);
                        preparar_usuario(datos_user,"creacion");
                        titulo_edi_form.innerHTML = 'Creando un usuario';
                        modal.style.display = 'flex';
                        modal.showModal();
                    })
                });
            }
            else {
                cuerpo_busqueda.innerHTML = `<li class="list-group-item">Sin coincidencias</li>`;
            }
        }
        else {
            cuerpo_busqueda.innerHTML = `<li class="list-group-item">${resultado.mensaje}</li>`
        }
    }
    catch (error) {
        cuerpo_busqueda.innerHTML = `<li class="list-group-item">Error con la petición de busqueda</li>`;
    }
});

document.getElementById('crear_o_editar_form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!confirm('¿Deseas agregar o actualizar este usuario?')) {
        return;
    }
    const valor_id_persona = id_persona.value;
    const valor_cedula = cedula.value;
    const valor_nombre = nombre.value;
    const valor_tipo = tipo.value;
    if (valor_id_persona == '' || valor_cedula == '' || valor_nombre == '' || valor_tipo == '') {
        alert('Ningún campo con * puede estar vacío');
        return;
    }
    try {
        const respuesta = await fetch('/administracion/confirmar_form_usuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id_persona: valor_id_persona,
                cedula: valor_cedula,
                nombre: valor_nombre,
                correo: correo.value,
                tipo: valor_tipo
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito) {
            document.getElementById('busqueda').value = '';
            cuerpo_busqueda.innerHTML = `<tr><td colspan="3">Sin coincidencias</td></tr>`;
            cerrar_y_limpiar();
            cargar_tabla();
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error al hacer la petición de crear o editar usuario");
    }
});

async function cargar_tabla() {
    try {
        const respuesta = await fetch('/administracion/cargar_usuarios');
        const resultado = await respuesta.json();
        if (resultado.exito) {
            const datos = resultado.datos;
            if (datos.length > 0) {
                cuerpo_usuarios.innerHTML = `${datos.map(dato => `
                    <tr>
                        <td>${dato.cedula_em}</td>
                        <td>${dato.nombre_em}</td>
                        <td>${dato.correo_us}</td>
                        <td>${dato.tipo_us}</td>
                        <td><button class="btn btn-warning edicion" data-datos='${JSON.stringify(dato)}'>Editar</button></td>
                        <td><button class="btn btn-danger eliminacion" id="${dato.id_usuario}">Eliminar</button></td>
                    </tr>
                    `).join('')}`;
                const btn_edicion = document.querySelectorAll(".edicion");
                btn_edicion.forEach(btn => {
                    btn.addEventListener("click", (e) => {
                        const datos_user = JSON.parse(e.target.dataset.datos);
                        preparar_usuario(datos_user,"edicion");
                        titulo_edi_form.innerHTML = 'Editando un usuario';
                        modal.style.display = 'flex';
                        modal.showModal();
                    });
                });
                const btn_eliminacion = document.querySelectorAll(".eliminacion");
                btn_eliminacion.forEach(btn => {
                    btn.addEventListener("click", (e) => {
                        if (confirm("¿Deseas eliminar a este usuario?")) {
                            eliminar_usuario(e.target.id);
                        }
                    })
                });
            }
            else {
                cuerpo_usuarios.innerHTML = `<tr><td class="text-center" colspan="5">Sin resultados</td></tr>`;
            }
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert('Ha ocurrido un error con la petición de cargar la tabla');
    }
}

function preparar_usuario(datos, modo) {
    if (modo === 'edicion') {
        id_persona.value = datos.id_usuario;
        cedula.value = datos.cedula_em;
        nombre.value = datos.nombre_em;
        correo.value = datos.correo_us;
        tipo.value = datos.tipo_us;
        cedula.disabled = false;
        nombre.disabled = false;
        correo.disabled = false;
        tipo.disabled = false;
        submit.disabled = false;
    }
    else if (modo === 'creacion') {
        id_persona.value = datos.id_usuario;
        cedula.value = datos.cedula_em;
        nombre.value = datos.nombre_em;
        correo.value = datos.correo_us;
        tipo.value = datos.tipo_us;
        correo.disabled = false;
        tipo.disabled = false;
        submit.disabled = false;
    }
}

async function eliminar_usuario(id_us) {
    try {
        const respuesta = await fetch('/administracion/eliminar_usuario', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_us: id_us
            })
        });
        const resultado = await respuesta.json();
        if (resultado.exito) {
            cargar_tabla();
        }
        else {
            alert(resultado.mensaje);
        }
    }
    catch (error) {
        alert("Ha ocurrido un error en la petición de eliminación");
    }
}

function es_movil() {
    return window.innerWidth <= 768;
}

function expandir_seccion(expande, contrae) {
    if (es_movil()) {
        expande.style.height = '90%';
        contrae.style.height = '10%';

        expande.style.width = '100%';
        contrae.style.width = '100%';
    }
    else {
        expande.style.width = '90%';
        contrae.style.width = '10%';

        expande.style.height = '100%';
        contrae.style.height = '100%';
    }

    expande.classList.add('expandido');
    expande.classList.remove('contraido');

    contrae.classList.add('contraido');
    contrae.classList.remove('expandido');
}

expandir_seccion(sect1, sect2);

sect1.addEventListener('click', () => expandir_seccion(sect1, sect2));
sect2.addEventListener('click', () => expandir_seccion(sect2, sect1));

window.addEventListener('resize', () => {
    if (sect1.classList.contains('expandido')) {
        expandir_seccion(sect1, sect2);
    }
    else {
        expandir_seccion(sect2, sect1);
    }
})

cargar_tabla()