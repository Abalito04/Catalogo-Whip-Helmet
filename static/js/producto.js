// Variables globales
let imagenesGaleria = [];
let imagenActualIndex = 0;

// Inicializar array de imágenes
function inicializarGaleria() {
    imagenesGaleria = [];
    
    // Obtener todas las imágenes de los thumbnails
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        imagenesGaleria.push(thumb.src);
    });
}

function cambiarImagen(src) {
    document.getElementById('imagen-main').src = src;
    
    // Actualizar thumbnail activo
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        if (thumb.src === src) {
            thumb.classList.add('active');
        } else {
            thumb.classList.remove('active');
        }
    });
}

function abrirLightbox() {
    inicializarGaleria();
    const img = document.getElementById('imagen-main');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    
    // Encontrar índice de la imagen actual
    imagenActualIndex = imagenesGaleria.findIndex(imgSrc => imgSrc === img.src);
    if (imagenActualIndex === -1) imagenActualIndex = 0;
    
    lightboxImg.src = imagenesGaleria[imagenActualIndex];
    actualizarContador();
    lightbox.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function cerrarLightbox(event) {
    if (event) event.stopPropagation();
    const lightbox = document.getElementById('lightbox');
    lightbox.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function cambiarImagenLightbox(direccion) {
    imagenActualIndex += direccion;
    
    // Ciclar: si llega al final, volver al principio y viceversa
    if (imagenActualIndex >= imagenesGaleria.length) {
        imagenActualIndex = 0;
    } else if (imagenActualIndex < 0) {
        imagenActualIndex = imagenesGaleria.length - 1;
    }
    
    const lightboxImg = document.getElementById('lightbox-img');
    lightboxImg.src = imagenesGaleria[imagenActualIndex];
    actualizarContador();
}

function actualizarContador() {
    const contador = document.getElementById('lightbox-counter');
    if (contador) {
        contador.textContent = `${imagenActualIndex + 1} / ${imagenesGaleria.length}`;
    }
}

// Navegación con teclado
document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('lightbox');
    if (lightbox && lightbox.style.display === 'flex') {
        if (e.key === 'Escape') {
            cerrarLightbox();
        } else if (e.key === 'ArrowLeft') {
            cambiarImagenLightbox(-1);
        } else if (e.key === 'ArrowRight') {
            cambiarImagenLightbox(1);
        }
    }
});

// Prevenir que el click en la imagen cierre el lightbox
document.addEventListener('DOMContentLoaded', function() {
    const lightboxImg = document.getElementById('lightbox-img');
    if (lightboxImg) {
        lightboxImg.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
});
