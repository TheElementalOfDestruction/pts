PIL Text Scaler
===============
Module for automatically fitting a string of text inside of a specified area.

Usage
_____
Loading a Font
--------------
To use a font with this module, it first needs to be loaded. The function ``loadTTF`` is used to load a True Type Font file. It takes 4 arguments: the name to be used for the font, the path of the font, an optional encoding, an option to load the fast version of the font, an optional minimum size, and an optional maximum size.

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

Getting the Minimum and Maximum Text Sizes
------------------------------------------
If you would like to get information on the sizes that a font is using, you can use the ``getSize`` function. It takes a font name and returns a dictionary with size information about that font.

.. code:: python

    import PTS

    information = PTS.getSize('arial')

Changing the Minimum and Maximum Text Sizes
-------------------------------------------
If you would like to change the minimum and maximum text sizes (as well as the difference between each size the module tries) you can use the ``setSize`` function. This function will change an existing font or will change the defaults for new fonts if no font has been specified. It takes 4 parameters: minimum size (inclusive), the maximum size (exclusive), an optional step parameter which is used to tell it how for to space each valid size from each other, and the name of a font to change. The default for these values are 15, 35, 2, and None, respectively.

.. code:: python

    import PTS

    minimum = 30
    maximum = 60
    step = 2

    PTS.setSizes(30, 60, 2) # Changes the default for new fonts.
    PTS.loadTTF('arial', 'arial.ttf') # Will load using the new sizes.

Fast Fonts
----------
Fast fonts are a way to process the text data much faster. The downsides are that they are memory intensive, taking longer to load, and are slightly less accurate.
