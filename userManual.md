# Cloud Management System — User Manual

## 1. Overview
This project is a menu-driven command-line interface (CLI) that provides a unified way to manage:

- Docker images and containers (via the Docker CLI)
- QEMU virtual machines (via `qemu-img` and `qemu-system-x86_64`)

The system is intended for learning and basic management tasks. It does not provide a graphical UI or a web interface.

## 2. Requirements

### 2.1 Software
- Python 3
- Docker Desktop / Docker Engine (must be running)
- QEMU (must be installed and available on `PATH`)

### 2.2 Operating system notes
- The menu “Clear Screen” option uses `cls` (Windows).
- QEMU VM disk files are stored as `*.qcow2` in the folder where you run the program.

## 3. Installation and Setup

### 3.1 Get the project
- Download or clone the repository.
- Open a terminal in the project folder (where `main.py` is located).

### 3.2 Verify Python
Run:

```bash
python --version
```

### 3.3 Verify Docker
1. Install Docker Desktop.
2. Start Docker Desktop and wait until it reports it is running.
3. Verify:

```bash
docker --version
docker info
```

If `docker info` fails, Docker is not running or not installed correctly.

### 3.4 Verify QEMU
1. Install QEMU.
2. Ensure the QEMU install folder is added to the Windows `PATH`.
3. Open a NEW terminal window (important after changing PATH) and verify:

```bat
where qemu-img
where qemu-system-x86_64
qemu-img --version
qemu-system-x86_64 --version
```

If `where qemu-img` returns no output, the PATH is not applied to that terminal session.

## 4. Running the System
From the project directory:

```bash
python main.py
```

You will see a menu of options. Enter the number (or letter) for the feature you want.

## 5. Feature Guide (Menu Options)

### c) Clear Screen
- **Purpose**: Clears the terminal screen.
- **How it works**: Executes `cls`.
- **Guideline**: Windows terminals only.

### 1) List Docker Images
- **Purpose**: Shows Docker images available locally.
- **Command executed**: `docker images`
- **Guidelines**:
  - Docker Engine must be running.
  - Useful to confirm image names before running containers.

### 2) List Running Containers
- **Purpose**: Displays only currently running containers.
- **Command executed**: `docker ps`
- **Guidelines**:
  - Use this to find the container name/ID before stopping it.

### 3) List All Containers (running + stopped)
- **Purpose**: Displays all containers including stopped ones.
- **Command executed**: `docker ps -a`
- **Guidelines**:
  - Helpful if a container exists but is not running.

### 4) Stop Container
- **Purpose**: Stops a running Docker container.
- **Commands executed**:
  - First lists running containers (`docker ps`)
  - Then stops the container (`docker stop <container>`)
- **Input required**:
  - Container ID or container name
- **Guidelines**:
  - Choose a container listed in the “running containers” output.

### 5) Search Image on DockerHub
- **Purpose**: Searches DockerHub for images.
- **Command executed**: `docker search <name>`
- **Input required**:
  - Search keyword (image name)
- **Guidelines**:
  - Use the “NAME” column in results when pulling.

### 6) Pull Docker Image
- **Purpose**: Downloads an image from DockerHub.
- **Command executed**: `docker pull <image>`
- **Input required**:
  - Image name (example: `ubuntu`, `nginx`, `python:3.12-slim`)
- **Guidelines**:
  - Pulling may take time depending on network speed.

### 7) Run Docker Image (create container)
- **Purpose**: Runs an image to create a container in detached mode.
- **Command executed**: `docker run -d [--name <name>] <image>`
- **Inputs**:
  - Image name (required)
  - Container name (optional)
- **Guidelines**:
  - If you do not specify a name, Docker will generate one.
  - Some images require ports/volumes/environment variables; this CLI uses only a basic `docker run -d`.

### 8) Create Dockerfile
- **Purpose**: Creates a simple Dockerfile template.
- **What it does**:
  - Asks for a save path (default: `./Dockerfile`)
  - Asks for a base image (default: `python:3.12-slim`)
  - Asks for a start command (default: `python app.py`)
- **Guidelines**:
  - If you choose a path that already exists, you will be asked to confirm overwrite.
  - Ensure your project folder contains the files you want to copy into the image.

### 9) Build Docker Image
- **Purpose**: Builds a Docker image from a Dockerfile.
- **Command executed**:
  - `docker build -t <image:tag> -f <Dockerfile> .`
- **Inputs**:
  - Dockerfile path (default: `Dockerfile`)
  - Image name and tag (example: `myapp:1.0`)
- **Guidelines**:
  - Run this in the directory containing your Dockerfile and application files.

### 10) Create Virtual Machine (QEMU)
- **Purpose**: Creates a VM disk file and starts a QEMU VM.
- **Commands executed**:
  - `qemu-img create -f qcow2 <name>.qcow2 <disk>`
  - `qemu-system-x86_64 -m <ram> -smp <cpu> -hda <name>.qcow2`
- **Inputs**:
  - VM name (used as the QCOW2 disk filename)
  - RAM in MB (example: `1024`)
  - CPU count (example: `1` or `2`)
  - Disk size (example: `5G`, `10G`)
- **Guidelines for correct usage**:
  - **Disk size should include a unit**, such as `G` (example: `5G`).
  - If QEMU is not found, you will see a “file not found” error. Verify QEMU is on PATH in the same terminal session.
  - This VM launch uses only a blank disk by default. To install an OS, you will typically need a bootable ISO (not currently requested by the program).

### 11) Delete Virtual Machine (QEMU)
- **Purpose**: Deletes a VM disk image file (`<name>.qcow2`).
- **What it does**:
  - Asks for the VM name
  - Confirms deletion
  - Removes the disk file from the current directory
- **Guidelines**:
  - This permanently deletes the VM disk file.
  - Make sure you are in the correct folder when running the program.

### 12) List Virtual Machines (QEMU)
- **Purpose**: Lists VM disk images (`*.qcow2`) in the current directory.
- **What it does**:
  - Scans the current folder for `*.qcow2` files
  - Prints them as available VMs
- **Guidelines**:
  - The list depends on the folder you run the program from.

### 0) Exit
- **Purpose**: Exits the program.

## 6. Common Problems and Solutions

### 6.1 “Docker Engine is not running. Please start Docker.”
- Start Docker Desktop.
- Re-run the Docker option.
- Verify with `docker info`.

### 6.2 QEMU “FileNotFoundError: [WinError 2] The system cannot find the file specified”
- Verify QEMU is installed and on PATH:
  - In CMD: `where qemu-img`
  - In PowerShell: `where.exe qemu-img` or `Get-Command qemu-img`
- Restart the IDE/terminal after changing PATH.
- Ensure you added the folder that contains `qemu-img.exe` and `qemu-system-x86_64.exe`.

### 6.3 No virtual machines appear in “List VMs”
- You may not have any `*.qcow2` files in the current folder.
- Run the program in the same directory where your VM disk files are stored.

## 7. Safety and Best Practices
- Use trusted Docker images.
- Be careful when deleting VMs; deletion removes the disk file permanently.
- Keep VM disk files organized in a dedicated folder (optional) so listing/deletion are predictable.
