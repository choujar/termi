#!/bin/bash

# Define the path to the .env file
ENV_FILE="./.env"

# Function to load environment variables from the .env file
load_env() {
  if [ -f "$ENV_FILE" ]; then
    export $(cat "$ENV_FILE" | sed 's/#.*//g' | xargs)
  fi
}

# Function to ask for API keys and update the .env file
update_env() {
  echo "API keys are not set or incomplete. Please enter them."

  # Ask for the OPENAI_API_KEY
  read -p "Enter your OpenAI API key: " openai_key
  echo "OPENAI_API_KEY=$openai_key" > "$ENV_FILE"

  # Ask for the ANTHROPIC_API_KEY
  read -p "Enter your Anthropic API key: " anthropic_key
  echo "ANTHROPIC_API_KEY=$anthropic_key" >> "$ENV_FILE"

  # Source the .env file to export the newly set variables
  load_env
}

# Load existing environment variables
load_env

# Check if both keys are set
if [[ -z "$OPENAI_API_KEY" || -z "$ANTHROPIC_API_KEY" ]]; then
  # If not, prompt the user and update .env
  update_env
  # if they are set, print them
else
  echo "Open AI API Key is set to: $OPENAI_API_KEY"
  echo "Anthropic API Key is set to: $ANTHROPIC_API_KEY"
  
fi

# Define the path for the virtual environment
VENV_PATH="./myenv"

# Check if the virtual environment already exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Creating one now..."
    # Create the virtual environment
    python3 -m venv $VENV_PATH
    
    # Activate the virtual environment
    source $VENV_PATH/bin/activate
    
    echo "Virtual environment created and activated."
    
    # Install dependencies from requirements.txt
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "Dependencies installed."
else
    echo "Virtual environment found. Activating..."
    # Activate the virtual environment
    source $VENV_PATH/bin/activate
fi



# Execute the Python script using the Python interpreter from the virtual environment
$VENV_PATH/bin/python termi.py "$@"

# Deactivate the virtual environment
deactivate
