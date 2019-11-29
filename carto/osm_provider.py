import time
from .zxy_provider import ZxyProvider

DEFAULT_URLS = [
    'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png',
]


class OsmProvider(ZxyProvider):

    def __init__(self, server_urls=DEFAULT_URLS):
        super().__init__(server_urls)

    def wait(self):
        time.sleep(3)
