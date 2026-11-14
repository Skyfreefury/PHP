"""Genera una pizza 3D procedural, la anima (giro lento) y exporta .blend + .glb.
Uso: blender -b --python pizza.py
"""
import bpy, bmesh, math, random, os
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
random.seed(7)

# Escena limpia
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 240

def mat(name, color, rough=0.6, sss=0.0, spec=0.3):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    if "Subsurface Weight" in b.inputs:
        b.inputs["Subsurface Weight"].default_value = sss
    return m

M_CRUST = mat("Masa", (0.55, 0.26, 0.07), 0.8)
M_SAUCE = mat("Tomate", (0.55, 0.06, 0.02), 0.35)
M_CHEESE = mat("Queso", (0.95, 0.58, 0.12), 0.4, sss=0.2)
M_PEPP = mat("Pepperoni", (0.45, 0.04, 0.02), 0.35)
M_BASIL = mat("Albahaca", (0.08, 0.32, 0.06), 0.5)
M_OLIVE = mat("Aceituna", (0.04, 0.03, 0.03), 0.25)

root = bpy.data.objects.new("Pizza", None)
scene.collection.objects.link(root)

def parent(o):
    o.parent = root
    return o

# Borde de masa (toro achatado)
bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.14,
                                 major_segments=96, minor_segments=24)
crust = parent(bpy.context.object); crust.name = "Borde"
crust.scale.z = 0.85
crust.data.materials.append(M_CRUST)
bpy.ops.object.shade_smooth()

# Base de masa
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.0, depth=0.06,
                                    location=(0, 0, -0.03))
base = parent(bpy.context.object); base.name = "Base"
base.data.materials.append(M_CRUST)

# Salsa
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.93, depth=0.02,
                                    location=(0, 0, 0.01))
sauce = parent(bpy.context.object); sauce.name = "Salsa"
sauce.data.materials.append(M_SAUCE)

# Queso: disco subdividido con ruido para que parezca fundido
bpy.ops.mesh.primitive_circle_add(vertices=96, radius=0.9, fill_type='NGON',
                                  location=(0, 0, 0.03))
cheese = parent(bpy.context.object); cheese.name = "Queso"
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.poke()
bpy.ops.mesh.subdivide(number_cuts=3)
bpy.ops.object.mode_set(mode='OBJECT')
tex = bpy.data.textures.new("Burbujas", 'CLOUDS'); tex.noise_scale = 0.18
d = cheese.modifiers.new("Fundido", 'DISPLACE'); d.texture = tex; d.strength = 0.035
s = cheese.modifiers.new("Grosor", 'SOLIDIFY'); s.thickness = 0.02
cheese.modifiers.new("Suave", 'SUBSURF').levels = 1
cheese.data.materials.append(M_CHEESE)
bpy.ops.object.shade_smooth()

def scatter(n, rmin, rmax, minsep, taken):
    pts = []
    tries = 0
    while len(pts) < n and tries < 2000:
        tries += 1
        r = math.sqrt(random.uniform(rmin**2, rmax**2))
        a = random.uniform(0, math.tau)
        p = Vector((r * math.cos(a), r * math.sin(a), 0))
        if all((p - q).length > minsep for q in taken + pts):
            pts.append(p)
    taken.extend(pts)
    return pts

taken = []
# Pepperoni
for i, p in enumerate(scatter(11, 0.0, 0.72, 0.30, taken)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=0.12, depth=0.025,
                                        location=(p.x, p.y, 0.075))
    o = parent(bpy.context.object); o.name = f"Pepperoni.{i:02d}"
    o.rotation_euler = (random.uniform(-.08, .08), random.uniform(-.08, .08), 0)
    bev = o.modifiers.new("Bisel", 'BEVEL'); bev.width = 0.008; bev.segments = 3
    o.data.materials.append(M_PEPP)
    bpy.ops.object.shade_smooth()

# Aceitunas (toros pequeños)
for i, p in enumerate(scatter(8, 0.1, 0.78, 0.18, taken)):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.04, minor_radius=0.018,
                                     location=(p.x, p.y, 0.08))
    o = parent(bpy.context.object); o.name = f"Aceituna.{i:02d}"
    o.data.materials.append(M_OLIVE)
    bpy.ops.object.shade_smooth()

# Albahaca (hojas: esfera aplastada y estirada)
for i, p in enumerate(scatter(6, 0.1, 0.7, 0.2, taken)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.07,
                                         location=(p.x, p.y, 0.09))
    o = parent(bpy.context.object); o.name = f"Albahaca.{i:02d}"
    o.scale = (1.6, 0.8, 0.12)
    o.rotation_euler.z = random.uniform(0, math.tau)
    o.data.materials.append(M_BASIL)
    bpy.ops.object.shade_smooth()

# Animación: giro lento de 360º en 8 s, con leve balanceo
root.rotation_mode = 'XYZ'
# Blender 5 usa acciones por capas: la interpolación se fija antes de insertar claves
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
for f, rz, rx in ((1, 0, math.radians(-8)), (121, math.pi, math.radians(-4)),
                  (241, math.tau, math.radians(-8))):
    root.rotation_euler = (rx, 0, rz)
    root.keyframe_insert("rotation_euler", frame=f)

# Cámara y luces para la vista previa
bpy.ops.object.camera_add(location=(0, -2.6, 2.2))
cam = bpy.context.object; scene.camera = cam
t = cam.constraints.new('TRACK_TO'); t.target = root
cam.data.lens = 40
bpy.ops.object.light_add(type='AREA', location=(2, -2, 3)); bpy.context.object.data.energy = 120
bpy.ops.object.light_add(type='AREA', location=(-2, 1, 2)); bpy.context.object.data.energy = 50
w = bpy.data.worlds.new("Mundo"); w.color = (0.03, 0.025, 0.02); scene.world = w

# Aplicar modificadores para que el .glb lleve la geometría final
bpy.ops.object.select_all(action='DESELECT')
for o in root.children:
    if o.modifiers:
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
        o.select_set(False)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "pizza.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "pizza.glb"),
                          export_format='GLB', export_animations=True,
                          export_cameras=False, export_lights=False)

# Render fijo para Figma
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in \
    [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = scene.render.resolution_y = 1200
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'
scene.frame_set(30)
scene.render.filepath = os.path.join(OUT, "pizza_render.png")
bpy.ops.render.render(write_still=True)
print("OK pizza exportada en", OUT)
