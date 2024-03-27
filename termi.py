import sys
import argparse
from collections import deque
import os
# Import the load_dotenv function from the dotenv module
from dotenv import load_dotenv
import time
from openai import OpenAI
from anthropic import Anthropic
from colorama import Fore, Back, Style
import colorama

# Initializes Colorama
colorama.init(autoreset=True)

# Call load_dotenv() at the start to load the .env file and environment variables
load_dotenv()


DEBUGGING = False

def printer(message, style, end="\n", flush=False):
    if style == "user":
        print(Fore.BLUE + Style.BRIGHT + message, end=end, flush=flush)
    elif style == "assistant":
        print(Fore.GREEN + Style.BRIGHT + message, end=end, flush=flush)
    elif style == "error":
        print(Fore.RED + message, end=end, flush=flush)
    elif style == "info":
        print(Fore.YELLOW + message, end=end, flush=flush)
    elif style == "question":
        print(Fore.LIGHTMAGENTA_EX + message, end=end, flush=flush)
    elif style == "tip":
        print(Fore.CYAN + message, end=end, flush=flush)
    elif style == "light":
        print(Fore.MAGENTA + message, end=end, flush=flush)
    elif style == "announcement":
        # Print announcement in bold with a white background
        print()
        print(Back.YELLOW + Fore.BLACK + Style.BRIGHT + ' ++ ' + message + ' ++ ', end=end, flush=flush)
        print()
    else:
        print(message, end=end, flush=flush)

def debug(message):
    if DEBUGGING:
        print(Fore.CYAN + message)

