from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import DataTable


class JournalEntryLines(Widget):
    """Lines of one journal entry,
    shown on the journal entries screen. 
    
    Shows GL-account, description, relation (only for D/C-accounts) and amount.
    """
    
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns('Grootboeknr.', 'Relatie', 'Omschrijving', 'Bedrag')
        table.add_row('1300', '1001', 'Factuur April diensten', '121.00')
        table.add_row('8000', '', 'Factuur April diensten', '-100.00')
        table.add_row('1500', '', 'Factuur April diensten', '-21.00')