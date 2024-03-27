#!/bin/bash

# Display the current values of the keys
echo "Current OPENAI_API_KEY: $OPENAI_API_KEY"
echo "Current ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY"

# Ask the user if they want to delete the keys
read -p "Do you want to delete these environment variables? (y/N): " response

# Check the user's response
case $response in
    [yY])
        # User wants to delete the keys
        echo "Deleting OPENAI_API_KEY and ANTHROPIC_API_KEY..."
        unset OPENAI_API_KEY
        unset ANTHROPIC_API_KEY
        # Check if the keys were deleted
        echo "Current OPENAI_API_KEY: $OPENAI_API_KEY"
        echo "Current ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY"
        echo "Environment variables deleted."
        ;;
    *)
        # User does not want to delete the keys or invalid input
        echo "No changes made."
        ;;
esac
