#!/bin/bash

# Define the path to the .env file
ENV_FILE="/Users/sahil/Sites/labs/scripts/talk/.env"

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
fi

# Path to the Python executable within the virtual environment
PYTHON="/Users/sahil/Sites/labs/scripts/talk/myenv/bin/python"

# Path to your Python script
SCRIPT="/Users/sahil/Sites/labs/scripts/talk/talk.py"

# Execute the Python script using the Python interpreter from the virtual environment
$PYTHON $SCRIPT "$@"
