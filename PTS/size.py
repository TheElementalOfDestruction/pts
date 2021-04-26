FAST_FONTS = {}

def createFastFont(fonts):
    for font in fonts:
        if font not in FAST_FONTS:
            FAST_FONTS[font] = {chr(x): font.getsize_multiline(chr(x)) for x in range(0x10000)}

def getSizeFast(text, font):
    if font in FAST_FONTS:
        ffont = FAST_FONTS[font]
        lines = (getSizeLine(line, ffont) for line in text.split('\n'))
        return (max(line[0] for line in lines), sum(line[1] for line in lines) + (4 * len(lines)))
    else:
        return getSizeSlow(text, font)

def getSizeLine(line, fastFont):
    return sumSizes(fastFont[char] for char in line)

def getSizeSlow(text, font):
    return font.getsize_multiline(text)

def sumSizes(sizes):
    """
    Takes in an iterable of sizes and returns the sums of each for a line.
    """
    args = tuple(args)
    return (sum(x[0] for x in args), max(x[1] for x in args))
