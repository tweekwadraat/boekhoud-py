from textual.widget import Widget
from textual.app import ComposeResult


class JournalEntryLines(Widget):
    """Journal entry line.
    
    Shows GL-account, if applicable relations field, if applicable project field, description and amount.
    """
    
    def compose(self) -> ComposeResult:
        # Content follows in future step
        return
        yield  # onbereikbaar, maar maakt de functie een generator