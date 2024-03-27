# Termi

Termi is an interactive chatbot powered by an AI named Zero. Users can chat with Zero to ask questions, get information, or just have a conversation. This document provides instructions on setting up and running Termi on your system.

## Prerequisites

- git (for cloning the repository)
- Python 3.8 or higher

## Installation

1. **Clone the Repository**

    Clone Termi to your local machine using git:

    ```bash
    git clone https://github.com/choujar/termi.git
    cd termi
    ```

2. **Set Up `termi.sh`**

    Before running Termi, you need to make `termi.sh` executable. Here's how you can do it on various operating systems:

    - **Unix/macOS**:

        ```bash
        chmod +x termi.sh
        ```

    - **Windows**:

        Windows users might need to use Git Bash or WSL to run shell scripts. Ensure you have one of these environments set up to proceed.

3. **Install Dependencies**

    Install all dependencies listed in the `requirements.txt` file to ensure Termi runs smoothly.

    ```bash
    pip install -r requirements.txt
    ```

## Running Termi

After setting up, you can start Termi by running:

```bash
./termi.sh


### (Recommended) Add an Alias for Termi

For convenience, you can add an alias to your shell configuration file to run Termi from anywhere.

- **Unix/macOS**:

  Add this line to your `.bashrc` or `.zshrc` file:

  ```bash
  alias termi='/absolute/path/to/termi.sh'
  ```

  Replace `/absolute/path/to/` with the actual path to `termi.sh` on your system.

  After adding the alias, apply the changes:

  ```bash
  source ~/.bashrc # Or source ~/.zshrc
  ```

- **Windows**:

  On Windows, using Git Bash, you can add an alias in your `.bash_profile` or `.bashrc` file within your home directory:

  ```bash
  alias termi='/absolute/path/to/termi.sh'
  ```

  Make sure to replace `/absolute/path/to/` with the correct path. Restart Git Bash or source the configuration file to apply the changes.

### License

Termi is made available under the MIT License. This means you're free to use, modify, distribute, and make private use of the features provided by Termi as long as you include the original copyright and permission notice in any copies or substantial portions of the software.
