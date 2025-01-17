import anthropic
import prompts
import sys
import argparse
from typing import List

client = anthropic.Anthropic()


class LLMTool:
    def call_api(self, prompt: str) -> str:
        print(prompt)
        # use sonnet for now
        return ""

    def explain_code(self, file_path: str):
        code = self.read_file(file_path)
        prompt = prompts.explainer.replace("{{CODE}}", code)
        self.call_api(prompt)

    def optimize_code(self, file_path: str):
        code = self.read_file(file_path)
        prompt = prompts.optimizer.replace("{{CODE}}", code)
        self.call_api(prompt)

    def chat(self, message: str):
        prompt = prompts.chat
        prompt = prompt.replace("{{USER_QUERY}}", message)
        # read conversation history here
        conversation_history = ""
        prompt = prompt.replace("{{CONVERSATION_HISTORY}}", conversation_history)

        self.call_api(prompt)

    def read_file(self, file_path: str) -> str:
        try:
            code = ""
            with open(file_path) as f:
                code += f"{f.read().strip()}\n"
            return code.strip()
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    explain_parser = subparsers.add_parser("explain", help="Explain code")
    explain_parser.add_argument("file", help="File to explain")

    optimize_parser = subparsers.add_parser("optimize", help="Optimize code")
    optimize_parser.add_argument("file", help="File to optimize")

    chat_parser = subparsers.add_parser("chat", help="General chat")
    chat_parser.add_argument("message", nargs="+", help="Chat message for the LLM")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    tool = LLMTool()

    if args.action == "explain":
        tool.explain_code(args.file)

    elif args.action == "optimize":
        tool.optimize_code(args.file)

    elif args.action == "chat":
        message = " ".join(args.message)
        tool.chat(message)


if __name__ == "__main__":
    main()
