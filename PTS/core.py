import collections
import threading

import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

from PTS.errors import FontError
from PTS.size import FAST_FONTS, createFastFont, getSizeFast, getSizeSlow

REGISTERED = []
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

MAX_SIZE = 33
MIN_SIZE = 15
STEP = 2

REF_IMG = PIL.Image.new('RGB', (1, 1), (0, 0, 0))
REF_DRAW = PIL.ImageDraw.ImageDraw(REF_IMG)


def attemptFit(text, words, width, height, font, size, fast):
    textsize = getSizeFast if fast else getSizeSlow
    currentAttempt = ''
    failed = False
    wrapped = False
    totalsize = textsize(text, font)
    if totalsize[0] <= width and totalsize[1] <= height: # This text will already fit into the area.
        return (text, font, size, wrapped)
    elif totalsize[1] > height: # This font size is already too big.
        return False
    # Create a list of words and whether or not we should split them.
    splitWords = [(word, font.getsize(word)[0] > width) for word in words]
    for word in splitWords:
        if textsize(currentAttempt + ' ' + word[0], font)[0] > width: # If the current word will overflow the line, we need to try a few things.
            if word[1]: # Can it be split?
                wrapped = True
                currentAttempt += '\n' if textsize(currentAttempt + ' ', font)[0] > width else ' '
                for character in word[0]:
                    currentAttempt += ('\n' + character) if textsize(currentAttempt + character, font)[0] > width else character
            else:
                currentAttempt += '\n' + word[0]
        else:
            currentAttempt += (' ' if (len(currentAttempt) > 0 and currentAttempt[-1] != '\n') else '') + word[0]
        if textsize(currentAttempt, font)[1] > height: # If the current attempt is two tall, we have failed.
            return False
    return (currentAttempt, font, size, wrapped)

def listFonts():
    return tuple(x for x in REGISTERED)

def loadTTF(name, path, encoding = '', fast = False, min = None, max = None, step = None):
    """
    Loads the font from the specified path and stores it with the specified
    name.
    """
    if name.lower() not in FONTS:
        max = max or MAX_SIZE
        min = min or MIN_SIZE
        step = step or STEP
        if max == MAX_SIZE and min == MIN_SIZE and step == STEP:
            sizes = SIZES
        else:
            sizes = tuple(reversed(range(min, max, int(abs(step)))))

        REGISTERED.append(name)
        name = name.lower()
        FONTS[name] = {size: PIL.ImageFont.truetype(path, size, encoding = encoding) for size in sizes}
        FONTS[name]['path'] = path
        FONTS[name]['encoding'] = encoding
        FONTS[name]['fast'] = fast
        FONTS[name]['sizes'] = sizes
        FONTS[name]['minSize'] = min
        FONTS[name]['maxSize'] = max
        FONTS[name]['step'] = step
        if fast:
            createFastFont(FONTS[name.lower()][size] for size in sizes)

def fitText(text, width, height, fontName = 'consolas', minSize = None, fast = False, preferUnwrapped = True):
    """
    Attempts to fit the text into the specified area. Will shrink the text size
    if the current size fails until it is less than minSize. Returns a tuple of
    the automatically wrapped text, the font that worked, and the size of the
    font. Returns None if the function failed.

    :param fast:            Tells it whether to use a faster (but slightly less
                            accurate) algorithm to determine the text size.
    :param preferUnwrapped: Tells the function to prefer a version that doesn't
                            wrap the text midword.
    """
    if fontName.lower() not in FONTS:
        raise FontError(fontName)

    fontName = fontName.lower()

    font = FONTS[fontName]

    if minSize is None:
        minSize = font['minSize']

    words = text.split(' ')

    ret = collections.deque()
    def attemptFitRet(text, words, width, height, font, size, fast, ret):
        ret.append(attemptFit(text, words, width, height, font, size, fast))

    threads = tuple(threading.Thread(target = attemptFitRet, args = (text, words, width, height, font[size], size, fast, ret), daemon = True) for size in font['sizes'] if size >= minSize)
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    largest = (None, None, 0, False)
    for result in ret:
        if result:
            if result[2] > largest[2]:
                largest = result

    if preferUnwrapped:
        # We need to get the largest unwrapped version.
        unwrappedLargest = (None, None, 0, False)
        for result in ret:
            if result and not result[3]:
                if result[2] > unwrappedLargest[2]:
                    unwrappedLargest = result

        largest = unwrappedLargest if unwrappedLargest[0] else largest

    return None if largest[0] is None else largest

    # for size in SIZES:
    #     if size < minSize:
    #         return None
    #     result = attemptFit(text, words, width, height, FONTS[fontName][size], size)
    #     if result:
    #         return result
    #
    # return None


def getSize(fontName):
    """
    Returns the minium size, the maximum size, and the step for the specified font.
    """
    if fontName not in FONTS:
        raise FontError(fontName)
    font = FONTS[fontName]
    return {'min': font['minSize'], 'max': font['maxSize'], 'step': font['step']}

def setSize(min, max, step, fontName = None):
    """
    Changes the size used for a specific font. If none are specified, changes
    the defaults and doesn't affect any existing fonts.
    :param min:      Minumum text size to use (inclusive).
    :param max:      Maximim text size to use (exclusive).
    :param step:     The step between sizes.
    :param fontName: The font to change.
    """
    sizes = tuple(reversed(range(min, max, int(abs(step)))))
    if fontName:
        for size in FONTS[fontName]['sizes']:
            if FONTS[fontName][size] in FAST_FONTS:
                del FAST_FONTS[FONTS[fontName][size]]

        path = FONTS[fontName]['path']
        encoding = FONTS[fontName]['encoding']
        del FONTS[fontName]
        loadTTF(fontName, path, encoding, min, max, step)

    else:
        global MAX_SIZE, MIN_SIZE, SIZES, STEP
        MAX_SIZE = max
        MIN_SIZE = min
        SIZES = sizes
        STEP = step
