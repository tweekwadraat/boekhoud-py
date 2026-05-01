from textual.widget import Widget
from textual.app import ComposeResult


class JournalEntryHeader(Widget):
    """Header of Journal Entries Screen.
    
    Shows diary, date, bookingsnumber, main relation, description and
    the balance of the current journal entry.
    """
    
    def compose(self) -> ComposeResult:
        # Content follows in future step
        return
        yield  # onbereikbaar, maar maakt de functie een generator