# ☁️ Cloud Management System

A command-line based **Cloud Management System** developed as part of the *Cloud Computing and Networking* course.  
The project provides a unified interface to manage **Docker containers and images** as well as **QEMU virtual machines**, demonstrating core virtualization and cloud infrastructure concepts.

---

## 📌 Project Overview

This system allows users to perform common cloud management tasks through a **menu-driven CLI**, including:
- Docker image and container management
- Dockerfile creation and image building
- Basic virtual machine management using QEMU

The project focuses on **practical understanding** rather than graphical interfaces, aligning with industry-standard cloud tools.

---

## 🐳 Docker Features

- List Docker images
- List running Docker containers
- List all containers (running + stopped)
- Stop a running container
- Search for Docker images on DockerHub
- Pull Docker images from DockerHub
- Run Docker images and create containers
- Create Dockerfiles using a configurable template
- Build Docker images from Dockerfiles

---

## 🖥️ QEMU Virtual Machine Features

- Create virtual machines using QEMU
  - Configure CPU, RAM, and disk size
- Automatically generate QCOW2 disk images
- List all available virtual machines
- Delete virtual machines safely
- Verify VM existence through disk image detection

> Virtual machines are represented as **QCOW2 disk image files**, and system resources are consumed only while the VM is running.

---

## 🛠️ Technologies Used

- **Python 3**
- **Docker & Docker CLI**
- **QEMU**
- **Git & GitHub**
