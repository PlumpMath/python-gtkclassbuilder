from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

ChatWin = from_filename(path.join(path.dirname(__file__), 'ChatWin.glade'))


class Handlers(object):

    def send(self, *args, **kwargs):
        # We need to add a way of locating specific objects. This isn't hard, I
        # just need to do it. For now though, we can't get the text, since we
        # don't actually have a path to the widgets that contain it.
        print("Oi! I can't get at the widgets!")

    def quit(self, *args, **kwargs):
        Gtk.main_quit()


w = ChatWin()
h = Handlers()
w.connect_signals(h)
w.show_all()
Gtk.main()
