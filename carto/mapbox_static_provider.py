import datetime
import time
from .zxy_provider import ZxyProvider

DEFAULT_URLS = [
    'https://api.mapbox.com/styles/v1/{username}/{style}/static/{lon},{lat},{z}/{size}x{size}?access_token={token}&attribution=false&logo=false',
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


class MapboxStaticProvider(ZxyProvider):

    def __init__(self, token, username='mapbox', style=STYLES[0], server_urls=DEFAULT_URLS):
        super().__init__(server_urls)
        self.token = token
        self.style = style
        self.username = username

    def prepare_url(self, tile_size, lon, lat, zoom):
        url = self.server_urls[self.current % len(self.server_urls)]
        self.current += 1
        return url.format(username=self.username, style=self.style, lon=lon, lat=lat, z=zoom, size=tile_size, token=self.token)

    def get_max_tile_size(self):
        return 1024

    def generate_filename(self):
        return 'mapbox_{style}_{date}'.format(style=self.style, date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def wait(self):
        time.sleep(3)
