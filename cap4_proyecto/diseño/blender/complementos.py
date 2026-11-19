"""Fotos de producto de los 8 complementos, sobre una tabla de pizarra. Mismo fondo y luz que las bebidas.
Uso: blender -b --python complementos.py [-- nombre ...]   ->   ../fotos/comp_<nombre>.png (800 x 800)
"""
import bpy, math, os, random, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fotos")


def mat(name, color, rough=0.5, coat=0.0, sss=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    b = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:
        nodes.clear(); b = nodes.new("ShaderNodeBsdfPrincipled")
        m.node_tree.links.new(b.outputs[0], nodes.new("ShaderNodeOutputMaterial").inputs[0])
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Subsurface Weight"].default_value = sss
    return m


def rebozado(name, color, escala=0.06, fuerza=0.02, coat=0.15):
    """Material con relieve de rebozado (textura de ruido en el bump)."""
    m = mat(name, color, 0.55, coat)
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = 1 / escala
    noise.inputs["Detail"].default_value = 8
    bump = nt.nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6
    bump.inputs["Distance"].default_value = fuerza
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    return m


def suave(o, nivel=1):
    for p in o.data.polygons:
        p.use_smooth = True
    if nivel:
        o.modifiers.new("Suave", 'SUBSURF').levels = nivel
    return o


def ruido(o, fuerza=0.02, escala=0.2, nombre="Bultos"):
    d = o.modifiers.new(nombre, 'DISPLACE'); d.strength = fuerza
    t = bpy.data.textures.get(nombre) or bpy.data.textures.new(nombre, 'CLOUDS')
    t.noise_scale = escala
    d.texture = t
    return o


def bola(loc, esc, m, sub=3):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=1, location=loc)
    o = bpy.context.object; o.scale = esc
    o.rotation_euler.z = random.uniform(0, math.tau)
    o.data.materials.append(m)
    return o


def palo(loc, largo, grosor, rot, m, bisel=0.3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.scale = (largo, grosor, grosor); o.rotation_euler = rot
    b = o.modifiers.new("Bisel", 'BEVEL'); b.width = grosor * bisel; b.segments = 3
    o.data.materials.append(m)
    return o


def cuenco(r=0.75, h=0.32, color=(0.9, 0.88, 0.84)):
    prof = [(0.0, 0.0), (r * 0.55, 0.0), (r * 0.85, h * 0.4), (r, h), (r * 0.97, h), (r * 0.82, h * 0.42),
            (r * 0.52, 0.04), (0.0, 0.04)]
    mesh = bpy.data.meshes.new("Cuenco")
    mesh.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
    o = bpy.data.objects.new("Cuenco", mesh); bpy.context.scene.collection.objects.link(o)
    sc = o.modifiers.new("Giro", 'SCREW'); sc.steps = 64; sc.render_steps = 64
    o.data.materials.append(mat("Cerámica", color, 0.25, 0.6))
    return suave(o, 1)


# ---------- Productos ----------

ORO = (0.62, 0.32, 0.07)


def patatas_fritas():
    m = rebozado("Patata frita", (0.62, 0.30, 0.03), 0.03, 0.005)
    cuenco(0.7, 0.3, (0.75, 0.08, 0.04))
    for i in range(46):
        a = random.uniform(0, math.tau); r = random.uniform(0, 0.42)
        palo((r * math.cos(a), r * math.sin(a), 0.25 + random.uniform(0, 0.35)), random.uniform(0.6, 0.85), 0.07,
             (random.uniform(-0.9, 0.9), random.uniform(-0.6, 0.6), random.uniform(0, math.tau)), m)


def aros_cebolla():
    m = rebozado("Rebozado aro", (0.42, 0.17, 0.025), 0.05, 0.02)
    for i in range(8):
        a = i / 8 * math.tau + random.uniform(-0.2, 0.2); r = 0.42 if i < 6 else 0.12
        z = 0.07 + (0.12 if i >= 6 else 0) + random.uniform(0, 0.03)
        bpy.ops.mesh.primitive_torus_add(major_radius=random.uniform(0.2, 0.26), minor_radius=0.075,
                                         location=(r * math.cos(a), r * math.sin(a), z))
        o = bpy.context.object
        o.rotation_euler = (random.uniform(-0.25, 0.25), random.uniform(-0.25, 0.25), 0)
        o.scale.z = 0.8
        o.data.materials.append(m)
        suave(ruido(o, 0.025, 0.08, "Rebozado"), 1)


def alitas():
    m = rebozado("Alita glaseada", (0.22, 0.04, 0.008), 0.08, 0.01, coat=0.8)
    for i in range(6):
        a = i / 6 * math.tau; r = 0.4
        o = bola((r * math.cos(a), r * math.sin(a), 0.11), (0.28, 0.14, 0.11), m)
        o.rotation_euler.z = a + random.uniform(-0.4, 0.4)
        sd = o.modifiers.new("Curva", 'SIMPLE_DEFORM'); sd.deform_method = 'BEND'; sd.angle = 0.6
        suave(ruido(o, 0.03, 0.15), 1)
    cuenco(0.22, 0.12, (0.92, 0.92, 0.9))
    bola((0, 0, 0.09), (0.19, 0.19, 0.02), mat("Salsa ranchera", (0.92, 0.9, 0.82), 0.3, 0.4))


def pan_de_ajo():
    miga = rebozado("Pan tostado", (0.48, 0.22, 0.04), 0.04, 0.01)
    hierba = mat("Perejil", (0.08, 0.3, 0.05), 0.5)
    for i in range(5):
        x = (i - 2) * 0.27
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 0.06 + i * 0.012))
        o = bpy.context.object; o.scale = (0.24, 0.62, 0.08); o.rotation_euler = (0, math.radians(-14), 0)
        b = o.modifiers.new("Bisel", 'BEVEL'); b.width = 0.04; b.segments = 4
        o.data.materials.append(miga)
        suave(ruido(o, 0.015, 0.1), 0)
        for _ in range(9):
            bola((x + random.uniform(-0.05, 0.05) + 0.03, random.uniform(-0.28, 0.28), 0.12 + i * 0.012),
                 (0.012, 0.012, 0.004), hierba, 1)


