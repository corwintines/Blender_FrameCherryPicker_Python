bl_info = {
  "name" : "The Cherry Picker",
  "category": "3D View",
  "author": "Corwin Smith"
}

import bpy

class cherry_picker(bpy.types.Panel):
    bl_label = "Frame Cherry Picker"
    bl_id = "view3D.custom_menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout

        # Layout for entering frames that need to be rendered
        row = layout.row()
        row.label("Enter frames to render:")
        row = layout.row()
        row.prop(context.scene, "render_frames_cherry_picker")
        row = layout.row()
        row.operator("frame.cherrypicker")

class OBJECT_OT_BUTTON(bpy.types.Operator):
    bl_idname = "frame.cherrypicker"
    bl_label = "Submit"

    def convert_string(frame_string, frames_render):


    def render_frames(frames_render):
        filepath = bpy.data.scenes[0].render.filepath
        for frame in frames_render:
            bpy.data.scenes[0].frame_current = frame
            renderpath = filepath + str(bpy.data.scenes[0].frame_current)
            bpy.data.scenes[0].render.filepath = renderpath
            bpy.ops.render.render(write_still = True)
            print(bpy.data.scenes[0].frame_current)
        bpy.data.scenes[0].render.filepath = filepath

    def execute(self, context):
        frame_string = bpy.data.scenes[0].render_frames_cherry_picker
        frames_render = []
        convert_string(frame_string, frames_render)
        render_frames(frames_render)
        return{'FINISHED'}


def register():
    bpy.utils.register_class(cherry_picker)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.render_frames_cherry_picker = bpy.props.StringProperty (name = "", description = "Frames", default = "default")

def unregister():
    bpy.utils.unregister_class(cherry_picker)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.render_frames_cherry_picker

if __name__ == "__main__":
    register()
