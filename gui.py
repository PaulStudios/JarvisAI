# skipcq
"""
GUI Handler
"""

import logging
import sys

from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Placeholder

from handler.utilities import resource_path

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
        with Vertical(classes="chatscreen", id="chatscreen"):
            yield Static("Chat", classes="box", id="Chat")
            yield Horizontal(Static("Input", id="input-text"),
                             Button("Send", id="send", name="Send"),
                             classes="input",
                             id="inputarea")
        yield Footer()
        yield Header()


class JarvisGui(App[None]):
    """GUI Core"""

    TITLE = "JarvisAI"
    SUB_TITLE = "Your personal AI Assistant"
    CSS_PATH = resource_path("gui.tcss")
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
        yield Placeholder()

    def action_quit(self) -> None:  # skipcq: PYL-W0236
        """Quit"""
        LOGGER.info("Exiting...")
        sys.exit(0)

    def on_mount(self) -> None:
        """On running the gui"""
        LOGGER.info("Starting GUI")
        self.switch_mode("chat")


app = JarvisGui()
app.run()
