import subprocess
import os
import json

def create_vm():
    print("\n=== Create Virtual Machine (QEMU) ===")

    name = input("Enter VM name: ").strip()
    ram  = input("Enter RAM size in MB (e.g. 1024): ").strip()
    cpu  = input("Enter number of CPUs (e.g. 1): ").strip()
    disk = input("Enter disk size (e.g. 5G): ").strip()

    if not all([name, ram, cpu, disk]):
        print("All fields are required.")
        return

    disk_file = f"{name}.qcow2"

    if os.path.exists(disk_file):
        print("Disk file already exists.")
        return

    print("[+] Creating disk image...")
    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        disk_file, disk
    ])

    print("[+] Starting virtual machine...")
    subprocess.run([
        "qemu-system-x86_64",
        "-m", ram,
        "-smp", cpu,
        "-hda", disk_file
    ])
def delete_vm():
    print("\n=== Delete Virtual Machine (QEMU) ===")

    name = input("Enter VM name to delete: ").strip()
    if not name:
        print("VM name cannot be empty.")
        return

    disk_file = f"{name}.qcow2"

    if not os.path.exists(disk_file):
        print(f"VM disk '{disk_file}' not found.")
        return

    confirm = input(f"Are you sure you want to delete '{disk_file}'? (y/n): ").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return

    os.remove(disk_file)
    print(f"VM '{name}' deleted successfully.")

def list_vms():
    vms = [f for f in os.listdir() if f.endswith(".qcow2")]

    if not vms:
        print("No virtual machines found.")
        return

    print("Available Virtual Machines:")
    for vm in vms:
        print("-", vm.replace(".qcow2", ""))


def create_vm_from_config():
    print("\n=== Create Virtual Machine from JSON config (QEMU) ===")
    path = input("Enter JSON config file path: ").strip()
    if not path or not os.path.exists(path):
        print("Config file not found.")
        return

    try:
        with open(path, "r") as f:
            cfg = json.load(f)
    except Exception as e:
        print("Failed to read config:", e)
        return

    name = str(cfg.get("name", "")).strip()
    ram = str(cfg.get("ram", "")).strip()
    cpu = str(cfg.get("cpu", "")).strip()
    disk = str(cfg.get("disk", "")).strip()

    if not all([name, ram, cpu, disk]):
        print("Config missing required fields: name, ram, cpu, disk")
        return

    disk_file = f"{name}.qcow2"

    if os.path.exists(disk_file):
        print("Disk file already exists.")
        return

    print("[+] Creating disk image...")
    subprocess.run([
        "qemu-img", "create",
        "-f", "qcow2",
        disk_file, disk
    ])

    print("[+] Starting virtual machine...")
    subprocess.run([
        "qemu-system-x86_64",
        "-m", ram,
        "-smp", cpu,
        "-hda", disk_file
    ])