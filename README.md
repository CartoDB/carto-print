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

printer = Printer('aromeu', 'tpl_87c5667f_3eb5_4a19_9300_b39a2d1970d1', 'default_public', 30, 20, 12, '1.956253,48.711127,2.835159,49.012429', 300)
printer.export('/tmp')
```

Where the signature of the `Printer` constructor is as follows:

```
Printer(CARTO_USER_NAME, MAP_ID, CARTO_API_KEY, WIDTH_CM, HEIGHT_CM, ZOOM_LEVEL, BOUNDING_BOX, DPI)
```

Known Issues
============

Some exported images may not represent exactly what you see in the map for the given zoom level when you ask for a resolution different than 72DPI. The reason is the static maps API returns images at 72DPI so to achieve a bigger resolution the library requests for bigger images to re-scale.

For this reason, specially labels and point size, line width, may be affected. If that's the case you should be able to "design your map for printing" by increaing the text, points and lines sizes.

Having said that, some of the known issues are:

- Google Maps basemaps cannot be rendered
