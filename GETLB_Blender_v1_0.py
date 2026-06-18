bl_info = {
    "name": "Timeline Sync (GETLB)",
    "author": "Team Gadget",
    "version": (1, 0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GECB Tab",
    "description": "Bidirectional timeline synchronization and offline baking for Cascadeur.",
    "category": "Animation",
}

import bpy
import socket
import struct

from bpy.app.handlers import persistent

# ==========================================
# Network Engine
# ==========================================
GETLB_HOST = '127.0.0.1'
GETLB_SEND_PORT = 8993  
GETLB_RECV_PORT = 8994  

CMD_SEEK = 0x03

getlb_send_socket = None
getlb_recv_socket = None

def init_network():
    global getlb_send_socket, getlb_recv_socket
    if getlb_send_socket is None:
        getlb_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if getlb_recv_socket is None:
        try:
            getlb_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            getlb_recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            getlb_recv_socket.bind((GETLB_HOST, GETLB_RECV_PORT))
            getlb_recv_socket.setblocking(False)
        except Exception as e:
            print(f"GETLB Receiver Bind Error: {e}")

def close_network():
    global getlb_send_socket, getlb_recv_socket
    if getlb_recv_socket:
        getlb_recv_socket.close()
        getlb_recv_socket = None
    if getlb_send_socket:
        getlb_send_socket.close()
        getlb_send_socket = None

# ★ @persistent をつけてファイルロード後も生き残らせる
@persistent
def getlb_frame_change_handler(scene):
    props = scene.getlb_props
    if props.sync_enable and props.sync_master == 'BLENDER' and not props.is_baking:
        current_frame = scene.frame_current
        try:
            packet = struct.pack('<4s B i', b'GTLB', CMD_SEEK, current_frame)
            getlb_send_socket.sendto(packet, (GETLB_HOST, GETLB_SEND_PORT))
        except Exception:
            pass

def getlb_receive_timer():
    # コンテキストがない場合はスキップ
    if getattr(bpy.context, 'scene', None) is None:
        return 0.016
        
    scene = bpy.context.scene
    props = scene.getlb_props
    
    if props.sync_enable and props.sync_master == 'CASCADEUR' and not props.is_baking:
        latest_frame = None
        while True:
            try:
                data, addr = getlb_recv_socket.recvfrom(1024)
                if len(data) >= 9:
                    header, cmd, frame = struct.unpack('<4s B i', data[:9])
                    if header == b'GTLB' and cmd == CMD_SEEK:
                        latest_frame = frame
            except BlockingIOError:
                break
            except Exception:
                break
                
        if latest_frame is not None and latest_frame != scene.frame_current:
            scene.frame_set(latest_frame)
            
    return 0.016

# ★ 新設：ファイルがロードされるたびにタイマーを蘇生するハンドラ
@persistent
def getlb_load_handler(dummy):
    if not bpy.app.timers.is_registered(getlb_receive_timer):
        bpy.app.timers.register(getlb_receive_timer)

# ==========================================
# Properties
# ==========================================
class GETLB_Properties(bpy.types.PropertyGroup):
    sync_master: bpy.props.EnumProperty(
        name="Master",
        items=[
            ('BLENDER', "Blender", "Blender controls the timeline"),
            ('CASCADEUR', "Cascadeur", "Cascadeur controls the timeline"),
        ],
        default='CASCADEUR'
    )
    
    sync_enable: bpy.props.BoolProperty(
        name="Enable Timeline Sync",
        default=False
    )
    
    bake_delay: bpy.props.FloatProperty(
        name="Bake Delay (s)",
        description="Wait time per frame to receive pose data",
        default=0.15,
        min=0.01,
        max=1.0,
        step=1
    )

    is_baking: bpy.props.BoolProperty(
        name="Is Baking",
        default=False
    )
    
    bake_start: bpy.props.IntProperty(
        name="Start",
        description="Start frame for baking",
        default=1,
        min=0
    )
    
    bake_end: bpy.props.IntProperty(
        name="End",
        description="End frame for baking",
        default=100,
        min=1
    )

# ==========================================
# Operators
# ==========================================
class GETLB_OT_bake_animation(bpy.types.Operator):
    bl_idname = "getlb.bake_animation"
    bl_label = "Bake from Cascadeur"
    bl_description = "Bake animation frame by frame (Press ESC to cancel)"
    
    _timer = None
    current_frame = 0
    end_frame = 0
    state = 'SEEK'

    def modal(self, context, event):
        if event.type == 'ESC':
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            scene = context.scene

            if self.state == 'SEEK':
                scene.frame_set(self.current_frame)
                try:
                    packet = struct.pack('<4s B i', b'GTLB', CMD_SEEK, self.current_frame)
                    getlb_send_socket.sendto(packet, (GETLB_HOST, GETLB_SEND_PORT))
                except Exception:
                    pass
                
                self.state = 'RECORD'

            elif self.state == 'RECORD':
                try:
                    context.view_layer.update()
                    obj = context.active_object
                    if obj and obj.type == 'ARMATURE' and obj.mode == 'POSE':
                        for pb in context.selected_pose_bones:
                            pb.keyframe_insert(data_path="location")
                            if pb.rotation_mode == 'QUATERNION':
                                pb.keyframe_insert(data_path="rotation_quaternion")
                            else:
                                pb.keyframe_insert(data_path="rotation_euler")
                except Exception as e:
                    print(f"GETLB Bake Error: {e}")

                if self.current_frame >= self.end_frame:
                    self.finish(context)
                    return {'FINISHED'}
                else:
                    self.current_frame += 1
                    self.state = 'SEEK'

        return {'PASS_THROUGH'}

    def execute(self, context):
        scene = context.scene
        props = scene.getlb_props
        
        if props.is_baking:
            self.report({'WARNING'}, "GETLB: Already baking!")
            return {'CANCELLED'}

        self.current_frame = props.bake_start
        self.end_frame = props.bake_end
        
        if self.current_frame > self.end_frame:
            self.report({'ERROR'}, "GETLB: Start frame must be less than or equal to End frame.")
            return {'CANCELLED'}

        self.state = 'SEEK'

        props.is_baking = True
        props.sync_master = 'BLENDER'
        props.sync_enable = True

        wm = context.window_manager
        delay = props.bake_delay
        self._timer = wm.event_timer_add(delay, window=context.window)
        wm.modal_handler_add(self)
        
        self.report({'INFO'}, f"GETLB: Bake Started! ({self.current_frame} to {self.end_frame})")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self._cleanup(context, "GETLB: Bake Cancelled.")

    def finish(self, context):
        self._cleanup(context, f"GETLB: Bake Completed! ({self.end_frame} frames)")
        
    def _cleanup(self, context, msg):
        wm = context.window_manager
        if self._timer:
            try:
                wm.event_timer_remove(self._timer)
            except:
                pass
            self._timer = None
            
        props = context.scene.getlb_props
        props.is_baking = False
        props.sync_enable = False
        props.sync_master = 'BLENDER'
        self.report({'INFO' if "Completed" in msg else 'WARNING'}, msg)

# ==========================================
# UI Panel
# ==========================================
class GETLB_PT_main_panel(bpy.types.Panel):
    bl_label = "Timeline Sync (GETLB)"
    bl_idname = "GETLB_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GECB'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.getlb_props
        
        row = layout.row()
        row.enabled = not props.is_baking
        row.prop(props, "sync_master", expand=True)
        
        row = layout.row()
        row.enabled = not props.is_baking
        sync_icon = 'PLAY' if props.sync_enable else 'PAUSE'
        row.prop(props, "sync_enable", text="Enable Timeline Sync", toggle=True, icon=sync_icon)
        
        bake_box = layout.box()
        bake_box.enabled = not props.is_baking
        
        row = bake_box.row(align=True)
        row.prop(props, "bake_start")
        row.prop(props, "bake_end")
        
        row = bake_box.row()
        row.prop(props, "bake_delay")
        
        row = bake_box.row()
        row.scale_y = 1.2
        if props.is_baking:
            row.enabled = False
            row.operator("getlb.bake_animation", text="Baking... (Press ESC to stop)", icon='TIME')
        else:
            row.operator("getlb.bake_animation", text="Bake from Cascadeur", icon='REC')

# ==========================================
# Registration
# ==========================================
classes = (
    GETLB_Properties,
    GETLB_OT_bake_animation,
    GETLB_PT_main_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.getlb_props = bpy.props.PointerProperty(type=GETLB_Properties)
    
    init_network()
    
    if getlb_frame_change_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(getlb_frame_change_handler)
        
    # ★ 蘇生ハンドラを登録
    if getlb_load_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(getlb_load_handler)
        
    if not bpy.app.timers.is_registered(getlb_receive_timer):
        bpy.app.timers.register(getlb_receive_timer)

def unregister():
    if getlb_frame_change_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(getlb_frame_change_handler)
        
    # ★ 蘇生ハンドラを解除
    if getlb_load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(getlb_load_handler)
        
    if bpy.app.timers.is_registered(getlb_receive_timer):
        bpy.app.timers.unregister(getlb_receive_timer)
        
    close_network()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.getlb_props

if __name__ == "__main__":
    register()