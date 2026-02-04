
function mostrarMensajesDjango() {
    const mensajes = document.querySelectorAll('.django-mensaje-data');
    
    mensajes.forEach(msg => {
        const tipo = msg.getAttribute('data-tipo'); 
        const texto = msg.getAttribute('data-text');
        
        // Mapeo de títulos según el tipo
        const titulos = {
            'success': '¡Éxito!',
            'error': 'Error',
            'warning': 'Atención',
            'info': 'Información'
        };

        if (typeof iziToast[tipo] === 'function') {
            iziToast[tipo]({
                title: titulos[tipo] || 'Notificación',
                message: texto,
                position: 'topRight',
                timeout: 5000,
                transitionIn: 'fadeInLeft'
            });
        }
    });
}

// Ejecutar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', mostrarMensajesDjango);