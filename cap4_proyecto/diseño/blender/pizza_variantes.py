"""Fotos de producto de las 5 pizzas de la carta, con el mismo estilo que el vídeo.
Parte de pizza_napolitana.blend y cambia ingredientes por variante.
Uso: blender -b pizza_napolitana.blend --python pizza_variantes.py
Salida: ../fotos/pizza_<nombre>.png (800 x 800)
"""
import bpy, math, random, os, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(bpy.data.filepath)), "fotos")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene
root = bpy.data.objects["Pizza"]
sauce = bpy.data.objects["Salsa"]
cheeses = [o for o in root.children if o.name.startswith("Mozzarella")]
basils = [o for o in root.children if o.name.startswith("Albahaca")]
SAUCE_MAT = sauce.data.materials[0]


def mat(name, color, rough=0.5, coat=0.0, sss=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    b = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:  # Blender 5 puede crear el material sin nodos por defecto
        nodes.clear()
        b = nodes.new("ShaderNodeBsdfPrincipled")
        out = nodes.new("ShaderNodeOutputMaterial")
        m.node_tree.links.new(b.outputs[0], out.inputs[0])
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Subsurface Weight"].default_value = sss
    return m


M_PEPP = mat("Pepperoni", (0.22, 0.02, 0.01), 0.3, 0.4)
M_SALAMI = mat("Salami picante", (0.16, 0.015, 0.012), 0.45, 0.2)
M_CHILI = mat("Guindilla", (0.6, 0.02, 0.01), 0.25, 0.3)
M_BBQ = mat("Salsa barbacoa", (0.12, 0.035, 0.01), 0.3, 0.5)
M_CHICKEN = mat("Pollo", (0.50, 0.28, 0.10), 0.6)
M_ONION = mat("Cebolla morada", (0.35, 0.05, 0.22), 0.3, 0.2, 0.2)
M_CREAM = mat("Base blanca", (0.90, 0.84, 0.68), 0.45, 0.0, 0.2)
M_FONTINA = mat("Fontina", (0.95, 0.72, 0.30), 0.4, 0.0, 0.3)
M_GORGO = mat("Gorgonzola", (0.82, 0.84, 0.74), 0.5, 0.0, 0.2)
M_BACON = mat("Bacon", (0.30, 0.07, 0.04), 0.35, 0.4)
M_JAMON = mat("Jamón cocido", (0.85, 0.42, 0.40), 0.4, 0.1, 0.25)

added = []


def scatter(n, rmax, sep, seed):
    random.seed(seed)
    pts = []
    for _ in range(3000):
        if len(pts) == n:
            break
        r = math.sqrt(random.uniform(0, rmax ** 2)); a = random.uniform(0, math.tau)
        p = (r * math.cos(a), r * math.sin(a))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > sep ** 2 for q in pts):
            pts.append(p)
    return pts


def add(o, m):
    o.parent = root
    o.data.materials.clear(); o.data.materials.append(m)
    for p in o.data.polygons:
        p.use_smooth = True
    added.append(o)
    return o


def discs(n, r, m, seed, z=0.075, cup=True):
    for x, y in scatter(n, 0.7, r * 2.1, seed):
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=r * random.uniform(0.9, 1.1), depth=0.018, location=(x, y, z))
        o = add(bpy.context.object, m)
        o.rotation_euler = (random.uniform(-.12, .12), random.uniform(-.12, .12), 0)
        b = o.modifiers.new("Bisel", 'BEVEL'); b.width = 0.006; b.segments = 3
        if cup:  # bordes un poco levantados, como el pepperoni al horno
            sd = o.modifiers.new("Copa", 'SIMPLE_DEFORM'); sd.deform_method = 'BEND'; sd.angle = 0.25


def rings(n, r, m, seed, minor=0.008):
    for x, y in scatter(n, 0.7, r * 1.6, seed):
        bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=minor, location=(x, y, 0.07))
        o = add(bpy.context.object, m)
        o.scale = (1, random.uniform(0.7, 1), 0.35)
        o.rotation_euler.z = random.uniform(0, math.tau)


