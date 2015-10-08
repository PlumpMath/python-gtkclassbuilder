#!/usr/bin/env python
from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

classes = from_filename(path.join(path.dirname(__file__), 'hello.glade'))
cls = classes['MainWindow']

w1 = cls()
w2 = cls()


class Handlers(object):

    def goodbye(self, *args, **kwargs):
        Gtk.main_quit()

w1.connect('delete-event', Gtk.main_quit)
w2.connect_signals(Handlers())

w1.show_all()
w2.show_all()

Gtk.main()
