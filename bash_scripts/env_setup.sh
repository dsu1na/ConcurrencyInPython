#!/bin/bash

# Define the name of the virtual environment directory
VENV_NAME="PythonConcurrencyEnv"

# Define requirements.txt directory
R_TXT="/ConcurrencyInPython/requirements.txt"

# Check if a virtual environment already exists
if [ -d "$VENV_NAME" ]; then
    echo "Virtual environment '$VENV_NAME' already exists."
    echo "To remove it, run: rm -rf $VENV_NAME"
    exit 0
fi

echo "Creating virtual environment '$VENV_NAME'..."
python3 -m venv "$VENV_NAME"

# Check if the virtual environment creation was successful
if [ $? -eq 0 ]; then
    echo "Virtual environment created successfully."

else
    echo "Error: Failed to create virtual environment."
    exit 1
fi

echo "Activating environment '$VENV_NAME' ..."
. /"$VENV_NAME"/bin/activate