class ChatBot:

    system_prompt = "You are a helpful assistant called Zero. You rely on several AI models to provide the best answers to the user's questions. You can switch between models and clear the chat history. The current date and time is" + time.strftime("%c") + ". If the user message is blank or just 'begin', start with a greeting based on the time of day."
    AI_NAME = "Zero"

    models = {
        "openai": {
            "gpt": "gpt-4-0125-preview",
            "gpt-vision": "gpt-4-vision-preview",
            "gpt-3": "gpt-3.5-turbo-0125",
        },
        "anthropic": {
            "claude": "claude-3-opus-20240229",
            "sonnet": "claude-3-sonnet-20240229",
            "haiku": "claude-3-haiku-20240307",
        }
    }

    api_keys = {
        "openai": os.getenv("OPENAI_API_KEY", None),
        "anthropic": os.getenv("ANTHROPIC_API_KEY", None)
    }

    ai_providers = {
        "openai": ["gpt", "gpt-vision", "gpt-3"],
        "anthropic": ["claude", "sonnet", "haiku"]
    }

    commands = {
        "exit": {
            "description": "Exit the chatbot",
            "aliases": ["bye", "ciao", "adios", "quit"]
        },
        "clear history": {
            "description": "Clear the message history",
            "aliases": ["restart"]
        },
        "cls": {
            "description": "Clear the screen",
            "aliases": ["clear", "clean window"]
        },
        "switch model": {
            "description": "Switch to a different model",
            "aliases": ["model", "change model"]
        },
        "help": {
            "description": "Print the list of commands",
            "aliases": ["commands", "list commands"]
        }
    }

    def __init__(self, openai_api_key, anthropic_api_key, model_key):
        printer("Welcome to the AI chatbot!", "announcement")
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        self.model_key = model_key
        self.message_history = deque(maxlen=10)
        # check if self.openai_api_key is set, and if it is then set the ai providers and models
        if self.openai_api_key:
            self.open_ai_client = OpenAI(api_key=openai_api_key)
            printer("OpenAI API key is set", "info")
        
        if self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=anthropic_api_key)
            printer("Anthropic API key is set", "info")

        self.model_id = self.get_model_id(model_key)
        
        # print welcome message and which model is being used
        
        printer(f"Using model: {model_key} > {self.model_id}", "info")
        self.print_commands()
        print()

    @staticmethod
    def models_list():
        """Static method to return list of available model keys"""
        # return available models based on the api keys
        available_models = list()
        for provider, api_key in ChatBot.api_keys.items():
            if api_key:
                available_models.extend(ChatBot.models[provider].keys())
        return available_models
        

    @staticmethod
    def print_commands():
        """Static method to print the available commands"""
        printer("Commands available:", "info")
        for command, data in ChatBot.commands.items():
            aliases = ", ".join(data["aliases"])
            printer(f"  {command}: {data['description']}, [{aliases}]", "tip")

    def get_model_id(self, model_key):
        """Get the model ID based on the model key"""
        for provider, models in ChatBot.models.items():
            if model_key in models:
                return models[model_key]
        return None
    
    def timer_and_speed(self, start_time, end_time, message):
        time_taken = end_time - start_time
        words_per_second = len(message.split()) / time_taken
        # print(f"Time taken: {time_taken:.2f} seconds")
        printer(f"\n(Speed: {words_per_second:.2f} words per second)", "light")

    def openai_chat(self, messages):
        start_time = time.time()
        # add system prompt to the start of the messages
        messages_with_system = [{"role": "system", "content": self.system_prompt}] + list(messages)
        response = self.open_ai_client.chat.completions.create(
            model=self.model_id,
            messages=list(messages_with_system),
            stream=True,
        )
        assistant_message = ""
        printer(f"{self.AI_NAME}: ", "assistant", end="", flush=True)
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                printer(content, "assistant",  end="", flush=True)  # Print as it comes
                assistant_message += content  # Accumulate for history

        end_time = time.time()
        self.timer_and_speed(start_time, end_time, assistant_message)
        print()  # Print a newline after the AI's response
        return assistant_message

    def anthropic_chat(self, messages):
        # Assuming similar streaming API response from Anthropic
        start_time = time.time()
        assistant_message = ""
        printer(f"{self.AI_NAME}: ", "assistant", end="", flush=True)
        with self.anthropic_client.messages.stream(
            system=self.system_prompt,
            model=self.model_id,
            max_tokens=1024,
            messages=list(messages)
        ) as stream:    
            for text in stream.text_stream:
                printer(text, "assistant", end="", flush=True)
                assistant_message += text
        
        end_time = time.time()
        self.timer_and_speed(start_time, end_time, assistant_message)
        print()  # Print a newline after the AI's response
        return assistant_message

    def send_to_AI(self):
        try:
            if self.model_key in self.ai_providers["openai"]:
                debug("calling openai")
                # Call OpenAI API
                assistant_message = self.openai_chat(self.message_history)
            elif self.model_key in self.ai_providers["anthropic"]:
                # Call Anthropic API
                debug("calling anthropic")
                assistant_message = self.anthropic_chat(self.message_history)

            # Append the AI's response to the history after it's been accumulated
            if assistant_message:
                self.message_history.append({"role": "assistant", "content": assistant_message})

        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
        
    def do_command(self, is_command, command):
        if is_command and command == "exit":
            print("Goodbye!\n")
            # Exit the chat
            sys.exit(0)
        elif is_command and command == "help":
            self.print_commands()
        elif is_command and command == "clear history":
            self.message_history.clear()
            print("Message history cleared.")
        elif is_command and command == "switch model":
            print("Switching model...")
            print("Available models: ", self.models_list())
            new_model_key = input("Enter the model key: ")
            if new_model_key in self.models_list():
                self.model_key = new_model_key
                self.model_id = self.get_model_id(self.model_key)
                print(f"Switched to {self.model_key} model > {self.model_id}")
            else:
                print(f"Invalid model key '{new_model_key}'. Using the current model '{self.model_key}'.")
        elif is_command and command == "cls":
            os.system("clear" if os.name == 'posix' else "cls")


    def chat(self, initial_messages=None):
        if initial_messages:
            self.message_history.extend(initial_messages)
        else:
            # add a 'begin' message to start the conversation
            self.message_history.append({"role": "user", "content": "begin"})
            self.send_to_AI()
        

        while True:
            user_input = input("\nYou: ")
            is_command = False
            command = None
            # is user_input.lower() in commands or any of the aliases?
            for cmd, data in ChatBot.commands.items():
                if user_input.lower() in [cmd] + data["aliases"]:
                    is_command = True
                    command = cmd
                    break
            
            self.do_command(is_command, command)


            self.message_history.append({"role": "user", "content": user_input})

            self.send_to_AI()





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with AI")
    parser.add_argument("initial_message", type=str, nargs="?", default=None, help="Initial message to start the chat")
    parser.add_argument("--model", type=str, default="haiku", help="Model key to use (e.g., 'gpt', 'claude')")
    args = parser.parse_args()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    if not openai_api_key or not anthropic_api_key:
        printer("At least one of the API keys is required to continue. Exiting...", "error")
        sys.exit(1)

    # model_key should be either the default model or the one passed as an argument
    model_key = args.model

    # Use the static method to get the list of models
    list_of_models = ChatBot.models_list()

    if model_key not in list_of_models:
        printer(f"Invalid model key '{model_key}'. Available models: {list_of_models}", "error")
        sys.exit(1)
        

    
            

   

    chatbot = ChatBot(openai_api_key, anthropic_api_key, model_key)
    initial_msgs = [{"role": "user", "content": args.initial_message}] if args.initial_message else []

    chatbot.chat(initial_msgs)

