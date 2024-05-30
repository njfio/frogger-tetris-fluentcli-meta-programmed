#!/bin/bash

# Check if the script is being run with root privileges
if [[ $EUID -ne 0 ]]; then
  echo "This script requires root privileges. Please run with sudo."
  exit 1
fi

# Update package lists
apt update

# Install Python and pip
apt install -y python3 python3-pip

# Create a virtual environment (recommended)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install Pygame
pip install pygame

# Test Pygame installation (optional)
python3 -m pygame.examples.aliens

echo "Python development environment with Pygame is set up!"
echo "Remember to activate the virtual environment with 'source .venv/bin/activate'"
