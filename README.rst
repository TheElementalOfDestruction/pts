PIL Text Scaler
===============
Module for automatically fitting a string of text inside of a specified area.

Usage
_____
Loading a Font
--------------
To use a font with this module, it first needs to be loaded. The function ``loadTTF`` is used to load a True Type Font file. It takes 4 arguments: the name to be used for the font, the path of the font, an optional encoding, and an option to load the fast version of the font.

.. code:: python

    import PTS

    PTS.loadTTF('arial', 'arial.ttf')

Scaling Text
------------
To figure out if a string of text will fit in an area with the current settings, all you need to do is use the main function of the module: ``fitText``. The function takes 5 arguments: the text to be fit, the width of the area in pixels, the height of the area in pixels, an optional font name (defaults to "consolas"), an optional minimum size to use (use None to try all available sizes), and an option to use fast fonts, when available. The function returns a tuple of the wrapped text, the font that worked, and the size of said font, in that order.

.. code:: python

    import PTS

    text = "This is a string of text to be fit."

    PTS.loadTTF('arial', 'arial.ttf') # Load the font
    result = PTS.fitText(text, 100, 500, 'arial', 23, fast = True)


Changing the Minimum and Maximum Text Sizes
-------------------------------------------
If you would like to change the minimum and maximum text sizes (as well as the difference between each size the module tries) you can use the ``setSizes`` command. This command will automatically reload any fonts already loaded. It takes 3 parameters: minimum size (inclusive), the maximum size (exclusive), and an optional step parameter which is used to tell it how for to space each valid size from each other. The default for these values are 15, 35, and 2, respectively.

.. code:: python

    import PTS

    minimum = 30
    maximum = 60
    step = 2

    PTS.setSizes(30, 60, 2)

Fast Fonts
----------
Fast fonts are a way to process the text data much faster. The downsides are that they are memory intensive, taking a lot longer to load, and are slightly less accurate.
