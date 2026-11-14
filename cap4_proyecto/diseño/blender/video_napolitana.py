"""Vídeo corto en bucle sin corte: giro muy lento y fundido del final sobre el inicio.
Uso: blender -b pizza_napolitana.blend --python video_napolitana.py
- Bucle de 6 s (180 fotogramas) a 30 fps.
- Giro de 1,5 grados por segundo (antes 45): 11,25 grados en los 225 fotogramas renderizados.
- Los últimos 45 fotogramas se funden sobre los 45 primeros, así el final enlaza con el inicio.
"""
import bpy, os, math, shutil

LOOP, FADE = 180, 45
TOTAL = LOOP + FADE
DEG_PER_FRAME = 1.5 / 30
OUT = os.path.dirname(bpy.data.filepath)
FRAMES = os.path.join(OUT, "frames")
shutil.rmtree(FRAMES, ignore_errors=True)
os.makedirs(FRAMES)

s = bpy.context.scene
root = bpy.data.objects["Pizza"]
root.animation_data_clear()
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
for f in (1, TOTAL):
    root.rotation_euler = (0, 0, math.radians(DEG_PER_FRAME * (f - 1)))
    root.keyframe_insert("rotation_euler", frame=f)

# 1) Fotogramas de la pizza girando
r = s.render
r.engine = 'BLENDER_EEVEE'
s.eevee.taa_render_samples = 32
r.resolution_x, r.resolution_y = 1280, 720
s.frame_start, s.frame_end = 1, TOTAL
r.image_settings.file_format = 'PNG'
r.filepath = os.path.join(FRAMES, "f_")
bpy.ops.render.render(animation=True)

# 2) Escena de montaje: inicio debajo, final encima con opacidad 1 -> 0
edit = bpy.data.scenes.new("Bucle")
edit.render.resolution_x, edit.render.resolution_y = 1280, 720
edit.render.fps = 30
edit.frame_start, edit.frame_end = 1, LOOP
edit.view_settings.view_transform = 'Standard'
se = edit.sequence_editor_create()
strips = se.strips if hasattr(se, "strips") else se.sequences
names = [f"f_{i:04d}.png" for i in range(1, TOTAL + 1)]

def image_strip(name, files, channel):
    st = strips.new_image(name=name, filepath=os.path.join(FRAMES, files[0]), channel=channel, frame_start=1)
    for fn in files[1:]:
        st.elements.append(fn)
    return st

base = image_strip("Inicio", names[:LOOP], 1)
tail = image_strip("Final", names[LOOP:], 2)
tail.blend_type = 'ALPHA_OVER'
tail.blend_alpha = 1.0; tail.keyframe_insert("blend_alpha", frame=1)
tail.blend_alpha = 0.0; tail.keyframe_insert("blend_alpha", frame=FADE)

er = edit.render
try:
    er.image_settings.media_type = 'VIDEO'
except (AttributeError, TypeError):
    pass
er.image_settings.file_format = 'FFMPEG'
er.ffmpeg.format = 'MPEG4'; er.ffmpeg.codec = 'H264'; er.ffmpeg.constant_rate_factor = 'HIGH'
er.filepath = os.path.join(OUT, "pizza_giro.mp4")
bpy.ops.render.render(animation=True, scene=edit.name)
shutil.rmtree(FRAMES, ignore_errors=True)
print("OK bucle")
