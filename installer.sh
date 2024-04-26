#!/bin/bash

# Ubuntu 20.04 is required without any updates

# Verify that we are running on Ubuntu 20.04
if [[ $(lsb_release -rs) != "20.04" ]]; then
    echo "This script is only compatible with Ubuntu 20.04."
    exit 1
fi

# Download the official NVIDIA drivers
echo "Please manually download the NVIDIA drivers from the following link:"
echo "https://www.nvidia.es/download/driverResults.aspx/224377/es"
echo "Save the downloaded file in the directory $(pwd) and run this script again."
read -p "Press [Enter] once you have downloaded the driver..."

# Verify if the driver file is present
if [ ! -f NVIDIA-Linux-x86_64-*.run ]; then
    echo "Driver file not found. Make sure you have downloaded it to the directory $(pwd)"
    exit 1
fi

# Update the system
sudo apt update && sudo apt upgrade -y

# Install basic development tools
sudo apt install build-essential -y

# Install software-properties-common to add repositories
sudo apt install software-properties-common -y

# Add the deadsnakes repository for Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa -y

# Install Python 3.10
sudo apt install python3.10 -y

# Install pip for Python 3
sudo apt install python3-pip -y

# Install the venv module for Python 3.10
sudo apt install python3.10-venv -y

# Install python3.10-dev for development and compiling extensions
sudo apt install python3.10-dev -y

# Install the TTS library for Python
pip install TTS

# List available models in TTS
tts --list_models

# Update and install Whisper
pip install -U openai-whisper

# Install ffmpeg
sudo apt update && sudo apt install ffmpeg -y

# Install the OpenAI library for Python
pip install openai

# Install the pydub library for audio manipulation
pip install pydub

# End of installation
echo "Installation complete. All required packages and libraries are installed."
