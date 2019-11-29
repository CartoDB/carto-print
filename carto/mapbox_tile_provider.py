import datetime
import time
from .zxy_provider import ZxyProvider
from .utils import latlon_2_tile

DEFAULT_URLS = [
    'https://api.mapbox.com/styles/v1/{username}/{style}/tiles/{tilesize}/{z}/{x}/{y}?access_token={token}',
]

STYLES = [
    'streets-v11',
    'outdoors-v11',
    'light-v10',
    'dark-v10',
    'satellite-v9',
    'satellite-streets-v11',
    'navigation-preview-day-v4',
    'navigation-preview-night-v4',
    'navigation-guidance-day-v4',
    'navigation-guidance-night-v4',
]


class MapboxTileProvider(ZxyProvider):

    def __init__(self, token, username='mapbox', style=STYLES[0], server_urls=DEFAULT_URLS):
        super().__init__(server_urls)
        self.token = token
        self.style = style
        self.username = username

    def prepare_url(self, tile_size, lon, lat, zoom):
        url = self.server_urls[self.current % len(self.server_urls)]
        self.current += 1
        x, y = latlon_2_tile(lat, lon, zoom)
        return url.format(username=self.username, style=self.style, tilesize=tile_size, z=zoom, x=x, y=y, token=self.token)

    def get_max_tile_size(self):
        return 512

    def generate_filename(self):
        return 'mapbox_{style}_{date}'.format(style=self.style, date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def wait(self):
        time.sleep(3)