def chunks(n, size, m, seed):
    for x, y in scatter(n, 0.68, size * 2.2, seed):
        bpy.ops.mesh.primitive_cube_add(size=size, location=(x, y, 0.07))
        o = add(bpy.context.object, m)
        o.scale = (random.uniform(0.8, 1.4), random.uniform(0.7, 1.1), 0.5)
        o.rotation_euler = (0, 0, random.uniform(0, math.tau))
        b = o.modifiers.new("Bisel", 'BEVEL'); b.width = size * 0.25; b.segments = 3


def blobs(n, r, m, seed):
    for x, y in scatter(n, 0.62, r * 1.7, seed):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=r, location=(x, y, 0.02))
        o = add(bpy.context.object, m)
        o.scale = (random.uniform(0.9, 1.3), random.uniform(0.8, 1.1), 0.28)
        o.modifiers.new("Suave", 'SUBSURF').levels = 1


def strips(n, m, seed):
    """Tiras de bacon onduladas."""
    for x, y in scatter(n, 0.66, 0.2, seed):
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x, y, 0.075))
        o = add(bpy.context.object, m)
        o.scale = (2.3, 0.55, 0.14)
        o.rotation_euler = (0, 0, random.uniform(0, math.tau))
        o.modifiers.new("Sub", 'SUBSURF').levels = 2
        w = o.modifiers.new("Onda", 'WAVE'); w.use_y = False; w.height = 0.012; w.width = 0.06; w.narrowness = 1.2


def folds(n, r, m, seed):
    """Lonchas de jamón: piezas finas, irregulares y algo onduladas."""
    for x, y in scatter(n, 0.6, r * 1.4, seed):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=r, location=(x, y, 0.06))
        o = add(bpy.context.object, m)
        o.scale = (random.uniform(1.1, 1.4), random.uniform(0.8, 1.0), 0.09)
        o.rotation_euler = (random.uniform(-.15, .15), random.uniform(-.15, .15), random.uniform(0, math.tau))
        d = o.modifiers.new("Arrugas", 'DISPLACE'); d.strength = 0.25
        d.texture = bpy.data.textures.get("Arrugas") or bpy.data.textures.new("Arrugas", 'CLOUDS')
        d.texture.noise_scale = 0.15
        o.modifiers.new("Suave", 'SUBSURF').levels = 1


def reset():
    for o in added:
        bpy.data.objects.remove(o, do_unlink=True)
    added.clear()
    sauce.data.materials[0] = SAUCE_MAT
    for o in cheeses + basils:
        o.hide_render = False


VARIANTS = {
    "margherita": lambda: None,
    "pepperoni": lambda: ([setattr(o, "hide_render", True) for o in basils], discs(13, 0.1, M_PEPP, 3)),
    "cuatro_quesos": lambda: (
        [setattr(o, "hide_render", True) for o in basils],
        sauce.data.materials.__setitem__(0, M_CREAM),
        blobs(5, 0.12, M_FONTINA, 5), blobs(4, 0.1, M_GORGO, 9)),
    "barbacoa": lambda: (
        [setattr(o, "hide_render", True) for o in basils],
        sauce.data.materials.__setitem__(0, M_BBQ),
        chunks(16, 0.11, M_CHICKEN, 7), rings(9, 0.08, M_ONION, 8, minor=0.014)),
    "bacon": lambda: ([setattr(o, "hide_render", True) for o in basils], chunks(26, 0.085, M_BACON, 12)),
    "jamon": lambda: ([setattr(o, "hide_render", True) for o in basils], folds(6, 0.17, M_JAMON, 13)),
    "diavola": lambda: (
        [setattr(o, "hide_render", True) for o in basils[2:]],
        discs(10, 0.12, M_SALAMI, 4, cup=False), rings(14, 0.028, M_CHILI, 6, minor=0.009)),
}

# Cámara cenital ligeramente inclinada, encuadre cuadrado
cam = scene.camera
cam.location = (0, -1.5, 3.45)
cam.data.lens = 50
cam.data.dof.use_dof = False
r = scene.render
r.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 48
r.resolution_x = r.resolution_y = 800
r.image_settings.file_format = 'PNG'
scene.frame_set(1)

# Tras "--" se pueden pasar nombres para renderizar solo esas variantes
only = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
for name, build in VARIANTS.items():
    if only and name not in only:
        continue
    build()
    r.filepath = os.path.join(OUT, f"pizza_{name}.png")
    bpy.ops.render.render(write_still=True)
    reset()
print("OK variantes")
