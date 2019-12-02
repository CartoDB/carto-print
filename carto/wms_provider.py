from .map_provider import MapProvider
from .utils import tile_2_bbox


class WmsProvider(MapProvider):

    def __init__(self, server_url='http://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&SRS=EPSG:4326&REQUEST=GETMAP&bbox={minx},{miny},{maxx},{maxy}&width=256&height=256&format=PNG&transparent=No&layers=OI.OrthoimageCoverage&VERSION=1.0'):
        super().__init__([server_url])

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        minx, miny, maxx, maxy = tile_2_bbox(x, y, zoom)
        return url.format(minx=minx, miny=miny, maxx=maxx, maxy=maxy)

    def get_name(self):
        return 'wms'
