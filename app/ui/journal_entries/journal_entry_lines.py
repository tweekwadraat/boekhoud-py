from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import DataTable, Input
from textual import events
from textual.coordinate import Coordinate
from textual.message import Message
from decimal import Decimal, InvalidOperation
from rich.text import Text

class JournalEntryLines(Widget):
    """Lines of one journal entry,
    shown on the journal entries screen.

    Shows GL-account, description, relation (only for D/C-accounts) and amount.
    """
    # Kolommen die niet leeg achtergelaten mogen worden bij Enter-doorgang.
    # 0 = GBnr, 3 = Bedrag — beide bepalend voor saldo en boekhoudregel.
    REQUIRED_COLUMNS = {0, 3}
    LAST_COLUMN = 3

    class BackToHeader(Message):
        """Posted when the user presses Esc on column 0 of a non-half row."""
        def __init__(self, balance: Decimal) -> None:
            super().__init__()
            self.balance = balance

    class BalanceChanged(Message):
        """Posted when the balance of the journal entry has changed."""
        def __init__(self, balance: Decimal) -> None:
            super().__init__()
            self.balance = balance

    def __init__(self) -> None:
        super().__init__()
        # Houdt bij of er nu een Input openstaat. None = geen edit actief.
        self._editing_input: Input | None = None

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns('Grootboeknr.', 'Relatie', 'Omschrijving', 'Bedrag')
        table.add_row('1300', '1001', 'Factuur', self._format_amount_cell('121.00'))
        table.add_row('8000', '', 'Factuur April diensten', self._format_amount_cell('-100.00'))
        table.add_row('1500', '', 'Factuur April diensten', self._format_amount_cell('-21.00'))
        self._recalculate_and_post_balance()

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

        elif event.key == 'escape':
            event.stop()
            event.prevent_default()
            row = table.cursor_row
            if not self._is_row_empty(table, row) and not self._is_row_complete(table, row):
                for col in range(self.LAST_COLUMN + 1):
                    table.update_cell_at(Coordinate(row, col), '')
                self._recalculate_and_post_balance()
                table.move_cursor(row=row, column=0)
            elif table.cursor_column == 0:
                if self._is_row_empty(table, row):
                    row_key = table.coordinate_to_cell_key(Coordinate(row, 0)).row_key
                    table.remove_row(row_key)
                    self._recalculate_and_post_balance()
                balance = self._calculate_balance()
                self.post_message(self.BackToHeader(balance))
            return

        elif event.key == 'up':
            if table.cursor_column == 0 and table.cursor_row != 0 and (
                self._is_row_complete(table, table.cursor_row)
                or self._is_row_empty(table, table.cursor_row)
            ):
                if self._is_row_empty(table, table.cursor_row):
                    row_key = table.coordinate_to_cell_key(Coordinate(table.cursor_row, 0)).row_key
                    table.remove_row(row_key)
                    self._recalculate_and_post_balance()
                    event.stop()
                    event.prevent_default()
                return
            event.stop()
            event.prevent_default()

        elif event.key == 'down':
            if table.cursor_column == 0 and self._is_row_complete(table, table.cursor_row):
                if table.cursor_row == table.row_count - 1:
                    self._append_empty_row_and_move_cursor()
                    event.stop()
                    event.prevent_default()
                return
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
        if coordinate.column == self.LAST_COLUMN:
            parsed = self._parse_amount(event.value)
            if parsed is None:
                self.notify("Ongeldig bedrag")
                return
            value_to_store = self._format_amount_cell(str(parsed))
        else:
            value_to_store = event.value
        table.update_cell_at(coordinate, value_to_store)
        self._recalculate_and_post_balance()
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
            value = self._get_cell_str(table, row, column)
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
        table.add_row("", "", "", self._format_amount_cell(""))
        table.cursor_coordinate = Coordinate(table.row_count - 1, 0)

    def _is_row_complete(self, table: DataTable, row: int) -> bool:
        """Return True if all required cells in the row are non-empty."""
        for column in self.REQUIRED_COLUMNS:
            value = self._get_cell_str(table, row, column)
            if not value.strip():
                return False
        return True

    def _is_row_empty(self, table: DataTable, row: int) -> bool:
        """Return True if all cells in the row are empty."""
        for column in range(len(table.columns)):
            value = self._get_cell_str(table, row, column)
            if value.strip():
                return False
        return True

    def _get_cell_str(self, table: DataTable, row: int, column: int) -> str:
        """Return cell content as a plain string, regardless of internal type.

        Cells in the amount column are stored as Rich Text objects (for
        right-alignment), while other cells are plain strings. This helper
        hides that distinction so callers can always treat cell content as
        a string.
        """
        raw = table.get_cell_at(Coordinate(row, column))
        return str(raw) if raw else ''

    def _parse_amount(self, raw: str) -> Decimal | None:
        """Parse a user-entered amount. Return Decimal or None if invalid."""
        try:
            value = Decimal(raw)
        except InvalidOperation:
            return None
        if value.as_tuple().exponent < -2:
            return None
        return value.quantize(Decimal('0.01'))

    def _format_amount_cell(self, value: str) -> Text:
        """Wrap an amount value in a right-aligned Text cell."""
        return Text(value, justify="right")

    def _calculate_balance(self) -> Decimal:
        """Sum the amount column over all rows. Empty cells contribute zero."""
        table = self.query_one(DataTable)
        total = Decimal('0')
        for row in range(table.row_count):
            value = self._get_cell_str(table, row, self.LAST_COLUMN)
            if value:
                total += Decimal(value)
        return total

    def _recalculate_and_post_balance(self) -> None:
        """Recalculate the balance and notify the screen of the new value."""
        self.post_message(self.BalanceChanged(self._calculate_balance()))

    def _close_editor(self) -> None:
        """Sluit de Input weer, focus terug naar de tabel."""
        if self._editing_input is not None:
            self._editing_input.remove()
            self._editing_input = None
        self.query_one(DataTable).focus()

    def clear(self) -> None:
        """Reset the journal entry lines to empty.

        Removes all rows, then adds one empty row so the cursor has a starting point and user
        can type immediately. Balance is recalculated.
        """
        table = self.query_one(DataTable)
        table.clear()
        table.add_row('', '', '', self._format_amount_cell(''))
        self._recalculate_and_post_balance()

    def ensure_row(self) -> None:
        """Make sure the table has at least one row."""
        table = self.query_one(DataTable)
        if table.row_count == 0:
            table.add_row('', '', '', self._format_amount_cell(''))