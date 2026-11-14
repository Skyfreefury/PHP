"""Pizza Margherita napolitana procedural: cornicione inflado e irregular con
manchas tostadas, salsa San Marzano, mozzarella en trozos fundidos y albahaca.
Guarda pizza_napolitana.blend y un render fijo (hero_frame.png).
Uso: blender -b --python pizza_napolitana.py
"""
import bpy, bmesh, math, random, os
from mathutils import Vector, noise

OUT = os.path.dirname(os.path.abspath(__file__))
random.seed(11)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 240


# ---------- Materiales ----------
def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    return m, nt, bsdf


def link(nt, a, b):
    nt.links.new(a, b)


def mix_color(nt, fac, a, b):
    """Mezcla dos colores con ShaderNodeMix en modo RGBA."""
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type = 'RGBA'
    link(nt, fac, mx.inputs[0])
    if isinstance(a, tuple):
        mx.inputs[6].default_value = (*a, 1)
    else:
        link(nt, a, mx.inputs[6])
    if isinstance(b, tuple):
        mx.inputs[7].default_value = (*b, 1)
    else:
        link(nt, b, mx.inputs[7])
    return mx.outputs[2]


def ramp(nt, src, stops):
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    els[0].position, els[0].color = stops[0][0], (*stops[0][1], 1)
    els[1].position, els[1].color = stops[1][0], (*stops[1][1], 1)
    for pos, col in stops[2:]:
        e = els.new(pos)
        e.color = (*col, 1)
    link(nt, src, r.inputs[0])
    return r.outputs[0]


def bump(nt, bsdf, height, strength):
    b = nt.nodes.new("ShaderNodeBump")
    b.inputs["Strength"].default_value = strength
    link(nt, height, b.inputs["Height"])
    link(nt, b.outputs["Normal"], bsdf.inputs["Normal"])


