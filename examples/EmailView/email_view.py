#!/usr/bin/env python
from gtkclassbuilder import from_filename
from gi.repository import Gtk
from os import path

classes = from_filename(path.join(path.dirname(__file__),
                                  'draft-email-view.glade'))


def build_email_view(from_, cc, subject, body):

    builder = Gtk.Builder()
    builder.add_from_file('draft-email-view.glade')

    email_view = classes['draft-email-view']()

    def _set_obj_label(name, value):
        widget = email_view.get_object(name)
        widget.set_property('label', value)

    _set_obj_label('from', from_)
    _set_obj_label('cc', cc)
    _set_obj_label('subject', subject)

    body_widget = email_view.get_object('body')
    body_widget.get_buffer().set_text(body)

    return email_view


def _email_link(name, address):
    return '<a href="mailto:%s">%s &lt;%s&gt;</a>' % (address, name, address)


if __name__ == '__main__':
    msg = """Hey There!

I think crypto is really cool, and I felt the need to tell you about it!

-Bob
"""

    email_view = build_email_view(_email_link('Bob', 'bob@example.com'),
                                  _email_link('Alice', 'alice@example.org'),
                                  'Crypto is awesome!',
                                  msg)
    email_view.connect("delete-event", Gtk.main_quit)
    email_view.show_all()
    Gtk.main()
