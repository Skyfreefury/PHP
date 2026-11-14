"""Renderiza el giro de la pizza (240 fotogramas, 8 s) a MP4 para el fondo del inicio.
Uso: blender -b pizza.blend --python render_video.py
"""
import bpy, os

OUT = os.path.dirname(bpy.data.filepath)
scene = bpy.context.scene
r = scene.render
r.resolution_x, r.resolution_y = 1280, 720
r.film_transparent = False
scene.world.color = (0.0045, 0.0035, 0.003)  # #0E0B09 en lineal
bg = scene.world.node_tree.nodes.get('Background') if scene.world.node_tree else None
if bg: bg.inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
scene.view_settings.view_transform = 'Standard'

# Encuadre centrado: la cámara apunta al centro de la pizza
cam = scene.camera
cam.location = (0, -3.9, 2.3)
cam.data.lens = 40

# Blender 5 separa imagen y vídeo; Blender 4 usa file_format FFMPEG
try:
    r.image_settings.media_type = 'VIDEO'
except (AttributeError, TypeError):
    pass
r.image_settings.file_format = 'FFMPEG'
r.ffmpeg.format = 'MPEG4'
r.ffmpeg.codec = 'H264'
r.ffmpeg.constant_rate_factor = 'MEDIUM'
r.filepath = os.path.join(OUT, "pizza_giro.mp4")
bpy.ops.render.render(animation=True)
print("OK video", r.filepath)
