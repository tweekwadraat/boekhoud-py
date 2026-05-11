from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Static, Input, Label
from textual.message import Message
from decimal import Decimal

class EscapableInput(Input):
    """An Input that posts an EscapePressed message when Esc is pressed."""

    BINDINGS = [('escape', 'back', 'Terug')]

    class EscapePressed(Message):
        """Posted when Esc is pressed on this input."""
        def __init__(self, input_id: str) -> None:
            super().__init__()
            self.input_id = input_id

    def action_back(self) -> None:
        """Post EscapePressed so a parent widget can act on it."""
        self.post_message(self.EscapePressed(self.id))


class JournalEntryHeader(Widget):
    """Header of one journal entry, shown on the journal entries screen.
    
    Shows diary, bookingsnumber, date, description and
    the balance of the current journal entry.
    """
    
    FIELD_ORDER = ['diary', 'entry_number', 'date', 'description']

    DEFAULT_CSS = """
    JournalEntryHeader {
        height: auto;
    }
    
    JournalEntryHeader HorizontalGroup Static.balance {
        width: 1fr;
        text-align: right;
    }
    
    JournalEntryHeader HorizontalGroup Static {
        width: auto;
    }

    JournalEntryHeader Input {
        border: none;
        height: 1;
        width: 30;
    }

    JournalEntryHeader Input:focus {
        border: none;
        height: 1;
    }

    JournalEntryHeader Static.out-of-balance {
        text-style: reverse;
    }
    """

    class Completed(Message):
        """Posted when the user pressed Enter on the last header field."""

    class Cancelled(Message):
        """Posted when the user pressed Esc on the first header field."""

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label('Dagboek      :')
            yield EscapableInput(value='VER1', id='diary')
            yield Static('Saldo: 0.00', classes='balance', id='balance')
        with HorizontalGroup():
            yield Label('Boekstuknr   :')
            yield EscapableInput(value='2026-0042', id='entry_number')
        with HorizontalGroup():
            yield Label('Datum        :')
            yield EscapableInput(value='15-04-2026', id='date')
        with HorizontalGroup():
            yield Label('Omschrijving :')
            yield EscapableInput(value='Factuur april diensten', id='description')

    def focus_first_field(self) -> None:
        '''Focus the diary input - the first field a user fills in for a new entry.'''
        self.query_one('#diary', EscapableInput).focus()

    def focus_last_field(self) -> None:
        """Focus the description input — used when returning from the lines zone."""
        self.query_one('#description', EscapableInput).focus()

    def update_balance(self, balance: Decimal) -> None:
        """Update the balance display with the given value."""
        balance_widget = self.query_one('#balance', Static)
        balance_widget.update(f'Saldo: {balance:.2f}')
        balance_widget.set_class(balance != Decimal('0'), 'out-of-balance')

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Move focus to the next header field when Enter is pressed."""
        field_id = event.input.id
        current_index = self.FIELD_ORDER.index(field_id)
        next_index = current_index + 1
        if next_index < len(self.FIELD_ORDER):
            next_id = self.FIELD_ORDER[next_index]
            self.query_one(f'#{next_id}', EscapableInput).focus()
        else:
            self.post_message(self.Completed())

    def on_escapable_input_escape_pressed(self, event: EscapableInput.EscapePressed) -> None:
        """Move focus to the previous header field when Esc is pressed."""
        field_id = event.input_id
        current_index = self.FIELD_ORDER.index(field_id)
        if current_index > 0:
            previous_id = self.FIELD_ORDER[current_index - 1]
            self.query_one(f'#{previous_id}', EscapableInput).focus()
        else:
            self.post_message(self.Cancelled())





