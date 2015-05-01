from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

classes = from_filename(path.join(path.dirname(__file__), 'ChatWin.glade'))


class MainWin(classes['ChatWin']):

    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)
        self.connect_signals(self)

    def send(self, *args, **kwargs):
        log = self.get_object('Log')
        compose = self.get_object('Compose')
        buf = log.get_buffer()
        buf.insert(buf.get_end_iter(), compose.get_text() + '\n')
        compose.set_text('')

    def quit(self, *args, **kwargs):
        Gtk.main_quit()


w = MainWin()
w.show_all()
Gtk.main()
