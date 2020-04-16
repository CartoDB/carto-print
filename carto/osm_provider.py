import time
from .zxy_provider import ZxyProvider

DEFAULT_URLS = [
    'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png',
]


class OsmProvider(ZxyProvider):

    def __init__(self, server_urls=DEFAULT_URLS, attribution='© OpenStreetMap contributors'):
        super().__init__(server_urls, attribution=attribution)

    def wait(self):
        time.sleep(3)

    def get_name(self):
        return 'osm'
