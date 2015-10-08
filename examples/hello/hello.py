from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

builder = from_filename(path.join(path.dirname(__file__), 'hello.glade'))
w1 = builder.make_object('MainWindow')
w2 = builder.make_object('MainWindow')


class Handlers(object):

    def goodbye(self, *args, **kwargs):
        Gtk.main_quit()

w1.connect('delete-event', Gtk.main_quit)
w2.connect_signals(Handlers())

w1.show_all()
w2.show_all()

Gtk.main()
