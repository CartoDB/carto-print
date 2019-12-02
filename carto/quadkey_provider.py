from .map_provider import MapProvider
import mercantile

DEFAULT_URLS = [
    "https://t0.ssl.ak.tiles.virtualearth.net/tiles/a{q}.jpeg?g=7863",
    "https://t1.ssl.ak.tiles.virtualearth.net/tiles/a{q}.jpeg?g=7863",
]


class QuadkeyProvider(MapProvider):

    def __init__(self, server_urls=DEFAULT_URLS):
        super().__init__(server_urls)

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        quadkey = mercantile.quadkey(x, y, zoom)
        return url.format(q=quadkey)

    def get_name(self):
        return 'quadkey'
