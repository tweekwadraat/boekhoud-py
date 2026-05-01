from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class JournalEntryHeader(Widget):
    """Header of one journal entry, shown on the journal entries screen.
    
    Shows diary, bookingsnumber, date, description and
    the balance of the current journal entry.
    """
    
    DEFAULT_CSS = """
    JournalEntryHeader {
        height: auto;
    }
    JournalEntryHeader Horizontal {
        height: auto;
    }
    JournalEntryHeader Horizontal Static.balance {
        width: 1fr;
        text-align: right;
    }
    JournalEntryHeader Horizontal Static {
        width: auto;
    }
    """

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static('Dagboek      : VER1')
            yield Static('Saldo: 0.00', classes='balance')
        yield Static('Boekstuknr   : 2026-0042')
        yield Static('Datum        : 15-04-2026')
        yield Static('Omschrijving : Factuur april diensten')
