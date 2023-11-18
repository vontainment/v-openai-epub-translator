#!/bin/bash

# Define the directory where the virtual environment will be located.
VENV_DIR="venv"

# Check if the virtual environment directory exists.
if [ ! -d "$VENV_DIR" ]; then
    # If it doesn't exist, set one up.
    echo "Setting up the Python virtual environment..."

    # Create the Python virtual environment.
    python -m venv $VENV_DIR

    # Activate the newly created virtual environment.
    source $VENV_DIR/bin/activate

    # Install the project's Python dependencies from the requirements file.
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    # If it exists, just activate the existing virtual environment.
    echo "Activating existing Python virtual environment..."
    source $VENV_DIR/bin/activate
fi

# The next few lines collect user input on the processing parameters.

# Prompt for the path to the input EPUB file, and read user input into the variable.
echo "Enter the path to the input EPUB file:"
read INPUT

# Prompt for the path to the output directory, and read user input into the variable.
echo "Enter the path for the output directory:"
read OUTPUT

# Prompt for the output language code, and read user input into the variable.
echo "Enter the output language code (e.g., 'en', 'de', 'es'):"
read LANGUAGE

# Prompt for the desired processing stage, and read user input into the variable.
echo "Enter the processing stage ('chunk', 'translate', 'assemble'):"
read STAGE

# Construct the command to process the EPUB file using the parameters provided by the user.
COMMAND="python main.py --input \"$INPUT\" --output \"$OUTPUT\" --output-language $LANGUAGE --stage $STAGE"
echo "Running command: $COMMAND"
# Execute the constructed command.
eval $COMMAND
