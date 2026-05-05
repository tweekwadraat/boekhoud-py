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
        """Open een Input-widget over de huidige cel met het ingetypte teken al erin."""
        table = self.query_one(DataTable)

        editor = Input(value=starting_text, compact=True)
        self._editing_input = editor
        self.mount(editor)

        # Positioneer de Input over de actieve cel
        self._position_editor_over_current_cell(editor, table)

        editor.focus()
        self.call_after_refresh(self._reset_editor_cursor)

    def _reset_editor_cursor(self) -> None:
        """Cursor naar einde, selectie opheffen — uitgevoerd na het focusen
        zodat Textual's standaard 'selecteer-bij-focus' al gebeurd is."""
        editor = self._editing_input
        if editor is None:
            return
        editor.action_end()
    
    def _position_editor_over_current_cell(
        self, editor: Input, table: DataTable
    ) -> None:
        """Bereken positie en breedte van de actieve cel en zet Input daar neer.

        Patroon overgenomen uit Textual Discussion #2449 (freylax, jan 2026).
        Werkt door de positie samen te stellen uit padding, header-hoogte en
        kolombreedtes vóór de actieve kolom.
        """
        cursor = table.cursor_coordinate

        # x-positie: padding links + breedte van alle kolommen vóór de actieve
        x = table.cell_padding
        width = 0
        for index, column in enumerate(table.ordered_columns):
            if index < cursor.column:
                x += column.get_render_width(table)
            else:
                width = column.get_render_width(table)
                break

        # y-positie: onder de header + de rij waar we op staan
        y = table.header_height + cursor.row

        # Compenseer voor positie van de tabel binnen het scherm en scrollen
        content_offset = table.content_offset
        scroll_offset = table.scroll_offset
        x += content_offset.x - scroll_offset.x
        y += content_offset.y - scroll_offset.y

        editor.styles.position = 'absolute'
        editor.styles.offset = (x, y)
        editor.styles.width = width

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