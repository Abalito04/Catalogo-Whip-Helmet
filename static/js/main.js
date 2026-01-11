// JavaScript para interacciones futuras
console.log('WHIP-HELMETS cargado');

// Header sticky con efecto scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Manejo de filtros móviles
document.addEventListener('DOMContentLoaded', function() {
    const btnAbrir = document.getElementById('btn-abrir-filtros');
    const btnCerrar = document.getElementById('btn-cerrar-filtros');
    const sidebar = document.getElementById('filtros-sidebar');
    
    // Crear overlay
    const overlay = document.createElement('div');
    overlay.className = 'filtros-overlay';
    document.body.appendChild(overlay);
    
    // Abrir filtros
    if (btnAbrir) {
        btnAbrir.addEventListener('click', function() {
            sidebar.classList.add('abierto');
            overlay.classList.add('activo');
            document.body.style.overflow = 'hidden';  // Bloquear scroll
        });
    }
    
    // Cerrar filtros
    function cerrarFiltros() {
        sidebar.classList.remove('abierto');
        overlay.classList.remove('activo');
        document.body.style.overflow = 'auto';  // Restaurar scroll
    }
    
    if (btnCerrar) {
        btnCerrar.addEventListener('click', cerrarFiltros);
    }
    
    // Cerrar al hacer click en overlay
    overlay.addEventListener('click', cerrarFiltros);
});

