# skipcq
"""
GUI Handler
"""

import sys
import textwrap

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Static, Button, Placeholder, Input, Markdown

from chatbot import Bot
from handler.logger import Logger, initlogs
from handler.utilities import print_custom
from handler.utilities import resource_path, correction

LOGGER: Logger = Logger("JarvisAI.gui")
wrapper = textwrap.TextWrapper(width=60)
initlogs()
bot: Bot = Bot()
USER = ()
mode_options = {"profile": 'open profile menu', "help": 'open help screen'}


class ProfileScreen(Screen):
    """Profile Management"""

    def compose(self) -> ComposeResult:  # skipcq: PYL-R0201
        """Internal compose"""
        profile_data = f"""\
        ::Profile Information::
        
        Name: {USER[0]}
        Username: {USER[1]}
        Country: {USER[2]}
        Email: {USER[3]}
        Password: {USER[4]}
        """
        with Vertical(classes="infoscreen", id="infoscreen"):
            with FocusableContainer(id="conversation_box"):
                yield MessageBox(
                    "Welcome to Profile Management!\n"
                    "See you account details below\n"
                    "Type '{Field Name} - {New Value}'\n"
                    "Example : Name - John Doe",
                    role="Info",
                )
            yield Markdown(profile_data, id="profile_info")
            with Horizontal(id="edit_box"):
                yield Input(placeholder="Enter your Edit",
                            id="edit_input")
                yield Button(label="Submit", variant="success", id="send_edit")
        yield Footer()
        yield Header(show_clock=True)

    async def on_button_pressed(self) -> None:
        """Process when send was pressed."""
        await self.process_edit()

    async def on_input_submitted(self) -> None:
        """Process when input was submitted."""
        await self.process_edit()

    async def process_edit(self) -> None:
        """Editing"""
        message_input = self.query_one("#edit_input", Input)
        # Don't do anything if input is empty
        if message_input.value == "":
            return
        button = self.query_one("#send_edit")

        toggle_widgets(message_input, button)




class HelpScreen(Screen):
    """Display commands"""

    def compose(self) -> ComposeResult:  # skipcq: PYL-R0201
        """Internal compose"""
        yield Placeholder("Help")
        yield Footer()
        yield Header()


class FocusableContainer(ScrollableContainer, can_focus=True):
    """Focusable container widget."""


class MessageBox(Widget, can_focus=True):
    """Box widget for the message."""

    def __init__(self, text: str, role: str) -> None:
        self.text = text
        self.role = role
        super().__init__()

    def compose(self) -> ComposeResult:
        """Yield message component."""
        yield Static(self.text, classes=f"message {self.role}")


def toggle_widgets(*widgets: Widget) -> None:
    """Toggle a list of widgets."""
    for w in widgets:
        w.disabled = not w.disabled


class ChatScreen(Screen):
    """Main chat interface"""

    def compose(self) -> ComposeResult:  # skipcq: PYL-R0201
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
                yield Input(placeholder="Enter your message",
                            id="message_input")
                yield Button(label="Send", variant="success", id="send_button")
        yield Footer()
        yield Header(show_clock=True)

    def on_mount(self):
        """On run"""
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

        toggle_widgets(message_input, button)

        # Create question message, add it to the conversation and scroll down
        message_input.value = correction(message_input.value)
        q = USER[1] + ": " + message_input.value
        string = wrapper.fill(text=q)
        message_box = MessageBox(string, "question")
        await conversation_box.mount(message_box)
        conversation_box.scroll_end(animate=True)
        msg = message_input.value

        # Clean up the input without triggering events
        with message_input.prevent(Input.Changed):
            message_input.value = ""

        # Take answer from the chat and add it to the conversation
        ans = "JarvisAI: " + bot.process(msg)
        string = wrapper.fill(text=ans)
        await conversation_box.mount(MessageBox(
            string,
            "answer",
        ))

        toggle_widgets(message_input, button)
        # For some reason single scroll doesn't work
        conversation_box.scroll_end(animate=True)
        conversation_box.scroll_end(animate=True)
        self.query_one(Input).focus()
        if msg.lower() == "ct_profile":
            await self.app.switch_mode("profile")


class JarvisGui(App[None]):
    """GUI Core"""

    TITLE = "JarvisAI"
    SUB_TITLE = "Your personal AI Assistant"
    CSS_PATH = resource_path("gui.tcss")
    BINDINGS = [("escape", "quit()", "QUIT")]
    MODES = {
        "profile": ProfileScreen,
        "chat": ChatScreen,
        "help": HelpScreen,
    }
    LOGGER.info("Setting up GUI Interface")

    def compose(self) -> ComposeResult:  # skipcq: PYL-R0201
        """Internal compose"""
        yield Placeholder()

    def action_quit(self) -> None:  # skipcq: PYL-W0236, PYL-R0201
        """Quit"""
        LOGGER.info("Exiting...")
        Exit()

    def on_mount(self) -> None:
        """On running the gui"""
        LOGGER.info("Starting GUI")
        #self.switch_mode("chat")
        self.switch_mode("profile")


def Exit():
    """Exit"""
    print("\n")
    print_custom("Goodbye", "bright_red")
    sys.exit()
