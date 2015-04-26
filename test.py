import xml.etree.ElementTree as et
from mkclass import make_class
import mkclass
from gi.repository import Gtk

tree = et.parse('test.glade')
root = tree.getroot()
mkclass.check(root)
obj = list(root)[1]

cls = make_class(obj)

w1 = cls()
w2 = cls()

w1.connect('delete-event', Gtk.main_quit)

w1.show_all()
w2.show_all()

Gtk.main()
