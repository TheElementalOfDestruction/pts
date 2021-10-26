**v1.4.7**
* Attempted to fix an issue that would occur in text with leading and trailing spaces by having them automatically stripped from the text.

**v1.4.6**
* Updated README for PyPI upload (finally).
* Added `MANIFEST.in`.
* Fixed module name in `setup.py`.

**v1.4.5**
* Fixed `setup.py`.
* Added new entries to `.gitignore`.

**v1.4.4**
* Added some additional docstrings.
* Fixed the date.

**v1.4.3**
* A specific font was giving me a weird error with Pillow so I went and added some code that should fix it.

**v1.4.2**
* Fixed error in setup if Pillow is not installed.

**v1.4.1**
* Changed `getSize` and `setSizes` to not use case-sensitive font names.

**v1.4.0**
* Changed font size to be specific to a particular font. If no font size is specified, the defaults will be used.
* Changed `setSizes` to `setSize` and changed its function.
* Added new function `getSize` that gives you size details of a font.
* Fixed bug in 1.3.1 that caused `setSizes` to fail.

**v1.3.1**
* Added `MAX_SIZE` field to `PTS.core`. Avoid importing it directly to be able to detect changes to the font size.

**v1.3.0**
* Added new option `preferUnwrapped` to `fitText`. If this is enabled then the function will try to find a size of the font where it does not wrap the text mid-word. Will return the standard if it cannot find any sizes that do not do this.

**v1.2.3**
* Changed the way `FontError` works so that you can now access the font that caused the error. Access is done through `FontError.font`.

**v1.2.2**
* Made adjustment to the core to allow fonts to keep their case when returned from `listFonts`.

**v1.2.1**
* Added new function `listFonts` that returns a list of registered fonts.

**v1.2.0**
* Added new options to some commands for the capability to use fast fonts, a slightly less accurate calculation method that is much faster than the more accurate version.
* Added .gitignore

**v1.1.1**
* Fixed bug caused by `MIN_SIZE` accidentally being deleted.

**v1.1.0**
* Implemented threading to make longer strings faster.
* Fixed an error with `setSizes` so that it actually modified the global variables.

**v1.0.1**
* Fixed version number.
* Added new function to core: `attemptFit`.

**v1.0.0**
* Initial release.
