## ⚙️ Implementation Details

### Recent Updates

- Docker module docstrings were converted to `#` comments for consistent comment style.
- Test method names were updated to camelCase (keeping the `test` prefix for `unittest` discovery).

This section explains how Docker and Virtual Machine operations are implemented internally.

---

## 🐳 Docker Implementation

Docker functionality is implemented using Python’s `subprocess` module to interact directly with the **Docker CLI**.  
The system acts as a **CLI orchestrator**, while Docker performs the actual containerization.

### Docker Engine Check
Before executing most Docker commands, the system verifies that the Docker daemon is running:

- Uses `docker info`
- Prevents crashes if Docker is not installed or not started
- Displays a clear error message instead of failing silently


### Supported Docker Operations

- **List Images**
  - Executes `docker images`
- **List Running Containers**
  - Executes `docker ps`
- **List All Containers**
  - Executes `docker ps -a`
- **Run Image**
  - Executes `docker run -d`
  - Supports optional container naming
  - Relies on Docker’s default behavior to pull the image if it does not exist locally
- **Stop Container**
  - Executes `docker stop`
  - Validates container existence before stopping
- **Start Container**
  - Executes `docker start`
  - Confirms container ID or name exists
- **Search Docker Hub**
  - Executes `docker search`
  - Does not require the Docker daemon to be running
- **Pull Image**
  - Executes `docker pull`
  - Displays Docker output or error messages
- **Search Local Images**
  - Filters results from `docker images`
- **Create Dockerfile**
  - Supports three modes:
    1. Guided prompts
    2. Manual multi-line input
    3. Load from existing file
- **Build Image**
  - Executes `docker build`
  - Allows custom Dockerfile paths and image tags

### Design Notes
- All Docker calls are wrapped with error handling
- User inputs are validated before execution
- No force operations are used to ensure safety

---

## 🖥️ Virtual Machine (QEMU) Implementation

Virtual machine functionality is implemented using **QEMU** through system commands executed from Python.

### VM Creation Flow

1. User provides:
   - VM name
   - RAM size
   - CPU count
   - Disk size
2. A virtual disk image is created using:
   ```bash
   qemu-img create -f qcow2 <name>.qcow2 <size>
   ```
3. The VM is started using:
   ```bash
   qemu-system-x86_64 -m <ram> -smp <cpu> -hda <name>.qcow2
   ```

### Additional VM Operations

- **List VMs**
  - Lists local `*.qcow2` files in the current working directory
- **Delete VM**
  - Deletes `<name>.qcow2` after confirmation
- **Create VM from JSON Config**
  - Reads `name`, `ram`, `cpu`, `disk` from a JSON file (example: `configs/vm_config.json`)
