#!/usr/bin/env python3
"""
Legion Core Claw - Docker Build and Run Script
Usage: python docker_build.py [--build] [--run] [--tag <tag>]
"""

import subprocess
import argparse
import sys
import os

DOCKERFILE = "runtime/Dockerfile"
IMAGE_NAME = "legion-core-claw"
DEFAULT_TAG = "latest"
CONTAINER_PORT = 8000
HOST_PORT = 8000


def build_image(tag=DEFAULT_TAG):
    """Build Docker image."""
    print(f"🐳 Building Docker image: {IMAGE_NAME}:{tag}")
    
    cmd = [
        "docker", "build",
        "-f", DOCKERFILE,
        "-t", f"{IMAGE_NAME}:{tag}",
        "-t", f"{IMAGE_NAME}:latest",
        "."
    ]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Failed to build image")
        return False
    
    print(f"✓ Image built successfully: {IMAGE_NAME}:{tag}")
    return True


def run_container(tag=DEFAULT_TAG, detach=False, port=HOST_PORT):
    """Run Docker container."""
    print(f"🚀 Starting container from {IMAGE_NAME}:{tag}")
    
    env_file = ".env" if os.path.exists(".env") else ".env.example"
    
    cmd = [
        "docker", "run",
        "--env-file", env_file,
        "-p", f"{port}:{CONTAINER_PORT}",
        "--name", f"legion-{tag}",
    ]
    
    if detach:
        cmd.append("-d")
    
    cmd.append(f"{IMAGE_NAME}:{tag}")
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Failed to start container")
        return False
    
    print(f"✓ Container started: legion-{tag}")
    return True


def list_images():
    """List Legion images."""
    cmd = ["docker", "images", "--filter", f"reference={IMAGE_NAME}"]
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Legion Core Claw Docker Build/Run")
    parser.add_argument("--build", action="store_true", help="Build Docker image")
    parser.add_argument("--run", action="store_true", help="Run Docker container")
    parser.add_argument("--detach", action="store_true", help="Run container in background")
    parser.add_argument("--tag", default=DEFAULT_TAG, help="Docker image tag")
    parser.add_argument("--port", type=int, default=HOST_PORT, help="Host port mapping")
    parser.add_argument("--list", action="store_true", help="List existing images")
    
    args = parser.parse_args()
    
    # Check Docker is installed
    if subprocess.run(["which", "docker"], capture_output=True).returncode != 0:
        print("❌ Docker not found. Please install Docker.")
        sys.exit(1)
    
    if args.list:
        list_images()
        return
    
    if args.build:
        if not build_image(args.tag):
            sys.exit(1)
    
    if args.run:
        if not run_container(args.tag, args.detach, args.port):
            sys.exit(1)
    
    if not args.build and not args.run and not args.list:
        parser.print_help()


if __name__ == "__main__":
    main()
