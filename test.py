from gtkclassbuilder import from_filename
from gi.repository import Gtk

cls = from_filename('test.glade')

w1 = cls()
w2 = cls()

w1.connect('delete-event', Gtk.main_quit)

w1.show_all()
w2.show_all()

Gtk.main()
