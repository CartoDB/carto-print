import time
from .zxy_provider import ZxyProvider

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

    def __init__(self, token, username='mapbox', style=STYLES[0], server_urls=DEFAULT_URLS, attribution='© Mapbox © OpenStreetMap contributors'):
        super().__init__(server_urls, attribution=attribution)
        self.token = token
        self.style = style
        self.username = username

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        return url.format(
            username=self.username,
            style=self.style,
            tilesize=tile_size,
            z=zoom,
            x=x,
            y=y,
            token=self.token
        )

    def get_max_tile_size(self):
        return 512

    def wait(self):
        time.sleep(3)

    def get_name(self):
        return 'mapbox'
