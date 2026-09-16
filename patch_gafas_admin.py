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

t_add = """<option value="casco">Casco</option>
                <option value="indumentaria">Indumentaria</option>
            </select>"""

r_add = """<option value="casco">Casco</option>
                <option value="indumentaria">Indumentaria</option>
                <option value="gafas">Gafas</option>
            </select>"""

patch_file('templates/agregar_casco.html', t_add, r_add)

t_edit = """<option value="casco" {% if casco.categoria == 'casco' %}selected{% endif %}>Casco</option>
                <option value="indumentaria" {% if casco.categoria == 'indumentaria' %}selected{% endif %}>Indumentaria</option>
            </select>"""

r_edit = """<option value="casco" {% if casco.categoria == 'casco' %}selected{% endif %}>Casco</option>
                <option value="indumentaria" {% if casco.categoria == 'indumentaria' %}selected{% endif %}>Indumentaria</option>
                <option value="gafas" {% if casco.categoria == 'gafas' %}selected{% endif %}>Gafas</option>
            </select>"""

patch_file('templates/editar_casco.html', t_edit, r_edit)
