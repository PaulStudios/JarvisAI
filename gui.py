import logging
import sys

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button


LOGGER = logging.getLogger("JarvisAI.GUI")


class ProfileScreen(Screen):
    """Profile Management"""

    def compose(self) -> ComposeResult:
        """Internal compose"""
        yield Static("Profile")
        yield Footer()
        yield Header()


class HelpScreen(Screen):
    """Display commands"""

    def compose(self) -> ComposeResult:
        """Internal compose"""
        yield Static("Help")
        yield Footer()
        yield Header()


class ChatScreen(Screen):
    """Main chat interface"""

    def compose(self) -> ComposeResult:
        """Internal compose"""
        yield Static("One", classes="box", id="profile")
        yield Static("Chat", classes="box", id="Chat")
        yield Static("Input", classes="box", id="input")
        yield Button("Send", id="send", name="Send")
        yield Footer()
        yield Header()


class JarvisGui(App[None]):
    """GUI Core"""

    TITLE = "JarvisAI"
    SUB_TITLE = "Your personal AI Assistant"
    CSS_PATH = "gui.tcss"
    USER = ""
    BINDINGS = [("escape", "quit()", "QUIT")]
    MODES = {
        "profile": ProfileScreen,
        "chat": ChatScreen,
        "help": HelpScreen,
    }
    LOGGER.info("Setting up Interface")

    def compose(self) -> ComposeResult:
        """Internal compose"""
        yield Header()
        yield Footer()

    def action_quit(self) -> None:
        """Quit"""
        LOGGER.info("Exiting...")
        sys.exit(0)

    def on_mount(self) -> None:
        """On running the gui"""
        LOGGER.info("Starting GUI")
        self.switch_mode("chat")
