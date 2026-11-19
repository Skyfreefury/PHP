"""Fotos de producto de las 6 bebidas restantes, sin logotipos. Mismo fondo y luz que bebida_cola.py y bebida_agua.py.
Uso: blender -b --python bebidas_resto.py [-- nombre ...]   ->   ../fotos/bebida_<nombre>.png (800 x 800)
"""
import bpy, math, os, sys

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fotos")


def mat(name, color, rough, metal=0.0, coat=0.0, transmission=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nodes = m.node_tree.nodes
    b = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:
        nodes.clear(); b = nodes.new("ShaderNodeBsdfPrincipled")
        m.node_tree.links.new(b.outputs[0], nodes.new("ShaderNodeOutputMaterial").inputs[0])
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = transmission
    b.inputs["IOR"].default_value = ior
    return m


def lathe(name, prof, m, thick=0.0):
    """Gira un perfil (x, z) sobre el eje Z."""
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
    o = bpy.data.objects.new(name, mesh); bpy.context.scene.collection.objects.link(o)
    sc = o.modifiers.new("Giro", 'SCREW'); sc.steps = 64; sc.render_steps = 64
    if thick:
        o.modifiers.new("Grosor", 'SOLIDIFY').thickness = thick
        o.modifiers.new("Suave", 'SUBSURF').levels = 2
    o.data.materials.append(m)
    return o


def cyl(r, depth, z, m):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=depth, location=(0, 0, z))
    o = bpy.context.object; o.data.materials.append(m)
    return o


def lata(color, banda):
    """Lata de 33 cl como bebida_cola.py, con otro color."""
    body = mat("Lata", color, 0.3, 0.6, 0.6)
    alu = mat("Aluminio", (0.8, 0.8, 0.82), 0.25, 1.0)
    prof = [(0.0, 0.0), (0.24, 0.0), (0.33, 0.06), (0.33, 1.12), (0.27, 1.24), (0.26, 1.26), (0.0, 1.26)]
    can = lathe("Lata", prof, body)
    cyl(0.262, 0.02, 1.265, alu)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.27, minor_radius=0.012, location=(0, 0, 1.27))
    bpy.context.object.data.materials.append(alu)
    cyl(0.332, 0.025, 0.72, mat("Franja", banda, 0.35, 0.2, 0.4))
    return can, (0, -3.0, 0.95), 84


def botella(vidrio, tapon, etiqueta, franja, liquido=None, alta=1.0):
    """Botella de vidrio como bebida_agua.py. 'liquido' rellena la botella (zumo)."""
    glass = mat("Vidrio", vidrio, 0.05, transmission=1.0, ior=1.5)
    prof = [(0.0, 0.0), (0.30, 0.0), (0.32, 0.03), (0.32, 1.05 * alta), (0.28, 1.25 * alta), (0.14, 1.55 * alta),
            (0.12, 1.75 * alta), (0.13, 1.78 * alta), (0.13, 1.82 * alta), (0.0, 1.82 * alta)]
    b = lathe("Botella", prof, glass, thick=0.015)
    if liquido:
        juice = mat("Líquido", liquido, 0.15, transmission=0.6, ior=1.34)
        lprof = [(0.0, 0.02), (0.295, 0.02), (0.295, 1.0 * alta), (0.26, 1.2 * alta), (0.0, 1.2 * alta)]
        lathe("Liquido", lprof, juice)
    cyl(0.145, 0.16, 1.86 * alta, mat("Tapón", tapon, 0.35, 0.5 if tapon[0] > 0.5 else 0.0))
    cyl(0.325, 0.5, 0.62, mat("Etiqueta", etiqueta, 0.6))
    cyl(0.327, 0.06, 0.5, mat("Franja", franja, 0.5))
    return b, (0, -4.2, 1.6 * alta), 86


BEBIDAS = {
    "cola_zero": lambda: lata((0.02, 0.02, 0.02), (0.6, 0.02, 0.01)),
    "fanta": lambda: lata((0.85, 0.22, 0.0), (0.05, 0.15, 0.5)),
    "nestea": lambda: lata((0.55, 0.30, 0.02), (0.95, 0.8, 0.2)),
    "agua_gas": lambda: botella((0.75, 0.88, 0.95), (0.05, 0.2, 0.55), (0.96, 0.96, 0.96), (0.1, 0.4, 0.85)),
    "cerveza": lambda: botella((0.35, 0.15, 0.03), (0.85, 0.7, 0.3), (0.92, 0.85, 0.6), (0.6, 0.05, 0.02),
                               liquido=(0.55, 0.28, 0.02), alta=1.05),
    "zumo": lambda: botella((0.95, 0.95, 0.95), (0.95, 0.45, 0.02), (0.96, 0.94, 0.88), (0.2, 0.55, 0.15),
                            liquido=(1.0, 0.45, 0.02), alta=0.9),
}


def escena(build, ruta):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    target, cam_loc, cam_rx = build()
    for o in scene.objects:
        if o.type == 'MESH':
            for p in o.data.polygons:
                p.use_smooth = True

    bpy.ops.mesh.primitive_plane_add(size=10)
    bpy.context.object.data.materials.append(mat("Suelo", (0.012, 0.010, 0.008), 0.6))

    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.object; scene.camera = cam
    cam.rotation_euler = (math.radians(cam_rx), 0, 0); cam.data.lens = 50

    for loc, energy, color, size in [((2.2, -2.0, 3.0), 260, (1.0, 0.88, 0.75), 2.5),
                                     ((-2.0, 2.0, 1.5), 420, (1.0, 0.55, 0.25), 1.5),
                                     ((-2.5, -1.5, 1.5), 60, (0.85, 0.9, 1.0), 3)]:
        bpy.ops.object.light_add(type='AREA', location=loc)
        l = bpy.context.object; l.data.energy, l.data.color, l.data.size = energy, color, size
        l.constraints.new('TRACK_TO').target = target

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
for nombre, build in BEBIDAS.items():
    if only and nombre not in only:
        continue
    escena(build, os.path.join(OUT, f"bebida_{nombre}.png"))
print("OK bebidas")