# Masa: dorada con zonas tostadas y manchas de leopardo casi negras
M_DOUGH, nt, bsdf = new_mat("Masa")
coord = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
n1 = nt.nodes.new("ShaderNodeTexNoise"); n1.inputs["Scale"].default_value = 4; n1.inputs["Detail"].default_value = 8
link(nt, coord, n1.inputs["Vector"])
base = ramp(nt, n1.outputs["Fac"], [(0.3, (0.62, 0.36, 0.14)), (0.5, (0.45, 0.21, 0.06)), (0.68, (0.22, 0.09, 0.03))])
vor = nt.nodes.new("ShaderNodeTexNoise"); vor.inputs["Scale"].default_value = 11; vor.inputs["Detail"].default_value = 3; vor.inputs["Distortion"].default_value = 0.6
link(nt, coord, vor.inputs["Vector"])
n2 = nt.nodes.new("ShaderNodeTexNoise"); n2.inputs["Scale"].default_value = 3
link(nt, coord, n2.inputs["Vector"])
# Las manchas solo aparecen donde el segundo ruido es alto (la parte más expuesta al fuego)
spots = ramp(nt, vor.outputs["Fac"], [(0.58, (0, 0, 0)), (0.64, (1, 1, 1))])
mask = ramp(nt, n2.outputs["Fac"], [(0.4, (0, 0, 0)), (0.52, (1, 1, 1))])
mm = nt.nodes.new("ShaderNodeMath"); mm.operation = 'MULTIPLY'
link(nt, spots, mm.inputs[0]); link(nt, mask, mm.inputs[1])
col = mix_color(nt, mm.outputs[0], base, (0.05, 0.03, 0.02))
link(nt, col, bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.85
bump(nt, bsdf, n1.outputs["Fac"], 0.5)

# Salsa San Marzano: rojo con variación y brillo de aceite
M_SAUCE, nt, bsdf = new_mat("Tomate")
coord = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 9; n.inputs["Detail"].default_value = 6
link(nt, coord, n.inputs["Vector"])
link(nt, ramp(nt, n.outputs["Fac"], [(0.3, (0.45, 0.04, 0.015)), (0.7, (0.25, 0.02, 0.008))]), bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.55
bsdf.inputs["Coat Weight"].default_value = 0.05
bump(nt, bsdf, n.outputs["Fac"], 0.25)

# Mozzarella fior di latte: blanco cremoso, translúcido, con algún dorado
M_CHEESE, nt, bsdf = new_mat("Mozzarella")
coord = nt.nodes.new("ShaderNodeTexCoord").outputs["Object"]
n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = 6
link(nt, coord, n.inputs["Vector"])
link(nt, ramp(nt, n.outputs["Fac"], [(0.5, (0.93, 0.89, 0.78)), (0.66, (0.78, 0.55, 0.28))]), bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.35
bsdf.inputs["Subsurface Weight"].default_value = 0.3
bump(nt, bsdf, n.outputs["Fac"], 0.2)

# Albahaca: verde oscuro brillante
M_BASIL, nt, bsdf = new_mat("Albahaca")
bsdf.inputs["Base Color"].default_value = (0.02, 0.11, 0.015, 1)
bsdf.inputs["Roughness"].default_value = 0.3
bsdf.inputs["Subsurface Weight"].default_value = 0.1

root = bpy.data.objects.new("Pizza", None)
scene.collection.objects.link(root)


def adopt(o, mat):
    o.parent = root
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


# ---------- Cornicione irregular ----------
R = 1.0
bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=0.17, major_segments=160, minor_segments=32)
crust = bpy.context.object; crust.name = "Cornicione"
for v in crust.data.vertices:
    a = math.atan2(v.co.y, v.co.x)
    c = Vector((math.cos(a), math.sin(a), 0)) * R
    d = v.co - c
    # Grosor del borde variable: burbujas grandes y pequeñas
    f = 1 + 0.22 * math.sin(3 * a + 1) + 0.12 * math.sin(7 * a + 2) + 0.08 * math.sin(13 * a + 0.5)
    f += 0.15 * noise.noise(c * 3)
    d *= f
    if d.z < 0:
        d.z *= 0.35  # base plana
    v.co = c + d
crust.scale.z = 0.85
tex = bpy.data.textures.new("Burbujas", 'CLOUDS'); tex.noise_scale = 0.12
dm = crust.modifiers.new("Burbujas", 'DISPLACE'); dm.texture = tex; dm.strength = 0.04
adopt(crust, M_DOUGH)


# ---------- Discos con borde irregular ----------
def disc(name, radius, z, wobble, mat, thickness):
    bm = bmesh.new()
    verts = []
    for i in range(128):
        a = i / 128 * math.tau
        r = radius * (1 + wobble * noise.noise(Vector((math.cos(a), math.sin(a), 0)) * 2.5))
        verts.append(bm.verts.new((r * math.cos(a), r * math.sin(a), z)))
    bm.faces.new(verts)
    bmesh.ops.poke(bm, faces=bm.faces[:])
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o)
    s = o.modifiers.new("Grosor", 'SOLIDIFY'); s.thickness = thickness
    return adopt(o, mat)


disc("Base", 1.0, 0.0, 0.0, M_DOUGH, 0.05)
sauce = disc("Salsa", 0.88, 0.012, 0.04, M_SAUCE, 0.012)

# ---------- Mozzarella en trozos fundidos ----------
taken = []
cheese_tex = bpy.data.textures.new("Fundido", 'CLOUDS'); cheese_tex.noise_scale = 0.06
for i in range(7):
    for _ in range(200):
        r = math.sqrt(random.uniform(0, 0.62 ** 2)); a = random.uniform(0, math.tau)
        p = Vector((r * math.cos(a), r * math.sin(a), 0))
        if all((p - q).length > 0.34 for q in taken):
            taken.append(p); break
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=random.uniform(0.15, 0.21), location=(p.x, p.y, 0.01))
    o = bpy.context.object; o.name = f"Mozzarella.{i}"
    o.scale = (random.uniform(0.8, 1.3), random.uniform(0.7, 1.1), 0.3)
    o.rotation_euler.z = random.uniform(0, math.tau)
    d = o.modifiers.new("Fundido", 'DISPLACE'); d.texture = cheese_tex; d.strength = 0.09
    o.modifiers.new("Suave", 'SUBSURF').levels = 1
    adopt(o, M_CHEESE)


