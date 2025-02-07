from typing import Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich import print
from models.session import Session
from utils.constants import HISTORY_PATH
from config.manager import ConfigManager
from providers.manager import ProviderManager


class ChatCLI:
    def __init__(self, config_path):
        super().__init__()

        self.running = True

        self.console = Console()
        self.config_manager = ConfigManager(config_path)

        self.sessions: Dict[str, Session] = {}
        self.current_session: Optional[Session] = None
        self.load_sessions()

        self.provider = None

        self.commands = {
            "new": self.new,
            "branch": self.branch,
            "title": self.title,
            "settings": self.settings,
            "list": self.list,
            "switch": self.switch,
            "send": self.send,
            "history": self.history,
            "tokens": self.tokens,
            "delete": self.delete,
            "quit": self.quit,
            "help": self.help,
        }

        self.multiline_mode = False
        self.multiline_buffer = []

    def load_sessions(self) -> None:
        if not HISTORY_PATH.exists():
            HISTORY_PATH.mkdir(exist_ok=True)
        else:
            conversations = list(HISTORY_PATH.glob("*.json"))
            for convo in conversations:
                convo_id = convo.stem
                self.sessions[convo_id] = Session(convo_id)

    def update_provider(self):
        settings = self.current_session.settings
        config = self.config_manager.get_config(settings)
        if config["api_key"] == "NOTSET":
            self.console.print(f"[red]API key not set for settings: {settings}[/]")
            self.provider = None
            return
        if config["model"] == "NOTSET":
            self.console.print(f"[red]Model not set for settings: {settings}[/]")
            self.provider = None
            return
        self.provider = ProviderManager.get_provider(config)

    def new(self, arg):
        "Start a new chat: /new"

        session = Session()
        self.sessions[session.id] = session
        self.current_session = session
        self.update_provider()
        self.console.print(f"[bold green]Created new session:[/] {session.id}")

    def title(self, arg):
        "Set the title for the current session, /title <title>"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        if not arg:
            self.console.print(f"Current title: {self.current_session.title}")
            return

        self.current_session.title = arg
        self.current_session.save_history()
        self.console.print(f"[bold green]Set title to:[/] {arg}")

    def settings(self, arg):
        "Change the settings for the current session: /settings <settings_name>"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        if not arg:
            settings = self.current_session.settings
            # Conversation settings might not exist if the config was modified manually
            if settings not in self.config_manager.configs:
                self.console.print(
                    f"[red]Current sessions settings do not exist: {settings}[/]"
                )
                return

            # Display config
            self.config_manager.print_config(settings)

            return

        if arg not in self.config_manager.configs:
            self.console.print(
                f"[red]Invalid settings name. Choose from: {', '.join(self.config_manager.get_config_names())}[/]"
            )
            return

        self.current_session.settings = arg
        self.update_provider()
        self.current_session.save_history()
        self.console.print(f"[bold green]Switched to settings: {arg}[/]")

    def list(self, arg):
        "List all chats"
        if not self.sessions:
            self.console.print(f"[red]No chats yet. Start one with 'new'[/]")
            return

        table = Table(title="All Chats:")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Created At")
        table.add_column("Branched From")
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
                session.branched_from,
                session.settings,
                msg_count,
                token_count,
            )

        self.console.print(table)

    def switch(self, session_id):
        "Switch to a different session: /switch <session_id>"
        if not session_id:
            self.console.print("[red]Please provide a valid chat ID[/]")
            return

        # Allow prefix matching of conversation IDs
        matching_sessions = [
            s for s in self.sessions.keys() if s.startswith(session_id)
        ]

        if len(matching_sessions) == 0:
            self.console.print(f"[red]No session found starting with {session_id}[/]")
        elif len(matching_sessions) > 1:
            self.console.print(
                f"[red]Multiple sessions found starting with {session_id}[/]"
            )
        else:
            self.current_session = self.sessions[matching_sessions[0]]
            self.update_provider()
            self.console.print(
                f"[bold green]Switched to session:[/] ({self.current_session.title}) {self.current_session.id}"
            )

    def send(self, message):
        "Send a message in the current session: <message>"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        if not message:
            self.console.print("[red]Provide a message to send[/]")
            return

        # if either model or api key are not set, a provider cannot be created
        if not self.provider:
            self.console.print(
                "[red]Model and api key are required for sending. Check current settings[/]"
            )
            return

        self.current_session.add_message("user", message)

        # TODO: don't like having to repeat this to get the config of the current session
        settings = self.current_session.settings
        config = self.config_manager.get_config(settings)

        # call LLM
        # TODO: if this fails due to a bad request, the user message is still added to the history
        # conversations should always alternate between user and assistant
        response = self.provider.send(config, self.current_session.history)
        full_response = self.stream_response(response)

        self.current_session.add_message("assistant", full_response)

    def stream_response(self, response) -> str:
        "Stream the response from the provider"

        # TODO repeated again
        settings = self.current_session.settings
        config = self.config_manager.get_config(settings)

        full_response = ""
        if config["api_type"] == "openai":
            for chunk in response:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        content = delta.content
                        full_response += content
                        print(content, end="", flush=True)
                    if chunk.choices[0].finish_reason:
                        print()
                        break
        elif config["api_type"] == "anthropic":
            for chunk in response:
                if chunk.type == "content_block_delta":
                    content = chunk.delta.text
                    full_response += content
                    print(content, end="", flush=True)
                elif chunk.type == "message_stop":
                    print()
                    break

        return full_response

    def history(self, arg):
        "Show message history for the active session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        if not self.current_session.history:
            self.console.print("[red]Current session is empty.[/]")
            return

        history_text = ""
        for msg in self.current_session.history:
            content = msg.content.strip()

            if msg.role == "user":
                history_text += f"\n[[yellow]{msg.role.upper()}[/]]\n\n{content}\n"
            elif msg.role == "assistant":
                history_text += f"\n[[bold blue]{msg.role.upper()}[/]]\n\n{content}\n"
            else:
                continue

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

    def tokens(self, arg):
        "Show token usage for the current session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        self.console.print(
            f"Total session tokens: {self.current_session.get_token_count()}"
        )

    def delete(self, arg):
        "Delete a session: /delete <session_id>"
        if not arg:
            self.console.print("[red]Please provide a valid chat ID[/]")
            return

        if arg not in self.sessions:
            self.console.print(f"[red]No chat found with ID: {arg}[/]")
            return

        file_path = HISTORY_PATH / f"{arg}.json"
        if file_path.exists():
            # double check
            confirm = input(f"Are you sure you want to delete chat: {arg}? (y/n): ")
            if confirm.lower() != "y":
                self.console.print("[red]Deletion cancelled[/]")
                return

            # delete the file
            file_path.unlink()

            del self.sessions[arg]

            if self.current_session and self.current_session.id == arg:
                self.current_session = None

            self.console.print(f"[bold green]Deleted chat: {arg}[/]")

    def branch(self, arg):
        "Create a new branch from the current session"
        if not self.current_session:
            self.console.print(
                "[red]You're not in a session. Start one with 'new' or switch to an existing one with 'switch'[/]"
            )
            return

        # create a new session with the same metadata as the current session
        branch_session = Session()
        branch_session.title = self.current_session.title + " (branch)"
        branch_session.branched_from = self.current_session.id
        branch_session.settings = self.current_session.settings
        branch_session.history = self.current_session.history
        branch_session.save_history()

        self.sessions[branch_session.id] = branch_session
        self.current_session = branch_session
        self.console.print(f"[bold green]Created branch: {branch_session.id}[/]")

    def handle_input(self, user_input: str) -> None:
        if not user_input:
            return

        # Handle commands
        # Slash commands cannot be used in multiline mode
        # Multiline mode is started and stopped with triple quotes,
        #   then the buffer is sent as a message
        if user_input.startswith("/") and not self.multiline_mode:
            command, *args = user_input[1:].split(" ")
            if command in self.commands:
                self.commands[command](" ".join(args))
            else:
                self.console.print(f"[red]Unknown command: {command}[/]")
        elif user_input.startswith('"""') and not self.multiline_mode:
            self.multiline_mode = True
            self.multiline_buffer = []
            # Check for input on the same line as the starting triple quotes
            user_input = user_input[3:].strip()
            if user_input:
                self.multiline_buffer.append(user_input)

        elif self.multiline_mode:
            if user_input.endswith('"""'):
                self.multiline_mode = False
                # Check for input on the same line as the ending triple quotes
                user_input = user_input[:-3].strip()
                if user_input:
                    self.multiline_buffer.append(user_input)
                multiline_input = "\n".join(self.multiline_buffer)
                print(multiline_input)
                if multiline_input:
                    self.send(multiline_input)
                self.multiline_buffer = []
            else:
                self.multiline_buffer.append(user_input)
        else:
            self.send(user_input)

    def run(self):
        "Start the chat CLI"

        self.console.print("[bold green]Welcome to Ellm![/]")
        self.console.print("[bold]Type /help for a list of commands[/]")

        while self.running:
            try:
                prompt = "... " if self.multiline_mode else ">>> "
                user_input = self.console.input(prompt)
                self.handle_input(user_input)
            except KeyboardInterrupt:
                self.quit()
            except EOFError:
                self.quit()

    def quit(self, arg):
        "Exit the chat CLI"
        self.console.print("[green]Goodbye![/]")
        self.running = False

    def help(self, arg):
        "Show available commands"
        self.console.print("Available commands:")
        for command, func in self.commands.items():
            self.console.print(f" - /{command}: {func.__doc__}")

        self.console.print("")
        self.console.print('Use """ to start and stop multiline mode')
        self.console.print("")
