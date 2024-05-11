#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed. Please install Python 3.6 or higher and try again."
    exit 1
fi

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Setup completed successfully!"
