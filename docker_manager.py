import subprocess
import os

ERROR_MSG = "Docker Engine is not running. Please start Docker."

def check_docker_running():
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
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "images"])


def list_running_containers():
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "ps"])

def list_all_containers():
    if not check_docker_running():
        print(ERROR_MSG)
        return
    subprocess.run(["docker", "ps","-a"])

def run_image():
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
    subprocess.run(cmd)
def stop_container():
    if not check_docker_running():
        print(ERROR_MSG)
        return

    list_running_containers()
    cid = input("Enter container ID or name to stop: ").strip()
    subprocess.run(["docker", "stop", cid])


def search_dockerhub():
    if not check_docker_running():
        print(ERROR_MSG)
        return

    name = input("Enter image name to search on DockerHub: ").strip()
    subprocess.run(["docker", "search", name])



def pull_image():
    if not check_docker_running():
        print(ERROR_MSG)
        return

    name = input("Enter image name to pull: ").strip()
    subprocess.run(["docker", "pull", name])



def create_dockerfile():
    path = input("Enter path to save Dockerfile (default: ./Dockerfile): ").strip()
    if not path:
        path = "Dockerfile"

    if os.path.exists(path):
        confirm = input("Dockerfile already exists. Overwrite? (y/n): ").lower()
        if confirm != "y":
            print("Operation cancelled.")
            return

    base_image = input("Enter base image (default: python:3.12-slim): ").strip()
    if not base_image:
        base_image = "python:3.12-slim"

    start_cmd = input("Enter start command (default: python app.py): ").strip()
    if not start_cmd:
        start_cmd = "python app.py"

    # split command safely
    cmd_parts = start_cmd.split()

    dockerfile_content = (
        f"FROM {base_image}\n"
        f"WORKDIR /app\n"
        f"COPY . .\n"
        f'CMD ["{cmd_parts[0]}", "{cmd_parts[1]}"]\n'
    )

    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(dockerfile_content)

    print(f"Dockerfile created successfully at {path}")



def build_image():
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

    subprocess.run([
        "docker", "build",
        "-t", image_name,
        "-f", dockerfile_path,
        "."
    ])
