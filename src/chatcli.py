import anthropic
import configparser
import os
import prompts
import json
import cmd
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich import print
from session import Session
from constants import CONFIG_PATH, HISTORY_PATH


class ChatCLI(cmd.Cmd):
    intro = "HERMES\nType help of ? to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.console = Console()
        self.config = self._load_config()
        self.sessions: Dict[str, Session] = {}
        self.current_session: Optional[Session] = None
        self.load_sessions()

    def _load_config(self) -> configparser.ConfigParser:
        config = configparser.ConfigParser()

        if CONFIG_PATH.exists():
            config.read(CONFIG_PATH)
        else:
            config["DEFAULT"] = {
                "api_key": "NOTSET",
                "model": "NOTSET",
                "max_tokens": "1000",
            }
            CONFIG_PATH.parent.mkdir(exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                config.write(f)

        return config

    # TODO: config stuff should probably be extracted
    def save_config(
        self, config_opts: Dict[str, str], settings_name: str = "DEFAULT"
    ) -> None:
        if settings_name not in self.config:
            self.config[settings_name] = {
                "api_key": "NOTSET",
                "model": "NOTSET",
                "max_tokens": "1000",
            }

        for k, v in config_opts.items():
            self.config[settings_name][k] = v

        CONFIG_PATH.parent.mkdir(exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            self.config.write(f)

    def load_sessions(self) -> None:
        conversations = list(HISTORY_PATH.glob("*.json"))
        for convo in conversations:
            convo_id = convo.stem
            self.sessions[convo_id] = Session(convo_id)

    def do_new(self, arg):
        "Start a new chat"

        session = Session()
        self.sessions[session.id] = session
        self.current_session = session
        self.console.print(f"[bold green]Created new session:[/] {session.id}")

    def do_title(self, arg):
        "Set/Get the title for the current session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/red]"
            )
            return

        if not arg:
            self.console.print(f"Current title: {self.current_session.title}")
            return

        self.current_session.title = arg
        self.current_session.save_history()
        self.console.print(f"[bold green]Set title to:[/bold green] {arg}")

    def do_settings(self, arg):
        "Change the settings for the current session: settings <settings_name>"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/red]"
            )
            return

        if not arg:
            settings = self.current_session.settings
            # Conversation settings might not exist if the config was modified manually
            if settings not in self.config:
                self.console.print(
                    f"[red]Current sessions settings do not exist: {settings}[/]"
                )
                return

            model_name = self.config[settings]["model"]
            max_tokens = self.config[settings]["max_tokens"]
            self.console.print(
                f"({settings}) model = {model_name}, max_tokens = {max_tokens}"
            )
            return

        if arg not in self.config:
            self.console.print(
                f"[red]Invalid settings name. Choose from: {', '.join(self.config.keys())}[/]"
            )
            return

        self.current_session.settings = arg
        self.current_session.save_history()
        self.console.print(f"[bold green]Switched to settings: {arg}[/]")

    def do_list(self, arg):
        "List all chats"
        if not self.sessions:
            print("No chats yet.")
            return

        table = Table(title="All Chats:")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Created At")
        table.add_column("Settings")
        table.add_column("Messages", justify="right")
        table.add_column("Tokens", justify="right")

        for session_id, session in self.sessions.items():
            is_current = " (current)" if session == self.current_session else ""

            title = f"{session.title} " if session.title else "(Untitled) "
            msg_count = str(len(session.history))
            token_count = str(session.get_token_count())
            table.add_row(
                session_id,
                title,
                session.created_at,
                session.settings,
                msg_count,
                token_count,
            )

        self.console.print(table)

    def do_switch(self, session_id):
        "Switch to a different chat: switch <session_id>"
        if not session_id:
            self.console.print("[red]Please provide a valid chat ID[/red]")
            return

        # Allow prefix matching of conversation IDs
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
                f"[bold green]Switched to session:[/] ({self.current_session.title}) {self.current_session.id}"
            )

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
            self.console.print("[red]Current session is empty.[/]")
            return

        history_text = ""
        for msg in self.current_session.history:
            content = msg.content.strip()
            if msg.role.upper() == "USER":
                history_text += (
                    f"\n[[bold green]{msg.role.upper()}[/]]: {msg.content}\n"
                )
            elif msg.role.upper() == "ASSISTANT":
                history_text += f"\n[[bold blue]{msg.role.upper()}[/]]: {msg.content}\n"
            else:
                history_text += (
                    f"\n[[bold yellow]{msg.role.upper()}[/]]: {msg.content}\n"
                )

        print(
            Panel(
                history_text.strip(),
                title=f"Chat History ({self.current_session.title})",
                box=box.ROUNDED,
                border_style="bright_black",
                padding=(1, 2),
            )
        )
        self.console.print()

    def do_tokens(self, arg):
        "Show token usage for the current session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/red]"
            )
            return

        self.console.print(
            f"Total session tokens: {self.current_session.get_token_count()}"
        )

    def do_quit(self, arg):
        "Exit the chat CLI"
        self.console.print("[green]Goodbye![/green]")
        return True
