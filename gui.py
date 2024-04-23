# skipcq
"""
GUI Handler
"""

import sys
import textwrap

from pymsgbox import prompt, password, confirm
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, ScrollableContainer
from textual.screen import Screen
from textual.validation import ValidationResult, Validator
from textual.widget import Widget
from textual.widgets import Header, Footer, Static, Button, Placeholder, Input, Markdown, Pretty

from chatbot import Bot
from handler.logger import Logger, initlogs
from handler.utilities import print_custom, get_field_index, checkmail, countries_exist
from handler.utilities import resource_path, correction
from user import process_edits

LOGGER: Logger = Logger("JarvisAI.gui")
wrapper = textwrap.TextWrapper(width=60)
initlogs()
bot: Bot = Bot()
USER = ()
edited_user = {}
_edit_list = {}
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
                    "Example : Name - John Doe\n"
                    "Type 'OK' to save your changes. "
                    "Type 'CANCEL' to go back without saving.",
                    role="Info",
                )
            yield Pretty("All OK")
            yield Markdown(profile_data, id="profile_info")
            with Horizontal(id="edit_box"):
                yield Input(placeholder="Enter your Edit",
                            id="edit_input",
                            validators=[edit_input_check()],
                            validate_on=["changed", "submitted"])
                yield Button(label="Submit", variant="success", id="send_edit")
        yield Footer()
        yield Header(show_clock=True)

    async def on_button_pressed(self) -> None:
        """Process when send was pressed."""
        await self.process_edit()

    async def on_input_submitted(self) -> None:
        """Process when input was submitted."""
        await self.process_edit()

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        """Updating the UI to show the reasons why validation failed"""
        if not event.validation_result.is_valid:
            self.query_one(Pretty).update(
                event.validation_result.failure_descriptions)
            self.query_one("#send_edit").disabled = True
        else:
            self.query_one(Pretty).update("All OK")
            self.query_one("#send_edit").disabled = False

    def on_mount(self):
        """On run"""
        self.query_one(Input).focus()

    async def process_edit(self) -> None:
        """Editing Process"""
        global edited_user, _edit_list
        edit_input = self.query_one("#edit_input", Input)
        button = self.query_one("#send_edit")

        if edit_input.value == "CANCEL":
            await self.app.switch_mode("chat")
        if edit_input.value == "OK":
            toggle_widgets(edit_input, button)
            process_edits(_edit_list)
            toggle_widgets(edit_input, button)
            await self.app.switch_mode("chat")

        # Don't do anything if input is empty or invalid
        if edit_input.value == "" or " - " not in edit_input.value:
            return
        try:
            get_field_index(edit_input.value.split(" - ")[0])
        except AttributeError:
            return

        info_box = self.query_one("#profile_info")
        field = edit_input.value.split(" - ")[0]
        field_data = edit_input.value.split(" - ")[1]
        field_index = get_field_index(field)

        if field_index == 3 and not checkmail(field_data):
            self.query_one(Pretty).update("Invalid Email entered...")
            toggle_widgets(edit_input, button)
            self.query_one(Input).focus()
            return
        if field_index == 0:
            if " " not in field_data:
                self.query_one(Pretty).update(
                    "Invalid Name Entered. Please enter your full name.")
                toggle_widgets(edit_input, button)
                self.query_one(Input).focus()
                return
            if len(field_data.split(" ")[0]) < 3 or len(
                    field_data.split(" ")[1]) < 3:
                self.query_one(Pretty).update(
                    "Invalid Name Entered. Please enter your full name.")
                toggle_widgets(edit_input, button)
                self.query_one(Input).focus()
                return
        if field_index == 2 and not countries_exist(field_data):
            self.query_one(Pretty).update(
                "Invalid Country Entered. Please check the spelling.")
            toggle_widgets(edit_input, button)
            self.query_one(Input).focus()
            return
        if field_index == 4:
            if len(field_data) <= 8 or " " in field_data:
                self.query_one(Pretty).update(
                    "Invalid Password Entered. It should contain 8 characters. No whitespaces are allowed."
                )
                toggle_widgets(edit_input, button)
                self.query_one(Input).focus()
                return
            conf = password("Please re-enter your new password",
                            title="Confirm New Password")
            if not conf == field_data:
                self.query_one(Pretty).update(
                    "Passwords did not match. Please try again")
                toggle_widgets(edit_input, button)
                with edit_input.prevent(Input.Changed):
                    edit_input.value = ""
                self.query_one(Input).focus()
                return

        _edit_list.update({field_index: field_data})
        edit = {0: USER[0], 1: USER[1], 2: USER[2], 3: USER[3], 4: USER[4]}
        if not edited_user == {}:
            edit = edited_user
        if field_index == 4:
            f = field_data
            field_data = ""
            for i in f:
                field_data = field_data + "*"
        if field_index == 3:
            full = field_data.split("@")
            f = full[0]
            field_data = ""
            for i in f:
                field_data = field_data + "*"
            field_data = field_data + "@" + full[1]
        field_data_edited = field_data + "  [Changed]"
        self.query_one(Pretty).update(["All OK"])
        edit.update({field_index: field_data_edited})

        q = f"""\
        ::Profile Information::
        
        Name: {edit[0]}
        Username: {edit[1]}
        Country: {edit[2]}
        Email: {edit[3]}
        Password: {edit[4]}
        """
        info_box.update(q)
        edited_user = edit

        # Clean up the input without triggering events
        with edit_input.prevent(Input.Changed):
            edit_input.value = ""
        toggle_widgets(edit_input, button)
        self.query_one(Input).focus()


class edit_input_check(Validator):
    """Validator"""

    def validate(self, value: str) -> ValidationResult:
        """Check if input is following format"""
        if value in ["OK", "CANCEL"]:
            return self.success()

        a1, a2 = 0, 0
        f = ""
        if self.is_syntax(value):
            a1 = 1
            if self.field_exists(value):
                a2 = 1
            else:
                f = f + "Please provide a valid Field"
                a2 = 0
        else:
            f = "Please follow the format..."
            a1 = 0
            a2 = 0
        if a1 == 1 and a2 == 1:
            return self.success()
        return self.failure(f)

    @staticmethod
    def is_syntax(value: str) -> bool:
        """Validates syntax"""
        if " - " in value:
            return True
        return False

    @staticmethod
    def field_exists(value: str) -> bool:
        """Validates field"""
        c = get_field_index(value.split(" - ")[0])
        if c == 10:
            return False
        return True


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
        # self.switch_mode("chat")
        self.switch_mode("profile")


def Exit():
    """Exit"""
    print("\n")
    print_custom("Goodbye", "bright_red")
    LOGGER.warning("Shutting Down...")
    sys.exit(0)
