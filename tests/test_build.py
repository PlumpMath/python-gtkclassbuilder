from gtkclassbuilder import from_string
from gi.repository import Gtk

input = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.18.3 -->
<interface>
  <requires lib="gtk+" version="3.12"/>
  <object class="GtkWindow" id="MainWindow">
    <property name="can_focus">False</property>
    <child>
      <object class="GtkBox" id="box1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkLabel" id="label1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="label" translatable="yes">Hello, World!</property>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="button1">
            <property name="label" translatable="yes">Goodbye</property>
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="receives_default">True</property>
            <property name="relief">none</property>
            <signal name="clicked" handler="goodbye" swapped="no"/>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
"""

builder = from_string(input)
w = builder.make_object('MainWindow')

assert isinstance(w, Gtk.Window)
assert w.get_object('MainWindow') is w

# We're peeking into the object for this one, so it's testing more than just
# the API:
assert isinstance(w.get_object('box1'), builder._classes['box1'])

w2 = builder.make_object('MainWindow')

assert w is not w2
assert w.get_object('box1') is not w2.get_object('box1')
