bl_info = {
  "name" : "The Cherry Picker",
  "category": "3D View",
  "author": "Corwin Smith"
}

import bpy

class cherry_picker(bpy.types.Panel):
    bl_label = "Frame Cherry Picker"
    bl_id = "view3D.custom_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    filepath = bpy.data.scenes[0].render.filepath
    renderFrames = []

    # def render(renderFrames):
    #     for frame in renderFrames:
    #         bpy.data.scenes[0].frame_current = frame
    #         renderpath = filepath + str(bpy.data.scenes[0].frame_current)
    #         bpy.data.scenes[0].render.filepath = renderpath
    #         bpy.ops.render.render(write_still = True)
    #         print(bpy.data.scenes[0].frame_current)
    #     bpy.data.scenes[0].render.filepath = filepath

    def draw(self, context):
        layout = self.layout

        # Layout for entering frames that need to be rendered
        row = layout.row()
        row.label("Enter frames to render:")
        row = layout.row()
        row.prop(context.scene, "render_frames_cherry_picker")


def register():
    bpy.utils.register_class(cherry_picker)
    bpy.types.Scene.render_frames_cherry_picker = bpy.props.StringProperty (name = "", description = "Frames", default = "default")

def unregister():
    bpy.utils.unregister_class(cherry_picker)
    del bpy.types.Scene.render_frames_cherry_picker

if __name__ == "__main__":
    register()
