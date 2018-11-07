bl_info = {
  "name" : "The Cherry Picker",
  "category": "3D View",
  "author": "Corwin Smith"
}

import bpy
import os

class CherryPickerInterface(bpy.types.Panel):
    bl_label = "Frame Cherry Picker"
    bl_id = "view3D.custom_menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        split = layout.split()

        # Layout for entering frames that need to be rendered
        row = layout.row()
        row.prop(context.scene, "render_frames_cherry_picker", text="Input Frames")
        row = layout.row()
        row.label("Enter file name (will use default if not specified):")
        rd = context.scene.render
        image_settings = rd.image_settings
        file_format = image_settings.file_format
        layout.prop(rd, "filepath", text="")
        row = layout.row()
        row.prop(context.scene, "render_frames_cherry_picker_render_consecutive_number", text="Frame name consecutive")
        row = layout.row()
        row.operator("frame.cherrypicker")


class CherryPickerSubmit(bpy.types.Operator):
    bl_idname = "frame.cherrypicker"
    bl_label = "Submit"

    def execute(self, context):
        frame_string = bpy.data.scenes[0].render_frames_cherry_picker
        frame_naming_type = bpy.data.scenes[0].render_frames_cherry_picker_render_consecutive_number
        frames_render = convert_string(frame_string)
        render_frames(frames_render, frame_naming_type)
        return{'FINISHED'}


def convert_string(frame_string):
    frames_render = []
    frame_split = frame_string.split(',')
    for frame in frame_split:
        hyphen = False
        for char in frame:
            if char == '-':
                hyphen = True
        if hyphen == True:
            temp = frame.split('-')
            for num in range(int(temp[0]), int(temp[1])+1):
                frames_render.append(int(num))
        else:
            frames_render.append(int(frame))

    return sorted(frames_render)


def render_frames(frames_render, frame_naming_consecutive):
    filepath = bpy.data.scenes["Scene"].render.filepath
    file_extension = bpy.data.scenes["Scene"].render.file_extension

    filedirectory, filename = parse_filepath(filepath)
    for frame in range(0, len(frames_render)):
        if frame_naming_consecutive is True:
            bpy.data.scenes["Scene"].render.filepath = os.path.join(filedirectory, filename+'_'+str(frame).zfill(4))
        else:
            bpy.data.scenes["Scene"].render.filepath = os.path.join(filedirectory, filename+'_'+str(frames_render[frame]).zfill(4))
        bpy.data.scenes[0].frame_current = frames_render[frame]
        bpy.ops.render.render(write_still=True)
    
    bpy.data.scenes["Scene"].render.filepath = filepath

def parse_filepath(filepath):
    filename = 'render'
    path, file = os.path.split(filepath)
    if (file is not ''):
        return path, file
    return path, filename


def register():
    bpy.utils.register_class(CherryPickerInterface)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.render_frames_cherry_picker = bpy.props.StringProperty (description = "Frames to be rendered", default = "")
    bpy.types.Scene.render_frames_cherry_picker_render_consecutive_number = bpy.props.BoolProperty(name="", description="Option to name files 0-render_frame_length to allow for easier use in compositing software")


def unregister():
    bpy.utils.unregister_class(CherryPickerInterface)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.render_frames_cherry_picker
    del bpy.types.Scene.render_frames_cherry_picker_render_consecutive_number 


if __name__ == "__main__":
    register()
