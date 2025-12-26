from docker_manager import *
import os

def menu():
    print("\n=== Cloud Management System (Docker) ===")
    print("c. Clear Screen")
    print("1. List Docker Images")
    print("2. List Running Containers")
    print("3. List All Containers (running + stopped)")
    print("4. Stop Container")
    print("5. Search Image on DockerHub")
    print("6. Pull Docker Image")
    print("7. Run Docker Image (create container)")
    print("8. Create Dockerfile")
    print("9. Build Docker Image")
    print("0. Exit")

while True:
    menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        list_images()
    elif choice == "2":
        list_running_containers()
    elif choice == "3":
        list_all_containers()
    elif choice == "4":
        stop_container()
    elif choice == "5":
        search_dockerhub()
    elif choice == "6":
        pull_image()
    elif choice == "c":
        os.system("cls")
    elif choice == "7":
        run_image()
    elif choice == "8":
        create_dockerfile()
    elif choice == "9":
        build_image()
    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
