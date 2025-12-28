from docker_manager import *
from vm_manager import *
import os

def menu():
    print("\n=== Cloud Management System ===")
    print("c. Clear Screen")

    print("\n--- Docker ---")
    print("1. List Docker Images")
    print("2. Search Local Images")
    print("3. Search Image on DockerHub")
    print("4. Pull Docker Image")
    print("5. Create Dockerfile")
    print("6. Build Docker Image")
    print("7. Run Docker Image (create container)")
    print("8. List Running Containers")
    print("9. List All Containers (running + stopped)")
    print("10. Start Container")
    print("11. Stop Container")

    print("\n--- Virtual Machines (QEMU) ---")
    print("12. Create Virtual Machine (interactive)")
    print("13. Create VM from JSON config")
    print("14. List Virtual Machines (QEMU)")
    print("15. Delete Virtual Machine (QEMU)")

    print("0. Exit")

while True:
    menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        list_images()
    elif choice == "2":
        search_local_images()
    elif choice == "3":
        search_dockerhub()
    elif choice == "4":
        pull_image()
    elif choice == "5":
        create_dockerfile()
    elif choice == "6":
        build_image()
    elif choice == "7":
        run_image()
    elif choice == "8":
        list_running_containers()
    elif choice == "9":
        list_all_containers()
    elif choice == "10":
        start_container()
    elif choice == "11":
        stop_container()
    elif choice == "c":
        os.system("cls")
    elif choice == "12":
        create_vm()
    elif choice == "13":
        create_vm_from_config()
    elif choice == "14":
        list_vms()
    elif choice == "15":
        delete_vm()
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
