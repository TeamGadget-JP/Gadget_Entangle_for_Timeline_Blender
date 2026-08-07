import csc
import socket
import sys
import ctypes
import struct

def command_name():
    return "GECB TimeLine Sync(v1_0)"

def command_description():
    return "Bidirectional timeline sync with Blender (GETLB)."

def run(scene):
    HWND = ctypes.c_void_p
    UINT = ctypes.c_uint
    UINT_PTR = ctypes.c_uint64 if sys.maxsize > 2**32 else ctypes.c_uint
    DWORD = ctypes.c_ulong
    TIMERPROC = ctypes.WINFUNCTYPE(None, HWND, UINT, UINT_PTR, DWORD)

    user32 = ctypes.windll.user32
    user32.SetTimer.argtypes = [HWND, UINT_PTR, UINT, TIMERPROC]
    user32.SetTimer.restype = UINT_PTR
    user32.KillTimer.argtypes = [HWND, UINT_PTR]
    user32.KillTimer.restype = ctypes.c_bool

    GETLB_RECV_PORT = 8993
    GETLB_SEND_PORT = 8994
    GETLB_HOST = "127.0.0.1"
    CMD_SEEK = 0x03

    if not hasattr(sys, 'getlb_sock'):
        sys.getlb_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sys.getlb_sock.bind((GETLB_HOST, GETLB_RECV_PORT))
        sys.getlb_sock.setblocking(False) 
        sys.getlb_last_frame = -1

    def sync_callback(hwnd, msg, timer_id, current_time):
        try:
            app = csc.app.get_application()
            curr_scene = app.current_scene()
            if not curr_scene: return
            domain = curr_scene.domain_scene()
            
            # 1. Receive from Blender
            latest_recv_frame = None
            while True:
                try:
                    data, addr = sys.getlb_sock.recvfrom(1024)
                    if len(data) >= 9:
                        header, cmd, frame = struct.unpack('<4s B i', data[:9])
                        if header == b'GTLB' and cmd == CMD_SEEK:
                            latest_recv_frame = frame
                except BlockingIOError:
                    break 
                except Exception:
                    break
            
            if latest_recv_frame is not None:
                domain.set_current_frame(latest_recv_frame)
                sys.getlb_last_frame = latest_recv_frame
                return

            # 2. Send to Blender
            try:
                cas_current_frame = domain.get_current_frame() 
                
                if cas_current_frame != sys.getlb_last_frame:
                    packet = struct.pack('<4s B i', b'GTLB', CMD_SEEK, cas_current_frame)
                    sys.getlb_sock.sendto(packet, (GETLB_HOST, GETLB_SEND_PORT))
                    sys.getlb_last_frame = cas_current_frame
                    
            except Exception as e:
                if not getattr(sys, 'getlb_err_printed', False):
                    print(f"GETLB API Error: {e}")
                    sys.getlb_err_printed = True

        except Exception:
            pass

    sys.getlb_timer_func = TIMERPROC(sync_callback)

    if getattr(sys, 'getlb_timer_id', None) is not None:
        user32.KillTimer(None, sys.getlb_timer_id)
        sys.getlb_timer_id = None
        if hasattr(sys, 'getlb_sock'): 
            sys.getlb_sock.close()
            del sys.getlb_sock
        
        scene.error("[GETLB] Stopped bidirectional sync.")
    else:
        sys.getlb_err_printed = False 
        timer_id = user32.SetTimer(None, 0, 16, sys.getlb_timer_func)
        if timer_id:
            sys.getlb_timer_id = timer_id
            scene.success(f"[GETLB] Running! (Recv:{GETLB_RECV_PORT} / Send:{GETLB_SEND_PORT})")