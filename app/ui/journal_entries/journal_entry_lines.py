from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import DataTable, Input
from textual import events
from textual.coordinate import Coordinate


class JournalEntryLines(Widget):
    """Lines of one journal entry,
    shown on the journal entries screen.

    Shows GL-account, description, relation (only for D/C-accounts) and amount.
    """

    def __init__(self) -> None:
        super().__init__()
        # Houdt bij of er nu een Input openstaat. None = geen edit actief.
        self._editing_input: Input | None = None

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns('Grootboeknr.', 'Relatie', 'Omschrijving', 'Bedrag')
        table.add_row('1300', '1001', 'Factuur April diensten', '121.00')
        table.add_row('8000', '', 'Factuur April diensten', '-100.00')
        table.add_row('1500', '', 'Factuur April diensten', '-21.00')

    def on_key(self, event: events.Key) -> None:
        table = self.query_one(DataTable)

        # Tijdens een edit-sessie alleen Esc afhandelen, rest aan Input overlaten
        if self._editing_input is not None:
            if event.key == 'escape':
                event.stop()
                event.prevent_default()
                self._close_editor()
            return

        if event.key == 'up' and table.cursor_row == 0:
            event.stop()
            event.prevent_default()

        elif event.key == 'down' and table.cursor_row == table.row_count - 1:
            event.stop()
            event.prevent_default()

        # Een normaal teken (letter, cijfer, punt, etc.) → open Input
        elif event.character is not None and event.character.isprintable():
            event.stop()
            event.prevent_default()
            self._open_editor(starting_text=event.character)

    def _open_editor(self, starting_text: str) -> None:
        """Open een Input-widget met het ingetypte teken al erin."""
        editor = Input(value=starting_text)
        self._editing_input = editor
        self.mount(editor)
        editor.focus()
        # Zet cursor aan het einde, zodat verder typen netjes erachter gebeurt
        editor.cursor_position = len(starting_text)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Enter in de Input → waarde opslaan in de cel en Input sluiten."""
        table = self.query_one(DataTable)
        coordinate = Coordinate(table.cursor_row, table.cursor_column)
        table.update_cell_at(coordinate, event.value)
        self._close_editor()

    def _close_editor(self) -> None:
        """Sluit de Input weer, focus terug naar de tabel."""
        if self._editing_input is not None:
            self._editing_input.remove()
            self._editing_input = None
        self.query_one(DataTable).focus()