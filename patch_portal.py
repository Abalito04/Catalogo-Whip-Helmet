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

t_css = """/* ==========================================
   MAIN CONTENT
   ========================================== */


main {"""

r_css = """/* ==========================================
   PORTAL / CATEGORIAS INICIALES
   ========================================== */

.categorias-iniciales {
    padding: 20px 0 60px;
    text-align: center;
}

.categorias-titulo {
    color: #ffd700;
    font-size: 36px;
    margin-bottom: 40px;
    font-weight: 700;
}

.categorias-grid {
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
}

.categoria-card {
    background: #2a2a2a;
    border-radius: 12px;
    overflow: hidden;
    text-decoration: none;
    width: 100%;
    max-width: 450px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.5);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 2px solid transparent;
}

.categoria-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 25px rgba(255, 215, 0, 0.2);
    border-color: #ffd700;
}

.categoria-img-container {
    width: 100%;
    height: 300px;
    overflow: hidden;
    background: #1a1a1a;
}

.categoria-img-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.categoria-card:hover .categoria-img-container img {
    transform: scale(1.05);
}

.categoria-card h3 {
    color: #fff;
    font-size: 28px;
    padding: 20px;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: linear-gradient(to top, #111, #2a2a2a);
}

.categoria-card:hover h3 {
    color: #ffd700;
}

/* ==========================================
   MAIN CONTENT
   ========================================== */


main {"""

patch_file('static/css/style.css', t_css, r_css)
