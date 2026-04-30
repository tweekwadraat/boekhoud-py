from textual.app import ComposeResult
from textual import events
from textual.screen import Screen
from textual.widgets import Label, ListView, ListItem
from dataclasses import dataclass
from app.ui.widgets.statusbalk import DOSFooter
from app.ui.dialogs.confirm import ConfirmQuitScreen

@dataclass(frozen=True)
class MenuItem:
    """A single entry in the main menu.
    
    The id is the stable technical identifier (used as key in App.SCREENS).
    The label is the user-facing text. The shortcut is the lowercase key 
    that activates the item.
    """
    id: str
    label: str
    shortcut: str


class MainMenuScreen(Screen):
    """
    DOS-style main menu. Items are activated via arrow keys + Enter,
    or directly via single-letter shortcuts (see MENU_ITEMS).
    """
    # TODO !important was needed as theme would otherwise prevail -> to be investigated
    DEFAULT_CSS = """
        ListView {
        background: black !important;
        }
        ListItem.--highlight {
        background: white !important;
        color: black !important;
        }
        ListItem.--highlight Label {
        color: black !important;
        }
        ListView > ListItem.--highlight {
        background: white !important;
        color: black !important;
        }
    """

    MENU_ITEMS: list[MenuItem] = [
        MenuItem(id='financial_administration', label='F   Financiële administratie', shortcut='f'),
        # TODO: Boekingen wordt submenu van financial_administration
        MenuItem(id='journal_entries', label='- B   Boekingen', shortcut='b'),
        
        MenuItem(id='financial_reports', label='Y   Financiële rapportage', shortcut='y'),
        MenuItem(id='invoicing', label='A   Facturering', shortcut='a'),
        MenuItem(id='system_functions', label='S   Systeemfuncties', shortcut='s'),
        MenuItem(id='quit_app', label='Q   Afsluiten programma', shortcut='q'),
    ]


    def compose(self) -> ComposeResult:

        # hoofdmenu
        yield ListView(*[ListItem(Label(menu_item.label), id=menu_item.id) for menu_item in self.MENU_ITEMS])

        #footer
        footer = DOSFooter()
        yield footer


    def _activate(self, item_id: str) -> None:
        """Centrally dispatch a menu item by its id."""
        if item_id == 'quit_app':
            def on_quit_response(result: bool | None) -> None:
                if result:
                    self.app.exit()
            self.app.push_screen(ConfirmQuitScreen(), on_quit_response)
            return
        screen_class = self.app.SCREENS.get(item_id)
        if screen_class is None:
            self.notify(f'Ongeldige keuze: {item_id}')
            return
        self.app.push_screen(screen_class())

    def on_key(self, event: events.Key) -> None:
        # Direct activation via shortcut letter; mirrors arrow+Enter behaviour.
        for index, menu_item in enumerate(self.MENU_ITEMS):
            if menu_item.shortcut == event.key:
                list_view = self.query_one(ListView)
                list_view.index = index
                self._activate(menu_item.id)
                return

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self._activate(event.item.id)
