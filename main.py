import sys
import argparse

from dotenv import load_dotenv

from agent import get_agent
from commands import say_text


# load environment variables
load_dotenv()

def main(command, model_name=None, provider=None):
    agent = get_agent(model_name, provider)

    result = agent.run(command)

    if result:
        say_text(f'The result is {result}')
    else:
        say_text(f'Finished doing {command}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GPT Automator CLI')
    parser.add_argument('command', help='The command to execute')
    parser.add_argument('--model', help='Model name')
    parser.add_argument('--provider', help='Model provider (openai, ollama, lm_studio)')

    args = parser.parse_args()

    if not args.command:
        print("Please provide a command to execute e.g. python main.py 'Open the calculator app'")
        exit(1)

    main(args.command, args.model, args.provider)
