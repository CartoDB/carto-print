from .zxy_provider import ZxyProvider
from .utils import latlon_2_tile

DEFAULT_URL = 'http://www.ign.es/wmts/pnoa-ma?FORMAT=image%2Fjpeg&VERSION=1.0.0&SERVICE=WMTS&REQUEST=GetTile&EXCEPTIONS=application%2Fvnd.ogc.se_inimage&LAYER=OI.OrthoimageCoverage&STYLE=default&SRS=EPSG%3A4258&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}'


class WmtsProvider(ZxyProvider):

    def __init__(self, server_url=DEFAULT_URL):
        super().__init__([server_url])
