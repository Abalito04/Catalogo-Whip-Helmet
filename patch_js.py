import sys

def patch_file(filepath, target, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if target in content:
        content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

t_js = """// Inicializar array de imágenes
function inicializarGaleria() {
    imagenesGaleria = [];
    
    // Obtener todas las imágenes de los thumbnails
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumb => {
        imagenesGaleria.push(thumb.src);
    });
}"""

r_js = """// Inicializar array de imágenes
function inicializarGaleria() {
    imagenesGaleria = [];
    
    // Obtener todas las imágenes de los thumbnails
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (thumbnails.length > 0) {
        thumbnails.forEach(thumb => {
            imagenesGaleria.push(thumb.src);
        });
    } else {
        // Si no hay thumbnails (producto con 1 sola foto), usamos la foto principal
        const imgMain = document.getElementById('imagen-main');
        if (imgMain) {
            imagenesGaleria.push(imgMain.src);
        }
    }
}"""

patch_file('static/js/producto.js', t_js, r_js)
