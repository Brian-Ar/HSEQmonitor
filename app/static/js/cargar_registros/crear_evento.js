const sect1 = document.getElementById('sec-form-fis');
const sect2 = document.getElementById('sec-form-vir');

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