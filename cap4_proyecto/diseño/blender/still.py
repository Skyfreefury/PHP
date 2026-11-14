import bpy, os
s = bpy.context.scene; r = s.render
r.resolution_x, r.resolution_y = 1920, 1080
r.film_transparent = False
s.world.color = (0.0045, 0.0035, 0.003)
bg = s.world.node_tree.nodes.get('Background') if s.world.node_tree else None
if bg: bg.inputs[0].default_value = (0.0045, 0.0035, 0.003, 1)
s.view_settings.view_transform = 'Standard'
cam = s.camera; cam.location = (0, -3.9, 2.3); cam.data.lens = 40
s.frame_set(60)
r.image_settings.file_format = 'PNG'
r.filepath = os.path.join(os.path.dirname(bpy.data.filepath), "hero_frame.png")
bpy.ops.render.render(write_still=True)
