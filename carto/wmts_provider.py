from .zxy_provider import ZxyProvider
from .utils import latlon_2_tile

DEFAULT_URL = 'http://www.ign.es/wmts/ign-base?FORMAT=image%2Fjpeg&VERSION=1.0.0&SERVICE=WMTS&REQUEST=GetTile&EXCEPTIONS=application%2Fvnd.ogc.se_inimage&LAYER=IGNBaseTodo&STYLE=default&SRS=EPSG%3A4258&TILEMATRIXSET=EPSG%3A4258&TILEMATRIX={z}&TILEROW={x}&TILECOL={y}'


class WmtsProvider(ZxyProvider):

    def __init__(self, server_url=DEFAULT_URL):
        super().__init__([server_url])
