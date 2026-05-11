from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, DataTable
from app.ui.journal_entries.journal_entry_header import JournalEntryHeader
from app.ui.journal_entries.journal_entry_lines import JournalEntryLines
from decimal import Decimal


class JournalEntriesScreen(Screen):
    BINDINGS = [("f9", "next", "Volgende boeking"), ("f10", "previous", "Vorige boeking"), ("escape", "back", "Terug")]
    
    def compose(self) -> ComposeResult:
        yield JournalEntryHeader()

        yield JournalEntryLines()

        footer = Footer()
        footer.show_command_palette = False
        yield footer

    def on_mount(self) -> None:
        self.query_one(JournalEntryHeader).focus_first_field()

    def action_next(self) -> None:
        pass

    def action_previous(self) -> None:
        pass

    def action_back(self) -> None:
        self.app.pop_screen()

    def on_journal_entry_header_completed(self, event: JournalEntryHeader.Completed) -> None:
        """Move focus from header to the lines zone when header is filled in."""
        self.query_one(DataTable).focus()
    
    def on_journal_entry_header_cancelled(self, event: JournalEntryHeader.Cancelled) -> None:
        """Return to the menu when the user pressed Esc on the first header field."""
        self.action_back()

    def on_journal_entry_lines_back_to_header(self, event: JournalEntryLines.BackToHeader) -> None:
        """Handle Esc from the lines zone: return to header if balanced, else show modal"""
        if event.balance == Decimal('0'):
            self.query_one(JournalEntryHeader).focus_last_field()
        else:
            self.notify(f'TODO modal — saldo is {event.balance}')
    
    def on_journal_entry_lines_balance_changed(self, event: JournalEntryLines.BalanceChanged) -> None:
        """Update the hader with the new balance."""
        self.query_one(JournalEntryHeader).update_balance(event.balance)
