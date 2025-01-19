import anthropic
import prompts
import sys
import argparse
import configparser
from pathlib import Path
from typing import List, Dict
from rich.console import Console

client = anthropic.Anthropic()


class LLMTool:
    def __init__(self):
        self.console = Console()
        self.config_path = Path.home() / ".hermes" / "config.ini"
        self.config = self._load_config()

    def _load_config(self):
        config = configparser.ConfigParser()

        if self.config_path.exists():
            config.read(self.config_path)
        else:
            config["DEFAULTS"] = {"api_key": "", "model": "", "max_tokens": "1000"}
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, "w") as f:
                config.write(f)

        return config

    def update_config(self, config_opts: Dict[str, str]) -> None:
        for k, v in config_opts.items():
            self.config["DEFAULTS"][k] = v

        with open(self.config_path, "w") as f:
            self.config.write(f)

    def call_api(self, prompt: str) -> str:
        # use sonnet for now
        return f"[bold green]Example response:[/bold green]{prompt}"

    def explain_code(self, file_path: str):
        code = self.read_file(file_path)

        prompt = prompts.explainer.replace("{{CODE}}", code)

        response = self.call_api(prompt)

        self.console.print(response)

    def optimize_code(self, file_path: str):
        code = self.read_file(file_path)

        prompt = prompts.optimizer.replace("{{CODE}}", code)

        response = self.call_api(prompt)

        self.console.print(response)

    def chat(self, message: str):
        prompt = prompts.chat
        prompt = prompt.replace("{{USER_QUERY}}", message)

        # read conversation history here
        conversation_history = ""
        prompt = prompt.replace("{{CONVERSATION_HISTORY}}", conversation_history)

        response = self.call_api(prompt)

        self.console.print(response)

    def read_file(self, file_path: str) -> str:
        try:
            code = ""
            with open(file_path) as f:
                code += f"{f.read().strip()}\n"
            return code.strip()
        except FileNotFoundError:
            self.console.print(f"[red]Error:[/red] File not found: {file_path}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    config_parser = subparsers.add_parser("config", help="Configure settings")
    config_parser.add_argument("--api-key", help="Set API key for your provider")
    config_parser.add_argument("--model", help="Set your model version")
    config_parser.add_argument("--max-tokens", help="Set max tokens")

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

    elif args.action == "config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        tool.update_config(args_dict)


if __name__ == "__main__":
    main()
