import cmd
import anthropic
import prompts
import sys
import json
import argparse
import configparser
from uuid import uuid4
import datetime
import os
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console

client = anthropic.Anthropic()

history_path = Path.home() / ".hermes" / "conversations"
history_path.mkdir(parents=True, exist_ok=True)

class Chat:
    def __init__(self, id: str = None):
        self.id = id or str(uuid4())
        self.history_file = history_path / f"{self.id}.json"
        self.history: List[Dict] = []
        self.load_history()

    def load_history(self) -> None:
        if self.history_file.exists():
            with open(self.history_file) as f:
                self.history = json.load(f)

    def save_history(self) -> None:
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        self.save_history()

class ChatCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        #self.config_path = Path.home() / ".hermes" / "config.ini"
        #self.config = self._load_config()
        self.sessions: Dict[str, Chat] = {}
        self.current_session = None
        self.load_sessions()
        
    def load_sessions(self) -> None:
        conversations = list(history_path.glob("*.json"))
        for convo in conversations:
            convo_id = convo.stem
            self.sessions[convo_id] = Chat(convo_id)

    def do_new(self, arg):
        'Start a new chat'
        session = Chat()
        self.sessions[session.id] = session
        self.current_session = session
        print(f"Created new session with ID: {session.id}")

    def do_list(self, arg):
        'List all chats'
        if not self.sessions:
            print("No chats yet.")
            return

        print("Your chats:")
        for session_id, session in self.sessions.items():
            msg_count = len(session.history)
            is_current = " (current)" if session == self.current_session else ""
            #last_updated = datetime.datetime.fromtimestamp(
            #        os.path.getmtime(convo_file)
            #    ).strftime("%Y-%m-%d %H:%M:%S")
            #print(f"- {session_id}: {msg_count} messages, last updated: {last_updated}{is_current}")

            print(f"- {session_id}: {msg_count} messages {is_current}")
    def do_switch(self, session_id):
        'Switch to a different chat: switch <session_id>'
        if not session_id or session_id not in self.sessions:
            print("Please provide a valid chat ID")
            return

        self.current_session = self.sessions[session_id]
        print(f"Switched to session {self.current_session.id}")
        self.do_history("")

    def do_send(self, message):
        'Send a message in the current session: send <message>'
        if not self.current_session:
            print("You're not in a session. Start one with 'new' or switch to an existing one with 'switch'")
            return

        if not message:
            print("Provide a message to send")
            return

        self.current_session.add_message("user", message)
        # call LLM
        response = "example assistant response"
        print(f"\n{response}\n")

        self.current_session.add_message("assistant", response)

    def do_history(self, arg):
        'Show message history for the active session'
        if not self.current_session:
            print("You're not in a session. Start one with 'new' or switch to an existing one with 'switch'")
            return

        if not self.current_session.history:
            print("Current session is empty")

        print("\nMessage history:")
        for msg in self.current_session.history:
            print(f"\n[{msg['role'].upper()}]: {msg['content']}")
        print()

    def do_quit(self, arg):
        'Exit the chat CLI'
        print("Goodbye!")
        return True

