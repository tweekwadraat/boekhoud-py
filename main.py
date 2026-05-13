from textual.app import App
from app.ui.menu import MainMenuScreen
from app.ui.journal_entries import JournalEntriesScreen 
from textual.theme import Theme

dos_theme = Theme(
    name="dos",
    # Backgrounds — pure black, no "depth"-shadings
    background="#000000",
    surface="#000000",
    panel="#000000",
    # Foreground — white
    foreground="#FFFFFF",
    # Accenten — No colors
    primary="#FFFFFF",
    secondary="#FFFFFF",
    accent="#FFFFFF",
    # Semantic colors — not applicable in DOS-style
    success="#FFFFFF",
    warning="#FFFFFF",
    error="#FFFFFF",
    dark=True,
)

class AdministrationApp(App):
    
    # TODO !important was needed as theme would otherwise prevail -> to be investigated
    # TODO font-family: "Courier New";
    DEFAULT_CSS = """
        Screen {
            background: black !important;
            color: white;
        }
        ListItem.-highlight {
            background: white !important; 
        }
        ListItem.-highlight Label {
            color: black !important;
        }
        DataTable:blur > .datatable--cursor {
        background: #000000;
        color: #FFFFFF;
        }
    """

    SCREENS = {
        "journal_entries": JournalEntriesScreen,
    }


    def on_mount(self):
        self.register_theme(dos_theme)
        self.theme = "dos"
        self.push_screen(MainMenuScreen())



def main():
    AdministrationApp().run()


if __name__ == '__main__':
    main()


