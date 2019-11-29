import datetime
from .map_provider import MapProvider
from .utils import latlon_2_tile

MAX_TILE_SIZE = 256


class TmsProvider(MapProvider):

    def __init__(self, server_urls):
        self.server_urls = server_urls
        self.current = 0

    def prepare_url(self, tile_size, lon, lat, zoom):
        url = self.server_urls[self.current % len(self.server_urls)]
        self.current += 1
        x, y = latlon_2_tile(lat, lon, zoom)
        y = (2 ** zoom) - y - 1
        return url.format(z=zoom, x=x, y=y)

    def generate_filename(self):
        return 'tms_{date}'.format(date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