# ---------- Superficie auxiliar (salsa + mozzarella) para pegar las hojas ----------
dg = bpy.context.evaluated_depsgraph_get()
sbm = bmesh.new()
for o in root.children:
    if o.name.startswith(("Salsa", "Mozzarella")):
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
        me.transform(o.matrix_world)
        sbm.from_mesh(me)
        bpy.data.meshes.remove(me)
smesh = bpy.data.meshes.new("Superficie"); sbm.to_mesh(smesh); sbm.free()
surface = bpy.data.objects.new("Superficie", smesh); scene.collection.objects.link(surface)
surface.hide_render = True; surface.hide_viewport = True


# ---------- Albahaca (4 hojas con forma de hoja y curvatura) ----------
def leaf(name, loc, rot, size):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=16, y_subdivisions=8, size=1)
    o = bpy.context.object; o.name = name
    for v in o.data.vertices:
        t = v.co.x + 0.5                      # 0 en el tallo, 1 en la punta
        w = 0.42 * math.sin(math.pi * t) ** 0.8 * (1 - 0.35 * t)
        y = v.co.y * 2 * w
        z = 0.12 * abs(y) - 0.05 * (v.co.x ** 2)  # pliegue suave
        v.co = Vector((v.co.x, y, z))
    o.scale = (size * 1.25, size * 0.8, size)
    o.location = loc
    o.rotation_euler = (0, 0, rot)
    # Proyecta la hoja hacia abajo sobre la salsa o la mozzarella
    sw = o.modifiers.new("Pegar", 'SHRINKWRAP'); sw.target = surface
    sw.wrap_method = 'PROJECT'; sw.use_project_z = True
    sw.use_negative_direction = True; sw.use_positive_direction = True
    sw.wrap_mode = 'ABOVE_SURFACE'; sw.offset = 0.022
    sm = o.modifiers.new("Suave", 'SMOOTH'); sm.factor = 0.8; sm.iterations = 6
    s = o.modifiers.new("Grosor", 'SOLIDIFY'); s.thickness = 0.008
    return adopt(o, M_BASIL)


for i, (x, y, rz) in enumerate([(0.12, 0.05, 0.6), (-0.30, 0.35, 2.4), (0.38, -0.32, 4.1), (-0.15, -0.45, 1.2)]):
    leaf(f"Albahaca.{i}", (x, y, 0.3), rz, random.uniform(0.2, 0.26))

# ---------- Animación: giro lento de 8 s ----------
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
for f, rz in ((1, 0), (241, math.tau)):
    root.rotation_euler = (0, 0, rz)
    root.keyframe_insert("rotation_euler", frame=f)

# ---------- Cámara y luz cálida de horno ----------
bpy.ops.object.camera_add(location=(0, -3.6, 2.3))
cam = bpy.context.object; scene.camera = cam
tr = cam.constraints.new('TRACK_TO'); tr.target = root
cam.data.lens = 42
cam.data.dof.use_dof = True
cam.data.dof.focus_object = root
cam.data.dof.aperture_fstop = 3.5


def area(loc, energy, color, size):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object
    l.data.energy, l.data.color, l.data.size = energy, color, size
    t = l.constraints.new('TRACK_TO'); t.target = root
    return l


area((2.2, -2.0, 3.0), 180, (1.0, 0.88, 0.75), 2.5)   # principal
area((-2.4, 2.4, 1.2), 420, (1.0, 0.55, 0.25), 1.5)   # contraluz anaranjado del horno
area((-2.5, -1.5, 1.5), 40, (0.85, 0.9, 1.0), 3)      # relleno

w = bpy.data.worlds.new("Mundo"); scene.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "pizza_napolitana.blend"))

# Render fijo para revisar y para Figma
r = scene.render
r.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 64
r.resolution_x, r.resolution_y = 1920, 1080
r.image_settings.file_format = 'PNG'
scene.frame_set(1)
r.filepath = os.path.join(OUT, "hero_frame.png")
bpy.ops.render.render(write_still=True)
print("OK napolitana")
