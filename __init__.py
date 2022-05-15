# Copyright 2021 by Hextant Studios. https://HextantStudios.com
# This work is licensed under GNU General Public License Version 3.
# License: https://download.blender.org/release/GPL3-license.txt

# Inspired by: https://github.com/AlansCodeLog/blender-debugger-for-vscode

# Notes: 
# * As of 5/3/2022 debugpy provides no methods to stop the server or check if one is
#   still listening.

bl_info = {
    "name": "Python Debugger",
    "author": "Hextant Studios",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "Click 'Install debugpy' below. Main Menu / Blender Icon / System / Start Python Debugger",
    "description": "Starts debugpy and listens for connections from a remote debugger such " \
        "as Visual Studio Code or Visual Studio 2019 v16.6+.",
    "doc_url": "https://github.com/hextantstudios/hextant_python_debugger",
    "category": "Development",
}

import bpy, sys, os, site, subprocess, importlib
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty

# The global debugpy module (imported when the server is started).
debugpy = None

# Returns true if debugpy has been installed.
def is_debugpy_installed() -> bool:
    try:
        # Blender does not add the user's site-packages/ directory by default.
        sys.path.append(site.getusersitepackages())
        return importlib.util.find_spec('debugpy') is not None
    finally:
        sys.path.remove(site.getusersitepackages())

#
# Addon Preferences
#

# Preferences to select the addon package name, etc.
class DebugPythonPreferences(AddonPreferences):
    bl_idname = __package__

    port: IntProperty(name="Server Port", default=5678, min=1024, max=65535,
        description="The port number the debug server will listen on. This must match the " +
        "port number configured in the debugger application.")

    def draw(self, context):
        installed = is_debugpy_installed()
        layout = self.layout
        layout.use_property_split = True
        
        if installed: 
            layout.prop(self, 'port')
            layout.operator(UninstallDebugpy.bl_idname)
        else:
            layout.operator(InstallDebugpy.bl_idname)            
        

#
# Operators
#

# Installs debugpy package into Blender's Python distribution.
class InstallDebugpy(Operator):
    """Installs debugpy package into Blender's Python distribution."""
    bl_idname = "script.install_debugpy"
    bl_label = "Install debugpy"

    def execute(self, context):
        python = os.path.abspath(sys.executable)
        self.report({'INFO'}, "Installing 'debugpy' package.")
        # Verify 'pip' package manager is installed.
        try:
            context.window.cursor_set('WAIT')
            subprocess.call([python, "-m", "ensurepip"])
            # Upgrade 'pip'. This shouldn't be needed.
            # subprocess.call([python, "-m", "pip", "install", "--upgrade", "pip", "--yes"])
        except Exception:
            self.report({'ERROR'}, "Failed to verify 'pip' package manager installation.")
            return {'FINISHED'}
        finally:
            context.window.cursor_set('DEFAULT')
        
        # Install 'debugpy' package.
        try:
            context.window.cursor_set('WAIT')
            subprocess.call([python, "-m", "pip", "install", "debugpy"])
        except Exception:
            self.report({'ERROR'}, "Failed to install 'debugpy' package.")
            return {'FINISHED'}
        finally:
            context.window.cursor_set('DEFAULT')
        
        self.report({'INFO'}, "Successfully installed 'debugpy' package.")
        return {'FINISHED'}


# Uninstalls debugpy package into Blender's Python distribution.
class UninstallDebugpy(Operator):
    """Uninstalls debugpy package from Blender's Python distribution."""
    bl_idname = "script.uninstall_debugpy"
    bl_label = "Uninstall debugpy"

    def execute(self, context):
        python = os.path.abspath(sys.executable)
        self.report({'INFO'}, "Uninstalling 'debugpy' package.")
        
        # Uninstall 'debugpy' package.
        try:
            context.window.cursor_set('WAIT')
            subprocess.call([python, "-m", "pip", "uninstall", "debugpy", "--yes"])
        except Exception:
            self.report({'ERROR'}, "Failed to uninstall 'debugpy' package.")
            return {'FINISHED'}
        finally:
            context.window.cursor_set('DEFAULT')
        
        self.report({'INFO'}, "Successfully uninstalled 'debugpy' package.")
        return {'FINISHED'}


# Starts the debug server for Python scripts.
class StartDebugServer(Operator):
    """Starts the remote debug server (debugpy) for Python scripts.
    Note: debugpy must be installed from the add-on's preferences."""
    bl_idname = "script.start_debug_server"
    bl_label = "Start Debug Server"

    @classmethod
    def poll(cls, context):
        return is_debugpy_installed()

    def execute(self, context):
        addon_prefs = context.preferences.addons[__package__].preferences

        # Import the debugpy package.
        global debugpy
        if not debugpy:
            try:
                sys.path.append(site.getusersitepackages())
                debugpy = importlib.import_module('debugpy')
            except:
                self.report({'ERROR'}, "Failed to import debugpy! " + 
                    "Verify that debugpy has been installed from the add-on's preferences.")
                return {'FINISHED'}
            finally:
                sys.path.remove(site.getusersitepackages())

        # Start debugpy listening. Note: Always try as there is no way to query if debugpy
        # is already listening.
        # Get the desired port to listen on.
        port = addon_prefs.port

        try:
            debugpy.listen(port)
        except:
            self.report({'WARNING'}, 
                f"Remote python debugger failed to start (or already started) on port {port}.")
            return {'FINISHED'}

        self.report({'INFO'}, f"Remote python debugger started on port {port}.")
        return {'FINISHED'}


#
# Menu Items
#

# Draw the main menu entry for: {Blender}/System/Start Remote Debugger
def start_remote_debugger_menu(self, context):
    self.layout.operator(StartDebugServer.bl_idname, icon='SCRIPT')

#
# Registration
#

_classes = (DebugPythonPreferences, InstallDebugpy, UninstallDebugpy, StartDebugServer)
_register, _unregister = bpy.utils.register_classes_factory(_classes)

def register():
    _register()
    # Add a System menu entry to start the server.
    bpy.types.TOPBAR_MT_blender_system.prepend(start_remote_debugger_menu)

def unregister():
    _unregister()
    # Remove System menu entry
    bpy.types.TOPBAR_MT_blender_system.remove(start_remote_debugger_menu)

