carto-print
===========

A Python module to export images at any resolution, size and bounding box from a CARTO named map:

* [Maps API](https://carto.com/docs/carto-engine/maps-api)

Installation
============

You can install carto-print by cloning this repository or by using
[Pip](http://pypi.python.org/pypi/pip):

    pip install carto-print

If you want to use the development version, you can install directly from github:

    pip install -e git+git://github.com/CartoDB/carto-print.git#egg=carto

If using, the development version, you might want to install dependencies as well:

    pip install -r requirements.txt

*Only tested in Python 3*

Usage Example
=============

In this example we are exporting a 300 dpi and 30x20 cm image of the [Paris flood map](https://aromeu.carto.com/builder/87c5667f-3eb5-4a19-9300-b39a2d1970d1/embed)

```python
from carto.print import Printer

printer = Printer('aromeu', '87c5667f-3eb5-4a19-9300-b39a2d1970d1', 'default_public', 30, 20, 12, '1.956253,48.711127,2.835159,49.012429', 300)
printer.export('/tmp')
```

Where the signature of the `Printer` constructor is as follows:

```
Printer(CARTO_USER_NAME, MAP_ID, CARTO_API_KEY, WIDTH_CM, HEIGHT_CM, ZOOM_LEVEL, BOUNDING_BOX, DPI)
```
