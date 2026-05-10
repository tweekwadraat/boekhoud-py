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
    # Kolommen die niet leeg achtergelaten mogen worden bij Enter-doorgang.
    # 0 = GBnr, 3 = Bedrag — beide bepalend voor saldo en boekhoudregel.
    REQUIRED_COLUMNS = {0, 3}
    LAST_COLUMN = 3

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
        
        if event.key == 'enter':
            event.stop()
            event.prevent_default()
            self._advance_to_next_field(table.cursor_row, table.cursor_column)

        elif event.key == 'up':
            if not self._is_row_complete(table, table.cursor_row) or table.cursor_row == 0:
                event.stop()
                event.prevent_default()

        elif event.key == 'down':
            if not self._is_row_complete(table, table.cursor_row) or table.cursor_row == table.row_count - 1:
                event.stop()
                event.prevent_default()

        elif event.key in ('left', 'right'):
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
        self._advance_to_next_field(table.cursor_row, table.cursor_column)

    def _advance_to_next_field(self, row: int, column: int) -> None:
        """Verspringt naar het volgende invoerveld in de Enter-keten.

        Op kolom 0–2: cursor één kolom naar rechts in dezelfde rij.
        Op kolom 3 (Bedrag): cursor naar kolom 0 van de volgende rij; als
        de huidige rij de laatste is, wordt eerst een lege rij toegevoegd.

        Wanneer de huidige cel verplicht is (kolom 0 of 3) en leeg, blokkeert
        de versprong stilzwijgend — de cursor blijft staan.
        """
        table = self.query_one(DataTable)

        # Fase 1: bewaking — verplichte cel mag niet leeg zijn
        if column in self.REQUIRED_COLUMNS:
            value = table.get_cell_at(Coordinate(row, column))
            if not value.strip():
                return

        # Fase 2: versprong
        if column == self.LAST_COLUMN:
            if row == table.row_count - 1:
                self._append_empty_row_and_move_cursor()
            else:
                table.cursor_coordinate = Coordinate(row + 1, 0)
        else:
            table.cursor_coordinate = Coordinate(row, column + 1)


    def _append_empty_row_and_move_cursor(self) -> None:
        """Voegt onderaan een lege rij toe en zet de cursor op (laatste rij, 0)."""
        table = self.query_one(DataTable)
        table.add_row("", "", "", "")
        table.cursor_coordinate = Coordinate(table.row_count - 1, 0)
        
    def _is_row_complete(self, table: DataTable, row: int) -> bool:
        """Geeft true terug als verplichte velden niet leeg zijn"""
        for column in self.REQUIRED_COLUMNS:
            coordinate = Coordinate(row, column)
            value = table.get_cell_at(coordinate)
            if not value.strip():
                return False
        return True

    def _close_editor(self) -> None:
        """Sluit de Input weer, focus terug naar de tabel."""
        if self._editing_input is not None:
            self._editing_input.remove()
            self._editing_input = None
        self.query_one(DataTable).focus()