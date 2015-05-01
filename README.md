`python-gtkclassbuilder` is an alternative to Gtk Builder, designed to 
ease the making of building blocks within glade.

When it processes a glade file, Gtk Builder gives you back an object -- 
*instances* of the widgets described in the file. This makes it 
unsuitable for creating generic widgets that you'll use multiple times.  
To get another one, you have to process the file all over again.

`python-gtkclassbuilder` on the other hand, constructs a class, which 
like any other widget class, may be instantiated multiple times.

This is still very WIP, but it's possible to do basic things.

See the `examples/` directory for a taste of the api.

# License

LGPL 2.1 or later (The same as Gtk). See `COPYING`
