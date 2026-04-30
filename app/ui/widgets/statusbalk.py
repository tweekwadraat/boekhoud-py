from textual.widgets import Footer

class DOSFooter(Footer):
    def on_mount(self):
        self.show_command_palette = False