from textual.app import App
from app.ui.menu import MainMenuScreen
from app.ui.journal_entries import JournalEntriesScreen 

class AdministrationApp(App):

    ENABLE_THEMING = False
    
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
    """

    SCREENS = {
        "journal_entries": JournalEntriesScreen,
    }


    def on_mount(self):
        self.push_screen(MainMenuScreen())



def main():
    AdministrationApp().run()


if __name__ == '__main__':
    main()


