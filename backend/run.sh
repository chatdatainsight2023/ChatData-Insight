#!/bin/bash

# Define the name of the virtual environment
VENV_NAME="polardash-backend-env"

# Check if the virtual environment exists
if [ ! -d "$VENV_NAME" ]
then
    echo "Virtual environment does not exist, creating..."
    python3 -m venv $VENV_NAME
else
    echo "Virtual environment exists, skipping creation step..."
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run main.py
echo "Starting the application..."
python main.py

