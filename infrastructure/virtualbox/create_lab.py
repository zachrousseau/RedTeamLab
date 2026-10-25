#region Initialization
import json
from types import SimpleNamespace
from vbox_utils import run_vbox


# Define `VBoxManage` as VBOX for use in Python.
VBOX = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

with open('config.jsonc', 'r') as file:
        config = json.load(
            file,
            object_hook=lambda d: SimpleNamespace(**d),
        )

#region Functions

# Function to create virtual machines
def create_vm(name, ostype, basefolder, image):
    run_vbox(  
        "createvm",
        "--name", name,
        "--ostype", ostype,
        "--basefolder", basefolder,
        "--register"
    )

    disk_path = rf"vdi\{basefolder}\{name}.vdi"

    run_vbox(
        "createmedium", "disk",
        "--filename", disk_path,
        "--size", "20480",
        "--format", "VDI",
    )

    run_vbox(
        "storagectl",
        name,
        "--name", "SATA Controller",
        "--add", "sata",
        "--controller", "IntelAhci"
    )

    run_vbox(
        "storageattach",
        name,
        "--storagectl", "SATA Controller",
        "--port", "1",
        "--device", "0",
        "--type", "dvddrive",
        "--medium", image,
    )

    run_vbox(
        "modifyvm", name,
        "--memory", "2048",
        "--cpus", "2",
        "--vram", "16",
        "--boot1", "dvd",
        "--boot2", "disk",
        "--boot3", "none",
        "--boot4", "none",
        "--nic1", "nat",
    )

    run_vbox(
        "startvm", name, "--type", "gui"
    )






#region Execution
# Creates nodes defined in config.jsonc
for node in config.nodes:
    create_vm(node.name, node.ostype, node.basefolder, node.image)
