# skipcq
"""
GUI Handler
"""

import logging
import sys
import textwrap

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Static, Button, Placeholder, Input

from handler.utilities import resource_path

LOGGER = logging.getLogger("JarvisAI.GUI")
wrapper = textwrap.TextWrapper(width=60)


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


class FocusableContainer(ScrollableContainer, can_focus=True):
    """Focusable container widget."""


class MessageBox(Widget, can_focus=True):
    """Box widget for the message."""

    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        self.msg = self.role + ": " + self.text
        if self.role == "Info":
            self.msg = self.text
        super().__init__()

    def compose(self) -> ComposeResult:
        """Yield message component."""
        yield Static(self.msg, classes=f"message {self.role}")


class ChatScreen(Screen):
    """Main chat interface"""

    def compose(self) -> ComposeResult:
        """Internal compose"""
        with Vertical(classes="chatscreen", id="chatscreen"):
            with FocusableContainer(id="conversation_box"):
                yield MessageBox(
                    "Welcome to JarvisAI v3.0!\n"
                    "Type your question, click enter or 'send' button "
                    "and wait for the response.",
                    role="Info",
                )
            with Horizontal(id="input_box"):
                yield Input(placeholder="Enter your message", id="message_input")
                yield Button(label="Send", variant="success", id="send_button")
        yield Footer()
        yield Header(show_clock=True)

    def on_mount(self):
        self.query_one(Input).focus()

    def action_clear(self) -> None:
        """Clear the conversation and reset widgets."""
        conversation_box = self.query_one("#conversation_box")
        conversation_box.remove()
        self.mount(FocusableContainer(id="conversation_box"))

    async def on_button_pressed(self) -> None:
        """Process when send was pressed."""
        await self.process_conversation()

    async def on_input_submitted(self) -> None:
        """Process when input was submitted."""
        await self.process_conversation()

    async def process_conversation(self) -> None:
        """Process a single question/answer in conversation."""
        message_input = self.query_one("#message_input", Input)
        # Don't do anything if input is empty
        if message_input.value == "":
            return
        button = self.query_one("#send_button")
        conversation_box = self.query_one("#conversation_box")

        self.toggle_widgets(message_input, button)

        # Create question message, add it to the conversation and scroll down
        string = wrapper.fill(text=message_input.value)
        message_box = MessageBox(string, "question")
        await conversation_box.mount(message_box)
        conversation_box.scroll_end(animate=True)

        # Clean up the input without triggering events
        with message_input.prevent(Input.Changed):
            message_input.value = ""

        # Take answer from the chat and add it to the conversation
        c = "Test"
        await conversation_box.mount(MessageBox(c, "answer", ))

        self.toggle_widgets(message_input, button)
        # For some reason single scroll doesn't work
        conversation_box.scroll_end(animate=True)
        conversation_box.scroll_end(animate=True)
        self.query_one(Input).focus()

    def toggle_widgets(self, *widgets: Widget) -> None:
        """Toggle a list of widgets."""
        for w in widgets:
            w.disabled = not w.disabled


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
