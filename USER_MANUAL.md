# User Manual - Cloud Management System

## Start the Program
```bash
python main.py
```

---

## Docker Features

**1. List Docker Images** - Shows all images on your system
- Enter: 1

**2. Search Local Images** - Find images by name
- Enter: 2, then image name

**3. Search DockerHub** - Search online (no Docker needed)
- Enter: 3, then image name

**4. Pull Image** - Download image from online
- Enter: 4, then image name (e.g., "python:3.9")

**5. Create Dockerfile** - Write instructions for building an image
- Enter: 5
- Path: where to save (e.g., "Dockerfile")
- Mode: 1=Guided, 2=Paste, 3=Load from file

**6. Build Image** - Create image from Dockerfile
- Enter: 6
- Dockerfile path: (e.g., "Dockerfile")
- Image name: (e.g., "myapp:1.0")

**7. Run Image** - Create and start a container
- Enter: 7
- Image name: (e.g., "python:3.9")
- Container name: (e.g., "my-app")

**8. List Running Containers** - Show active containers only
- Enter: 8

**9. List All Containers** - Show all containers (running + stopped)
- Enter: 9

**10. Start Container** - Restart a stopped container
- Enter: 10
- Container ID or name: 

**11. Stop Container** - Stop a running container
- Enter: 11
- Container ID or name:

---

## Virtual Machine Features

**12. Create VM (Interactive)** - Create VM by answering questions
- Enter: 12
- VM name: 
- RAM (MB): (e.g., 2048)
- CPU count: (e.g., 2)
- Disk size (GB): (e.g., 20)

**13. Create VM from Config** - Create VM from JSON file
- Create `config.json`:
  ```json
  {"name": "vm1", "ram": "2048", "cpu": "2", "disk": "20G"}
  ```
- Enter: 13
- Config path: (e.g., "config.json")

**14. List VMs** - Show all virtual machines
- Enter: 14

**15. Delete VM** - Remove a VM (cannot undo!)
- Enter: 15
- VM name:
- Confirm: type "yes"

---

## Quick Examples

### Example 1: Pull and Run Ubuntu
```
Option 4 → ubuntu:22.04
Option 7 → ubuntu:22.04, container name: ubuntu-server
Option 8 → See running containers
```

### Example 2: Create a VM
```
Option 12 → vm-name: "server1", ram: 2048, cpu: 2, disk: 20
Option 14 → See your new VM
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker not found | Install Docker from docker.com |
| No such image | Use option 4 to pull it first |
| Container name exists | Use different name |
| Config file not found | Check file path exists |
| Invalid JSON | Check JSON syntax |

---

## Quick Reference

| # | Feature |
|----|---------|
| 1 | List images |
| 2 | Search local images |
| 3 | Search DockerHub |
| 4 | Pull image |
| 5 | Create Dockerfile |
| 6 | Build image |
| 7 | Run container |
| 8 | List running |
| 9 | List all containers |
| 10 | Start container |
| 11 | Stop container |
| 12 | Create VM |
| 13 | Create VM from config |
| 14 | List VMs |
| 15 | Delete VM |
| 0 | Exit |
| c | Clear screen |

---
