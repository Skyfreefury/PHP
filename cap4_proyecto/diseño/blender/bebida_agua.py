"""Foto de producto: botella de agua con gas de 50 cl, mismo fondo y luz que las pizzas.
Uso: blender -b --python bebida_agua.py   ->   ../fotos/bebida_agua.png (800 x 800)
"""
import bpy, math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fotos")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def mat(name, color, rough, transmission=0.0, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nodes = m.node_tree.nodes
    b = next((n for n in nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:
        nodes.clear(); b = nodes.new("ShaderNodeBsdfPrincipled")
        m.node_tree.links.new(b.outputs[0], nodes.new("ShaderNodeOutputMaterial").inputs[0])
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = transmission
    b.inputs["IOR"].default_value = ior
    return m


GLASS = mat("Vidrio verde", (0.55, 0.85, 0.65), 0.05, 1.0, 1.5)
CAP = mat("Tapón", (0.08, 0.30, 0.15), 0.35)
LABEL = mat("Etiqueta", (0.96, 0.94, 0.88), 0.6)
STRIPE = mat("Franja", (1.0, 0.35, 0.0), 0.5)

# Perfil de la botella girado sobre Z (screw)
prof = [(0.0, 0.0), (0.30, 0.0), (0.32, 0.03), (0.32, 1.05), (0.28, 1.25), (0.14, 1.55),
        (0.12, 1.75), (0.13, 1.78), (0.13, 1.82), (0.0, 1.82)]
mesh = bpy.data.meshes.new("Botella")
mesh.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
bottle = bpy.data.objects.new("Botella", mesh); scene.collection.objects.link(bottle)
sc = bottle.modifiers.new("Giro", 'SCREW'); sc.steps = 64; sc.render_steps = 64
bottle.modifiers.new("Grosor", 'SOLIDIFY').thickness = 0.015
bottle.modifiers.new("Suave", 'SUBSURF').levels = 2
bottle.data.materials.append(GLASS)

bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.145, depth=0.16, location=(0, 0, 1.86))
cap = bpy.context.object; cap.data.materials.append(CAP)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.325, depth=0.5, location=(0, 0, 0.62))
label = bpy.context.object; label.data.materials.append(LABEL)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.327, depth=0.06, location=(0, 0, 0.5))
band = bpy.context.object; band.data.materials.append(STRIPE)
for o in (bottle, cap, label, band):
    for p in o.data.polygons:
        p.use_smooth = True

# Suelo oscuro para recibir sombra
bpy.ops.mesh.primitive_plane_add(size=10)
floor = bpy.context.object
floor.data.materials.append(mat("Suelo", (0.012, 0.010, 0.008), 0.6))

bpy.ops.object.camera_add(location=(0, -4.2, 1.6))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(86), 0, 0); cam.data.lens = 50


def area(loc, energy, color, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object; l.data.energy, l.data.color, l.data.size = energy, color, size
    t = l.constraints.new('TRACK_TO'); t.target = bottle


area((2.2, -2.0, 3.0), 260, (1.0, 0.88, 0.75), 2.5)
area((-2.0, 2.0, 1.5), 420, (1.0, 0.55, 0.25), 1.5)
area((-2.5, -1.5, 1.5), 60, (0.85, 0.9, 1.0), 3)

w = bpy.data.worlds.new("Mundo"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

r = scene.render
r.engine = 'CYCLES'  # el vidrio necesita trazado de rayos
scene.cycles.samples = 96
r.resolution_x = r.resolution_y = 800
r.image_settings.file_format = 'PNG'
r.filepath = os.path.join(OUT, "bebida_agua.png")
bpy.ops.render.render(write_still=True)
print("OK agua")