def nuggets():
    m = rebozado("Nugget", (0.45, 0.19, 0.03), 0.04, 0.02)
    for i in range(8):
        a = i / 8 * math.tau + random.uniform(-0.15, 0.15); r = 0.45 if i < 6 else 0.15
        z = 0.08 + (0.1 if i >= 6 else 0)
        o = bola((r * math.cos(a), r * math.sin(a), z),
                 (random.uniform(0.17, 0.21), random.uniform(0.12, 0.15), 0.07), m)
        o.rotation_euler = (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(0, math.tau))
        suave(ruido(o, 0.035, 0.12), 1)


def ensalada_cesar():
    cuenco(0.85, 0.34)
    lechuga = mat("Lechuga", (0.05, 0.18, 0.02), 0.4, 0.2, 0.3)
    pollo = rebozado("Pollo plancha", (0.42, 0.20, 0.06), 0.06, 0.005)
    pan = rebozado("Picatoste", (0.45, 0.20, 0.04), 0.03, 0.01)
    queso = mat("Parmesano", (0.95, 0.88, 0.65), 0.5, 0.0, 0.2)
    for i in range(16):
        a = random.uniform(0, math.tau); r = random.uniform(0, 0.55)
        bpy.ops.mesh.primitive_grid_add(x_subdivisions=8, y_subdivisions=8, size=0.42,
                                        location=(r * math.cos(a), r * math.sin(a), 0.22 + random.uniform(0, 0.08)))
        o = bpy.context.object
        o.rotation_euler = (random.uniform(-0.6, 0.6), random.uniform(-0.6, 0.6), random.uniform(0, math.tau))
        o.data.materials.append(lechuga)
        o.modifiers.new("Grosor", 'SOLIDIFY').thickness = 0.01
        suave(ruido(o, 0.09, 0.12, "Hoja"), 1)
    for i in range(7):
        a = random.uniform(0, math.tau); r = random.uniform(0, 0.45)
        palo((r * math.cos(a), r * math.sin(a), 0.34), 0.2, 0.07, (0, 0, random.uniform(0, math.tau)), pollo)
    for i in range(8):
        a = random.uniform(0, math.tau); r = random.uniform(0, 0.5)
        palo((r * math.cos(a), r * math.sin(a), 0.36), 0.07, 0.07,
             (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)), pan)
    for i in range(10):
        a = random.uniform(0, math.tau); r = random.uniform(0, 0.5)
        palo((r * math.cos(a), r * math.sin(a), 0.38), 0.09, 0.01, (0, random.uniform(-0.4, 0.4), random.uniform(0, 3)),
             queso, 0.4)


