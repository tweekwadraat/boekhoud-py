from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer
from app.ui.journal_entries.journal_entry_header import JournalEntryHeader

class JournalEntriesScreen(Screen):
    BINDINGS = [("f9", "next", "Volgende boeking"), ("f10", "previous", "Vorige boeking"), ("escape", "back", "Terug")]
    
    def compose(self) -> ComposeResult:
        yield JournalEntryHeader()

        footer = Footer()
        footer.show_command_palette = False
        yield footer

    def action_next(self) -> None:
        pass

    def action_previous(self) -> None:
        pass

    def action_back(self) -> None:
        self.app.pop_screen()