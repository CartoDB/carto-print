from .map_provider import MapProvider

DEFAULT_URLS = ['https://maps1.nyc.gov/tms/1.0.0/carto/basemap/{z}/{x}/{y}.jpg']


class TmsProvider(MapProvider):

    def __init__(self, server_urls=DEFAULT_URLS):
        super().__init__(server_urls)

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        y = (2 ** zoom) - y - 1
        return url.format(z=zoom, x=x, y=y)

    def get_name(self):
        return 'tms'
