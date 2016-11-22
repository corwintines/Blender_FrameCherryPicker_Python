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
        frame_split = frame_string.split(',')
        for frame in frame_split:
            hyphen = False
            for char in frame:
                if char == '-':
                    hyphen = True
            if hyphen == True:
                temp = frame.split('-')
                for num in range(int(temp[0]), int(temp[1])+1):
                    frame_render.append(num)
            else:
                frame_render.append(frame)

    def execute(self, context):
        frame_string = bpy.data.scenes[0].render_frames_cherry_picker
        frames_render = []
        convert_string(frame_string, frames_render)
        sort_frames(frames_render)
        render_frames(frames_render)
        return{'FINISHED'}

    def render_frames(frames_render):
        filepath = bpy.data.scenes[0].render.filepath
        for frame in frames_render:
            bpy.data.scenes[0].frame_current = frame
            renderpath = filepath + str(bpy.data.scenes[0].frame_current)
            bpy.data.scenes[0].render.filepath = renderpath
            bpy.ops.render.render(write_still = True)
            print(bpy.data.scenes[0].frame_current)
        bpy.data.scenes[0].render.filepath = filepath

    def sort_frames(frames_render):
        # Using merge sort algorithm
        if len(frames_render)>1:
            mid = len(frames_render)/2
            left = frames_render[:mid]
            right = frames_render[mid:]

            sort_frames(left)
            soft_frame(right)

            i=0
            j=0
            k=0

            while i<len(left) and j<len(right):
                if left[i] < right[j]:
                    frames_render[k] = left[i]
                    i +=1
                else:
                    frames_render[k] = right[j]
                    j += 1
                k += 1

            while i<len(left):
                frames_render[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                frames_render[k] = right[j]
                j += 1
                k += 1

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
