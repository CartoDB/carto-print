from .map_provider import MapProvider


class ZxyProvider(MapProvider):

    def __init__(self, server_urls, attribution=None):
        super().__init__(server_urls, attribution=attribution)

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        return url.format(z=zoom, x=x, y=y)

    def get_name(self):
        return 'zxy'
