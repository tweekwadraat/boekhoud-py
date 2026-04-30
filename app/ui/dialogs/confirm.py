from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Static


class ConfirmQuitScreen(ModalScreen[bool]):
    """
    Modal dialog asking the user to confirm quitting the application.
    """
    
    PROMPT = 'Weet u zeker dat u wilt afsluiten? (J/N)'
    
    BINDINGS = [
        ('j', 'confirm', 'Ja'),
        ('n', 'cancel', 'Nee'),
        ('escape', 'cancel', 'Annuleren')
    ]

    def compose(self) -> ComposeResult:
        yield Static(self.PROMPT)

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)