class LLMTool:
    def __init__(self):
        self.console = Console()
        self.config_path = Path.home() / ".hermes" / "config.ini"
        self.config = self._load_config()
        self.history_path = Path.home() / ".hermes" / "conversations"
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.current_conversation_id = None

    def _load_config(self) -> configparser.ConfigParser:
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

    def _load_conversation(self, conversation_id: str) -> List[Dict]:
        history_file = self.history_path / f"{conversation_id}.json"
        if not history_file.exists():
            self.console.print(
                f"[red]Error:[/red] Conversation not found: {conversation_id}"
            )
            sys.exit(1)
        with open(history_file) as f:
            return json.load(f)

    def _save_conversation(self, conversation_id: str, messages: List[Dict]) -> None:
        history_file = self.history_path / f"{conversation_id}.json"
        with open(history_file, "w") as f:
            json.dump(messages, f, indent=2)

    def list_conversations(self) -> None:
        conversations = list(self.history_path.glob("*.json"))

        if not conversations:
            self.console.print("[yellow]No saved conversations[/yellow]")
            return

        self.console.print("[bold blue]Saved conversations:[/bold blue]")
        for convo_file in conversations:
            convo_id = convo_file.stem
            try:
                messages = self._load_conversation(convo_id)
                last_updated = datetime.datetime.fromtimestamp(
                    os.path.getmtime(convo_file)
                ).strftime("%Y-%m-%d %H:%M:%S")
                self.console.print(f"[green]{convo_id}[/green]")
                self.console.print(f" - Last updated: {last_updated}")
                self.console.print(f" - Last message: {messages[-1]['content'][:50]}")
                self.console.print()
            except Exception as e:
                self.console.print(f"[red]Error loading conversation {convo_id}[/red]")

    def call_api(self, prompt: str) -> str:
        # use sonnet for now
        return f"example response"

    def explain_code(self, file_path: str) -> None:
        code = self.read_file(file_path)

        prompt = prompts.explainer.replace("{{CODE}}", code)

        response = self.call_api(prompt)

        self.console.print(response)

    def optimize_code(self, file_path: str) -> None:
        code = self.read_file(file_path)

        prompt = prompts.optimizer.replace("{{CODE}}", code)

        response = self.call_api(prompt)

        self.console.print(response)

    def chat(self, message: str, conversation_id: Optional[str]) -> None:
        if conversation_id:
            # Load the previous conversation state with the new message
            self.current_conversation_id = conversation_id
            messages = self._load_conversation(conversation_id)
            if not messages:
                messages = [{"role": "system", "content": prompts.chat}]
        else:
            # Create a new conversation with the chat prompt
            self.current_conversation_id = str(uuid.uuid4())
            messages = [{"role": "system", "content": prompts.chat}]

        messages.append({"role": "user", "content": message})
        response = self.call_api(message)

        messages.append({"role": "assistant", "content": response})

        self._save_conversation(self.current_conversation_id, messages)

    def read_file(self, file_path: str) -> str:
        try:
            code = ""
            with open(file_path) as f:
                code += f"{f.read().strip()}\n"
            return code.strip()
        except FileNotFoundError:
            self.console.print(f"[red]Error:[/red] File not found: {file_path}")
            sys.exit(1)


def main_deprecated():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    config_parser = subparsers.add_parser("config", help="Configure settings")
    config_parser.add_argument("--api-key", help="Set API key for your provider")
    config_parser.add_argument("--model", help="Set your model version")
    config_parser.add_argument("--max-tokens", help="Set max tokens")

    #explain_parser = subparsers.add_parser("explain", help="Explain code")
    #explain_parser.add_argument("file", help="File to explain")

    #optimize_parser = subparsers.add_parser("optimize", help="Optimize code")
    #optimize_parser.add_argument("file", help="File to optimize")

    chat_parser = subparsers.add_parser("chat", help="General chat")
    chat_parser.add_argument("message", nargs="+", help="Chat message for the LLM")
    chat_parser.add_argument("file", help="File for the LLM")
    chat_parser.add_argument(
        "--convo_id", help="Conversation ID to continue a conversation"
    )

    list_parser = subparsers.add_parser("list", help="List all conversations")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    tool = LLMTool()

    if args.action == "chat":
        message = " ".join(args.message)
        if args.convo_id:
            tool.chat(message, args.convo_id)
        else:
            tool.chat(message, None)

    elif args.action == "list":
        tool.list_conversations()

    elif args.action == "config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        tool.update_config(args_dict)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    config_parser = subparsers.add_parser("config", help="Configure settings")
    config_parser.add_argument("--api-key", help="Set API key for your provider")
    config_parser.add_argument("--model", help="Set your model version")
    config_parser.add_argument("--max-tokens", help="Set max tokens")

    args = parser.parse_args()
    if args.action == "config":
        #modify config
        print("modified config")
        pass
    else:
        ChatCLI().cmdloop()

if __name__ == "__main__":
    main()
