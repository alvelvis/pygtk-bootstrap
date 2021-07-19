import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, Gdk, GtkSource, GObject
import sys
import os
import json
if 'win' in sys.platform:
    print("Running on Windows")

def show_dialog_ok(message, entry=False):
    md = Gtk.MessageDialog(window, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, message)
    if entry:
        md.userEntry = Gtk.Entry()
        md.userEntry.set_size_request(250,0)
        md.get_content_area().pack_end(md.userEntry, False, False, 0)
    md.show_all()
    md.run()
    if entry:
        window.userEntry = md.userEntry.get_text()
    md.destroy()
    return

class FileChooserWindow(Gtk.Window):
    def __init__(self):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=window, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            self.filename = dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            self.filename = ""
        
        dialog.destroy()

    def add_filters(self, dialog):
        filter = Gtk.FileFilter()
        filter.set_name("Filter")
        filter.add_pattern("*.*")
        dialog.add_filter(filter)

def click_button(btn):
    button = Gtk.Buildable.get_name(btn)
    
    if button == "":
        return

def save_config():
    with open(config_path, "w") as f:
        json.dump(window.config, f)
    return

def dark_mode_changed(btn, state):
    for obj in objects:
        try:
            objects[obj].get_style_context().remove_class('light' if state else 'dark')
            objects[obj].get_style_context().add_class('dark' if state else 'light')
        except AttributeError:
            pass
    settings.set_property("gtk-application-prefer-dark-theme", state)  # if you want use dark theme, set second arg to True
    window.config['dark_mode'] = state
    save_config()
    return
    
builder = Gtk.Builder()
GObject.type_register(GtkSource.View)
builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/gui.glade")
screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path(os.path.dirname(os.path.abspath(__file__)) + "/gui.css")
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

settings = Gtk.Settings.get_default()

buttons = "".split()
other_objects = "".split()

objects = {
    x: builder.get_object(x)
    for x in buttons + other_objects
}

for button in buttons:
    if isinstance(objects[button], Gtk.Button):
        objects[button].connect('clicked', click_button)

if 'dark_mode' in objects:
    objects['dark_mode'].connect('state-set', dark_mode_changed)

window = builder.get_object("window1")
window.config = {}

config_path = os.path.dirname(os.path.abspath(__file__)) + "/config.json"
if os.path.isfile(config_path):
    with open(config_path) as f:
        window.config.update(json.load(f))

objects['dark_mode'].props.active = window.config.get('dark_mode')
dark_mode_changed(objects['dark_mode'], objects['dark_mode'].props.active)

if len(sys.argv):
    pass

def on_close(x, y):
    if False:
        return True
    Gtk.main_quit()

window.connect('delete_event', on_close)
window.connect("destroy", Gtk.main_quit)
window.show_all()

if __name__ == "__main__":
    Gtk.main()