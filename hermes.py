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
from session import Session

client = anthropic.Anthropic()

history_path = Path.home() / ".hermes" / "conversations"
history_path.mkdir(parents=True, exist_ok=True)


class ChatCLI(cmd.Cmd):
    intro = "HERMES\nType help of ? to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.console = Console()
        self.config_path = Path.home() / ".hermes" / "config.ini"
        self.config = self._load_config()
        self.sessions: Dict[str, Session] = {}
        self.current_session = None
        self.load_sessions()

    def _load_config(self) -> None:
        config = configparser.ConfigParser()

        if self.config_path.exists():
            config.read(self.config_path)
        else:
            config["DEFAULTS"] = {"api_key": "", "model": "", "max_tokens": "1000"}
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, "w") as f:
                config.write(f)

        return config

    def save_config(self, config_opts: Dict[str, str]) -> None:
        for k, v in config_opts.items():
            self.config["DEFAULTS"][k] = v

        with open(self.config_path, "w") as f:
            self.config.write(f)

    def load_sessions(self) -> None:
        conversations = list(history_path.glob("*.json"))
        for convo in conversations:
            convo_id = convo.stem
            self.sessions[convo_id] = Session(convo_id)

    def do_new(self, arg):
        "Start a new chat"

        session = Session()
        self.sessions[session.id] = session
        self.current_session = session
        self.console.print(
            f"[bold green]Created new session with ID[/bold green]: [green]{session.id}[/green]"
        )

    def do_list(self, arg):
        "List all chats"
        if not self.sessions:
            print("No chats yet.")
            return

        self.console.print("[bold blue]Your chats:[/bold blue]")
        for session_id, session in self.sessions.items():
            msg_count = len(session.history)
            is_current = " (current)" if session == self.current_session else ""
            # last_updated = datetime.datetime.fromtimestamp(
            #        os.path.getmtime(convo_file)
            #    ).strftime("%Y-%m-%d %H:%M:%S")
            # print(f"- {session_id}: {msg_count} messages, last updated: {last_updated}{is_current}")

            self.console.print(
                f"- [green]{session_id}[/green]: {msg_count} messages {is_current}"
            )

    def do_switch(self, session_id):
        "Switch to a different chat: switch <session_id>"
        if not session_id:
            self.console.print("[red]Please provide a valid chat ID[/red]")
            return

        matching_sessions = [
            s for s in self.sessions.keys() if s.startswith(session_id)
        ]

        if len(matching_sessions) == 0:
            self.console.print(
                f"[red]No session found starting with {session_id}[/red]"
            )
        elif len(matching_sessions) > 1:
            self.console.print(
                f"[red]Multiple sessions found starting with {session_id}[/red]"
            )
        else:
            self.current_session = self.sessions[matching_sessions[0]]
            self.console.print(
                f"[bold green]Switched to session {self.current_session.id}[/bold green]"
            )
            self.do_history("")

    def do_send(self, message):
        "Send a message in the current session: send <message>"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/red]"
            )
            return

        if not message:
            self.console.print("[red]Provide a message to send[/red]")
            return

        self.current_session.add_message("user", message)
        # call LLM
        response = "example assistant response"
        self.console.print(f"\n{response}\n")

        self.current_session.add_message("assistant", response)

    def do_history(self, arg):
        "Show message history for the active session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/red]"
            )
            return

        if not self.current_session.history:
            self.console.print("[red]Current session is empty[/red]")

        self.console.print("\n[bold blue]Message history:[/bold blue]")
        for msg in self.current_session.history:
            if msg["role"].upper() == "USER":
                self.console.print(
                    f"\n[[yellow]{msg['role'].upper()}[/yellow]]: {msg['content']}"
                )
            elif msg["role"].upper() == "ASSISTANT":
                self.console.print(
                    f"\n[[orange1]{msg['role'].upper()}[/orange1]]: {msg['content']}"
                )
            else:
                # Don't print system messages
                pass
        self.console.print()

    def do_quit(self, arg):
        "Exit the chat CLI"
        self.console.print("[green]Goodbye![/green]")
        return True


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="Available actions")

    config_parser = subparsers.add_parser("config", help="Configure settings")
    config_parser.add_argument("--api-key", help="Set API key for your provider")
    config_parser.add_argument("--model", help="Set your model version")
    config_parser.add_argument("--max-tokens", help="Set max tokens")

    args = parser.parse_args()
    if args.action == "config":
        args_dict = {
            key: value for key, value in vars(args).items() if value is not None
        }
        del args_dict["action"]
        ChatCLI().save_config(args_dict)
        print("modified config")
        pass
    else:
        ChatCLI().cmdloop()


if __name__ == "__main__":
    main()
