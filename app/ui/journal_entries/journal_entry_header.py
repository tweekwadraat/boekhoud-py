from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Static, Input, Label


class JournalEntryHeader(Widget):
    """Header of one journal entry, shown on the journal entries screen.
    
    Shows diary, bookingsnumber, date, description and
    the balance of the current journal entry.
    """
    
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
    """

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label('Dagboek      :')
            yield Input(value='VER1', id='diary')
            yield Static('Saldo: 0.00', classes='balance')
        with HorizontalGroup():
            yield Label('Boekstuknr   :')
            yield Input(value='2026-0042', id='entry_number')
        with HorizontalGroup():
            yield Label('Datum        :')
            yield Input(value='15-04-2026', id='date')
        with HorizontalGroup():
            yield Label('Omschrijving :')
            yield Input(value='Factuur april diensten', id='description')
