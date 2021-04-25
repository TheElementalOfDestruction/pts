import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from PTS.errors import FontError


FONTS = {}
SIZES = (
    33,
    31,
    29,
    27,
    25,
    23,
    21,
    19,
    17,
    15,
)

MIN_SIZE = 15

REF_IMG = PIL.Image.new('RGB', (1, 1), (0, 0, 0))
REF_DRAW = PIL.ImageDraw.ImageDraw(REF_IMG)


def loadTTF(name, path, encoding = ''):
    """
    Loads the font from the specified path and stores it with the specified name.
    """
    if name.lower() not in FONTS:
        FONTS[name.lower()] = {size: PIL.ImageFont.truetype(path, size, encoding = encoding) for size in SIZES}
        FONTS[name.lower()]['path'] = path
        FONTS[name.lower()]['encoding'] = ''

def fitText(text, width, height, fontName = 'consolas', minSize = None):
    """
    Attempts to fit the text into the specified area. Will shrink the text size
    if the current size fails until it is less than minSize. Returns a tuple of
    the automatically wrapped text, the font that worked, and the size of the
    font. Returns None if the function failed.
    """
    fontName = fontName.lower()
    if fontName not in FONTS:
        raise FontError('Could not find the specified font (Did you load it and use the right name?)')

    if minSize is None:
        minSize = MIN_SIZE

    words = text.split(' ')

    for size in SIZES:
        currentAttempt = ''
        failed = False
        font = FONTS[fontName][size]
        if size < minSize:
            return None
        totalsize = font.getsize(text)
        if totalsize[0] <= width and totalsize[1] <= height: # This text will already fit into the area.
            return (text, font, size)
        elif totalsize[1] > height: # This font size is already too big.
            continue # Go back to the start of the loop.
        # Create a list of words and whether or not we should split them.
        splitWords = [(word, font.getsize(word)[0] > width) for word in words]
        for word in splitWords:
            if REF_DRAW.textsize(currentAttempt + ' ' + word[0], font)[0] > width: # If the current word will overflow the line, we need to try a few things.
                if word[1]: # Can it be split?
                    currentAttempt += '\n' if REF_DRAW.textsize(currentAttempt + ' ', font)[0] > width else ' '
                    for character in word[0]:
                        currentAttempt += ('\n' + character) if REF_DRAW.textsize(currentAttempt + character, font)[0] > width else character
                else:
                    currentAttempt += '\n' + word[0]
            else:
                currentAttempt += (' ' if (len(currentAttempt) > 0 and currentAttempt[-1] != '\n') else '') + word[0]
            if REF_DRAW.textsize(currentAttempt, font)[1] > height: # If the current attempt is two tall, we have failed.
                failed = True
                break
        if not failed:
            return (currentAttempt, font, size)

    return None

def setSizes(min, max, step):
    """
    Changes the size list used by the module.
    :param min:  Minumum text size to use (inclusive).
    :param max:  Maximim text size to use (exclusive).
    :param step: The step between sizes.
    """
    # Change the SIZES constant.
    SIZES = tuple(reversed(range(min, max, int(abs(step)))))
    MIN_SIZE = min
    # Reload all fonts to use the new text sizes.
    for name in FONTS:
        path = FONTS[name]['path']
        encoding = FONTS[name]['encoding']
        del FONTS[name]
        loadTTF(name, path, encoding)
