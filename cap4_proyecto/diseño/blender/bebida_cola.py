"""Foto de producto: lata de refresco de cola de 33 cl, sin logotipo. Mismo fondo y luz que el agua.
Uso: blender -b --python bebida_cola.py   ->   ../fotos/bebida_cola.png (800 x 800)
"""
import bpy, math, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fotos")
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def mat(name, color, rough, metal=0.0, coat=0.0):
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
    return m


RED = mat("Lata roja", (0.55, 0.01, 0.01), 0.3, 0.6, 0.6)
ALU = mat("Aluminio", (0.8, 0.8, 0.82), 0.25, 1.0)
WHITE = mat("Franja blanca", (0.92, 0.92, 0.9), 0.35, 0.2, 0.4)

# Perfil de la lata girado sobre Z: cuerpo, hombro y cuello
prof = [(0.0, 0.0), (0.24, 0.0), (0.33, 0.06), (0.33, 1.12), (0.27, 1.24), (0.26, 1.26), (0.0, 1.26)]
mesh = bpy.data.meshes.new("Lata")
mesh.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
can = bpy.data.objects.new("Lata", mesh); scene.collection.objects.link(can)
sc = can.modifiers.new("Giro", 'SCREW'); sc.steps = 64; sc.render_steps = 64
can.data.materials.append(RED)

# Tapa y base de aluminio, franja blanca lisa sin marca
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.262, depth=0.02, location=(0, 0, 1.265))
top = bpy.context.object; top.data.materials.append(ALU)
bpy.ops.mesh.primitive_torus_add(major_radius=0.27, minor_radius=0.012, location=(0, 0, 1.27))
rim = bpy.context.object; rim.data.materials.append(ALU)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.332, depth=0.025, location=(0, 0, 0.72))
band = bpy.context.object; band.data.materials.append(WHITE)
for o in (can, top, rim, band):
    for p in o.data.polygons:
        p.use_smooth = True

bpy.ops.mesh.primitive_plane_add(size=10)
bpy.context.object.data.materials.append(mat("Suelo", (0.012, 0.010, 0.008), 0.6))

bpy.ops.object.camera_add(location=(0, -3.0, 0.95))
cam = bpy.context.object; scene.camera = cam
cam.rotation_euler = (math.radians(84), 0, 0); cam.data.lens = 50


def area(loc, energy, color, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object; l.data.energy, l.data.color, l.data.size = energy, color, size
    l.constraints.new('TRACK_TO').target = can


area((2.2, -2.0, 3.0), 260, (1.0, 0.88, 0.75), 2.5)
area((-2.0, 2.0, 1.5), 420, (1.0, 0.55, 0.25), 1.5)
area((-2.5, -1.5, 1.5), 60, (0.85, 0.9, 1.0), 3)

w = bpy.data.worlds.new("Mundo"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

r = scene.render
r.engine = 'CYCLES'
scene.cycles.samples = 96
r.resolution_x = r.resolution_y = 800
r.image_settings.file_format = 'PNG'
r.filepath = os.path.join(OUT, "bebida_cola.png")
bpy.ops.render.render(write_still=True)
print("OK cola")
