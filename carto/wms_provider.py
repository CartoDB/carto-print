import datetime
from .map_provider import MapProvider
from .utils import latlon_2_tile, tile_2_bbox

MAX_TILE_SIZE = 256


class WmsProvider(MapProvider):

    def __init__(self, server_url='http://ovc.catastro.meh.es/Cartografia/WMS/ServidorWMS.aspx?SERVICE=WMS&SRS=EPSG:4326&REQUEST=GETMAP&bbox={minx},{miny},{maxx},{maxy}&width=256&height=256&format=PNG&transparent=No&layers=catastro'):
        self.server_url = server_url

    def prepare_url(self, tile_size, lon, lat, zoom):
        x, y = latlon_2_tile(lat, lon, zoom)
        minx, miny, maxx, maxy = tile_2_bbox(x, y, zoom)
        return self.server_url.format(minx=minx, miny=miny, maxx=maxx, maxy=maxy)

    def generate_filename(self):
        return 'wms_{date}'.format(date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def get_max_tile_size(self):
        return MAX_TILE_SIZE
