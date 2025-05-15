const messages = document.querySelectorAll('.mensaje_flash_container');
setTimeout(() => {
    messages.forEach(msg => {
        msg.classList.add('fade-out');
        setTimeout(() => msg.remove(), 250);
    });
}, 3000);