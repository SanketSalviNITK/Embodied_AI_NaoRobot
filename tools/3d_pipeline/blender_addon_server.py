# -*- coding: utf-8 -*-
"""
Blender Add-on Server (blender_addon_server.py)
-----------------------------------------------
This script runs a background TCP server inside Blender on port 9876.
It listens for Python code, queues it, executes it on Blender's main thread
using a timer (preventing crashes), and returns stdout/stderr as a JSON string.
"""

import socket
import threading
import queue
import sys
import json
import io
import traceback

# If running inside Blender, we can import bpy
try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False

PORT = 9876
HOST = '127.0.0.1'

# Global state to manage server threads and timers
server_thread = None
server_socket = None
is_running = False
execution_queue = queue.Queue()

def execute_code_on_main_thread(code_str):
    """Executes a block of python code and returns its stdout/stderr and status."""
    # Redirect stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer
    
    success = True
    error_message = ""
    
    try:
        # We compile the code and execute it in Blender's context
        # Use a unified namespace dictionary for both globals and locals
        # to ensure functions can reference each other perfectly.
        context = globals().copy()
        context.update({
            'bpy': sys.modules.get('bpy'),
            'math': sys.modules.get('math'),
            'time': sys.modules.get('time'),
        })
        
        # Execute the code snippet
        compiled = compile(code_str, '<string>', 'exec')
        exec(compiled, context, context)
    except Exception as e:
        success = False
        error_message = traceback.format_exc()
        print(error_message, file=sys.stderr)
    finally:
        # Restore standard streams
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
    return {
        "success": success,
        "stdout": stdout_buffer.getvalue(),
        "stderr": stderr_buffer.getvalue(),
    }

def blender_timer_callback():
    """Timer callback registered in Blender's main thread to poll for execution tasks."""
    global is_running
    if not is_running:
        return None  # Unregister timer
        
    while not execution_queue.empty():
        try:
            task = execution_queue.get_nowait()
            code_str = task['code']
            client_conn = task['conn']
            
            # Execute on main thread
            result = execute_code_on_main_thread(code_str)
            
            # Send result back as JSON
            response = json.dumps(result)
            client_conn.sendall(response.encode('utf-8'))
            client_conn.close()
        except queue.Empty:
            break
        except Exception as e:
            print("[Blender Addon Server] Error in timer execution: " + str(e))
            
    return 0.05  # Check again in 50ms

def client_handler(conn, addr):
    """Handles an incoming client TCP connection."""
    try:
        conn.settimeout(5.0)
        data_buffer = []
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data_buffer.append(chunk.decode('utf-8'))
            
        full_data = "".join(data_buffer)
        if not full_data.strip():
            conn.close()
            return
            
        # Queue the code to be run in Blender's main thread
        execution_queue.put({
            'code': full_data,
            'conn': conn
        })
    except Exception as e:
        print("[Blender Addon Server] Connection error from {}: {}".format(addr, e))
        try:
            conn.close()
        except:
            pass

def server_listen_loop():
    """Main TCP listener loop running in a background thread."""
    global server_socket, is_running
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("[Blender Addon Server] Active and listening on {}:{}".format(HOST, PORT))
        
        while is_running:
            try:
                conn, addr = server_socket.accept()
                t = threading.Thread(target=client_handler, args=(conn, addr))
                t.daemon = True
                t.start()
            except socket.error:
                break  # Socket closed
    except Exception as e:
        print("[Blender Addon Server] Thread critical error: " + str(e))
    finally:
        is_running = False
        print("[Blender Addon Server] Server thread terminated.")

def start_server():
    """Initializes and runs the server inside Blender."""
    global server_thread, is_running
    
    if is_running:
        print("[Blender Addon Server] Already running!")
        return True
        
    is_running = True
    server_thread = threading.Thread(target=server_listen_loop)
    server_thread.daemon = True
    server_thread.start()
    
    # Register timer inside Blender if running inside Blender
    if IN_BLENDER:
        if not bpy.app.timers.is_registered(blender_timer_callback):
            bpy.app.timers.register(blender_timer_callback)
            print("[Blender Addon Server] Main-thread timer registered in Blender.")
    else:
        print("[Blender Addon Server] WARNING: Not inside Blender environment. Timer NOT registered.")
        
    return True

def stop_server():
    """Stops the server and cleans up resources."""
    global is_running, server_socket, server_thread
    
    print("[Blender Addon Server] Stopping server...")
    is_running = False
    
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
        server_socket = None
        
    if server_thread:
        server_thread.join(timeout=1.0)
        server_thread = None
        
    if IN_BLENDER:
        try:
            if bpy.app.timers.is_registered(blender_timer_callback):
                bpy.app.timers.unregister(blender_timer_callback)
                print("[Blender Addon Server] Timer unregistered.")
        except Exception as e:
            print("[Blender Addon Server] Error unregistering timer: " + str(e))
            
    print("[Blender Addon Server] Server stopped successfully.")

if __name__ == "__main__":
    # If run as script in Blender, immediately start the server
    # First stop any existing to support live-reloading
    stop_server()
    start_server()