def patatas_gajo():
    m = rebozado("Patata gajo", (0.42, 0.17, 0.03), 0.03, 0.008)
    piel = mat("Especias", (0.35, 0.12, 0.03), 0.6)
    for i in range(10):
        a = i / 10 * math.tau + random.uniform(-0.15, 0.15); r = random.uniform(0.25, 0.5)
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=0.11, depth=0.6,
                                            location=(r * math.cos(a), r * math.sin(a), 0.1 + (i % 3) * 0.04))
        o = bpy.context.object
        o.rotation_euler = (math.radians(90), random.uniform(-0.2, 0.2), a + random.uniform(-0.5, 0.5))
        b = o.modifiers.new("Bisel", 'BEVEL'); b.width = 0.04; b.segments = 4
        sd = o.modifiers.new("Curva", 'SIMPLE_DEFORM'); sd.deform_method = 'BEND'; sd.angle = 0.5
        o.data.materials.append(m)
        suave(o, 0)
        for _ in range(4):
            bola((o.location.x + random.uniform(-0.12, 0.12), o.location.y + random.uniform(-0.12, 0.12), o.location.z + 0.1),
                 (0.01, 0.01, 0.004), piel, 1)


def tequenos():
    m = rebozado("Masa tequeño", (0.50, 0.24, 0.05), 0.05, 0.006)
    for i in range(6):
        x = (i - 2.5) * 0.2
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.075, depth=0.75, location=(x, -0.12, 0.08))
        o = bpy.context.object
        o.rotation_euler = (math.radians(90), 0, random.uniform(-0.12, 0.12))
        b = o.modifiers.new("Bisel", 'BEVEL'); b.width = 0.05; b.segments = 4
        o.data.materials.append(m)
        suave(ruido(o, 0.01, 0.06), 1)
    cuenco(0.2, 0.12, (0.92, 0.92, 0.9)).location = (0.35, 0.5, 0)
    bola((0.35, 0.5, 0.09), (0.17, 0.17, 0.02), mat("Salsa guacamole", (0.25, 0.4, 0.06), 0.35, 0.3))


COMPLEMENTOS = {
    "patatas_fritas": patatas_fritas, "aros_cebolla": aros_cebolla, "alitas": alitas, "pan_de_ajo": pan_de_ajo,
    "nuggets": nuggets, "ensalada_cesar": ensalada_cesar, "patatas_gajo": patatas_gajo, "tequenos": tequenos,
}


def escena(build, ruta, semilla):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    random.seed(semilla)
    scene = bpy.context.scene
    build()

    # Tabla de pizarra redonda y suelo oscuro, como el fondo negro de las pizzas
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.05, depth=0.04, location=(0, 0, -0.02))
    tabla = bpy.context.object
    tabla.data.materials.append(mat("Pizarra", (0.012, 0.011, 0.011), 0.6))
    bpy.ops.mesh.primitive_plane_add(size=12, location=(0, 0, -0.04))
    bpy.context.object.data.materials.append(mat("Suelo", (0.006, 0.005, 0.004), 0.7))

    bpy.ops.object.camera_add(location=(0, -2.3, 2.6))
    cam = bpy.context.object; scene.camera = cam
    cam.rotation_euler = (math.radians(41), 0, 0); cam.data.lens = 50

    for loc, energy, color, size in [((2.2, -2.0, 3.0), 170, (1.0, 0.88, 0.75), 2.5),
                                     ((-2.0, 2.0, 1.5), 300, (1.0, 0.55, 0.25), 1.5),
                                     ((-2.5, -1.5, 1.5), 35, (0.85, 0.9, 1.0), 3)]:
        bpy.ops.object.light_add(type='AREA', location=loc)
        l = bpy.context.object; l.data.energy, l.data.color, l.data.size = energy, color, size
        l.constraints.new('TRACK_TO').target = tabla

    w = bpy.data.worlds.new("Mundo"); scene.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'

    r = scene.render
    r.engine = 'CYCLES'
    scene.cycles.samples = 96
    r.resolution_x = r.resolution_y = 800
    r.image_settings.file_format = 'PNG'
    r.filepath = ruta
    bpy.ops.render.render(write_still=True)


only = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
for i, (nombre, build) in enumerate(COMPLEMENTOS.items()):
    if only and nombre not in only:
        continue
    escena(build, os.path.join(OUT, f"comp_{nombre}.png"), 100 + i)
print("OK complementos")
