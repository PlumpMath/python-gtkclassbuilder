from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

builder = from_filename(path.join(path.dirname(__file__), 'ChatWin.glade'))


class Handlers(object):

    def __init__(self, win):
        self.win = win

    def send(self, *args, **kwargs):
        log = self.win.get_object('Log')
        compose = self.win.get_object('Compose')
        buf = log.get_buffer()
        buf.insert(buf.get_end_iter(), compose.get_text() + '\n')
        compose.set_text('')

    def quit(self, *args, **kwargs):
        Gtk.main_quit()


w = builder.make_object('ChatWin')
w.connect_signals(Handlers(w))
w.show_all()
Gtk.main()
