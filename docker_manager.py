import subprocess
import os
import shlex

ERROR_MSG = "Docker Engine is not running. Please start Docker."

def check_docker_running():
    """Return True if Docker daemon is reachable on this host."""
    try:
        subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
    
def list_images():
    """List available Docker images (prints output)."""
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "images"]) 


def list_running_containers():
    """List running Docker containers (prints output)."""
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "ps"]) 

def list_all_containers():
    """List all Docker containers (running and stopped)."""
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "ps","-a"]) 

def run_image():
    """Run an image in detached mode; prompts for image and optional container name."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    image = input("Enter image name: ").strip()
    if not image:
        print("Image name cannot be empty.")
        return

    name = input("Enter container name (optional): ").strip()

    cmd = ["docker", "run", "-d"]
    if name:
        cmd += ["--name", name]

    cmd.append(image)
    try:
        result = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Failed to run image:")
            print(result.stderr.strip())
    except FileNotFoundError:
        print("Docker CLI not found. Please install Docker.")
def stop_container():
    """Stop a running container given its ID or name."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    list_running_containers()
    cid = input("Enter container ID or name to stop: ").strip()
    try:
        result = subprocess.run(["docker", "stop", cid], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Failed to stop container:")
            print(result.stderr.strip())
    except FileNotFoundError:
        print("Docker CLI not found. Please install Docker.")


def search_dockerhub():
    """Search Docker Hub for images (prints search results)."""
    # `docker search` doesn't require the daemon to be running, so skip the daemon check.
    name = input("Enter image name to search on DockerHub: ").strip()
    if not name:
        print("Image name cannot be empty.")
        return
    subprocess.run(["docker", "search", name])



def pull_image():
    """Pull an image from Docker Hub by name:tag."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    name = input("Enter image name to pull: ").strip()
    try:
        result = subprocess.run(["docker", "pull", name], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Failed to pull image:")
            print(result.stderr)
    except FileNotFoundError:
        print("Docker CLI not found. Please install Docker.")



def create_dockerfile():
    """Create a Dockerfile using guided prompts, pasted content, or loading from a file."""
    path = input("Enter path to save Dockerfile (default: ./Dockerfile): ").strip()
    if not path:
        path = "Dockerfile"

    if os.path.exists(path):
        confirm = input("Dockerfile already exists. Overwrite? (y/n): ").lower()
        if confirm != "y":
            print("Operation cancelled.")
            return

    print("Choose Dockerfile input mode:")
    print("1. Guided prompts (base image + start command)")
    print("2. Paste full multi-line Dockerfile (end with a single line containing a dot '.')")
    print("3. Load from existing file path")
    mode = input("Mode [1/2/3] (default 1): ").strip() or "1"

    dockerfile_content = ""

    if mode == "3":
        src = input("Enter source file path to load Dockerfile from: ").strip()
        if not src or not os.path.exists(src):
            print("Source file not found.")
            return
        with open(src, "r") as f:
            dockerfile_content = f.read()

    elif mode == "2":
        print("Paste your Dockerfile contents. End with a single '.' on its own line.")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == ".":
                break
            lines.append(line)
        dockerfile_content = "\n".join(lines) + "\n"

    else:
        base_image = input("Enter base image (default: python:3.12-slim): ").strip()
        if not base_image:
            base_image = "python:3.12-slim"

        start_cmd = input("Enter start command (default: python app.py): ").strip()
        if not start_cmd:
            start_cmd = "python app.py"

        # split command safely
        try:
            cmd_parts = shlex.split(start_cmd)
        except Exception:
            cmd_parts = start_cmd.split()

        cmd_array = ", ".join([f'"{p}"' for p in cmd_parts])

        dockerfile_content = (
            f"FROM {base_image}\n"
            f"WORKDIR /app\n"
            f"COPY . .\n"
            f"CMD [{cmd_array}]\n"
        )

    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(dockerfile_content)

    print(f"Dockerfile created successfully at {path}")


def search_local_images():
    """Search for local images matching a name or tag and display results."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    name = input("Enter image name or tag to search locally: ").strip()
    # Use docker images with a simple filter and print matching lines
    result = subprocess.run(["docker", "images"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("Failed to list local images:")
        print(result.stderr)
        return

    lines = result.stdout.splitlines()
    header = lines[0] if lines else ""
    matches = [l for l in lines if name.lower() in l.lower()]

    if not matches:
        print("No local images found matching:", name)
        return

    print(header)
    for m in matches:
        print(m)



def build_image():
    """Build a Docker image from a Dockerfile and tag it."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    dockerfile_path = input("Enter Dockerfile path (default: Dockerfile): ").strip()
    if not dockerfile_path:
        dockerfile_path = "Dockerfile"

    if not os.path.exists(dockerfile_path):
        print("Dockerfile not found.")
        return

    image_name = input("Enter image name:tag (e.g. myapp:1.0): ").strip()
    if not image_name:
        print("Image name cannot be empty.")
        return

    try:
        result = subprocess.run([
            "docker", "build",
            "-t", image_name,
            "-f", dockerfile_path,
            "."
        ], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Failed to build image:")
            print(result.stderr)
    except FileNotFoundError:
        print("Docker CLI not found. Please install Docker.")


def start_container():
    """Start a stopped container by ID or name (prints result)."""
    if not check_docker_running():
        print(ERROR_MSG)
        return

    # Show all containers so user can pick one to start
    subprocess.run(["docker", "ps", "-a"])
    cid = input("Enter container ID or name to start: ").strip()
    if not cid:
        print("Container ID/name cannot be empty.")
        return

    # validate container exists
    try:
        ps = subprocess.run(["docker", "ps", "-a", "--format", "{{.ID}}\t{{.Names}}"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        entries = [line.split("\t") for line in ps.stdout.splitlines() if line.strip()]
        ids = {e[0] for e in entries}
        names = {e[1] for e in entries}
    except Exception:
        ids = set()
        names = set()

    if cid not in ids and cid not in names:
        print(f"No such container: {cid}")
        return

    try:
        result = subprocess.run(["docker", "start", cid], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print("Failed to start container:", cid)
            print(result.stderr.strip())
    except FileNotFoundError:
        print("Docker CLI not found. Please install Docker.")
