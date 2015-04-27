from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

cls = from_filename(path.join(path.dirname(__file__), 'hello.glade'))

w1 = cls()
w2 = cls()

w1.connect('delete-event', Gtk.main_quit)

w1.show_all()
w2.show_all()

Gtk.main()
