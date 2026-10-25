#region Initialization
import json
import os
from types import SimpleNamespace
from vbox_utils import run_vbox
import shutil


# Define `VBoxManage` as VBOX for use in Python.
VBOX = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

with open('config.jsonc', 'r') as file:
        config = json.load(
            file,
            object_hook=lambda d: SimpleNamespace(**d),
        )

#region Functions
def destroy_vm(name, basefolder):

    VDI_PATH = "vdi"

    # if os.path.exists(VDI_PATH):
    #     shutil.rmtree(VDI_PATH)

    # Check VM state
    try:
        result = run_vbox("showvminfo", name, "--machinereadable")
    except: 
        print(f"VM '{name}' is not registered.")
        return
    
    if 'State="running"' in result.stdout:
        run_vbox("controlvm", name, "acpipowerbutton")
    else:
        print(f"{name} is not running; skipping shutdown.")


    # Unregister and delete files owned by the VM
    result = run_vbox("unregistervm", name, "--delete")

    if result.returncode == 0:
        print(f"Destroyed VM: {name}")

    medium_path =  rf"vdi\{basefolder}\{name}.vdi"
    result = run_vbox("closemedium", "disk", medium_path, "--delete")



for node in config.nodes:  
    destroy_vm(node.name, node.basefolder)