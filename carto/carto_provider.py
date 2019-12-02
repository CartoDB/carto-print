from .map_provider import MapProvider

DEFAULT_URL = 'https://{username}.carto.com'
MAX_TILE_SIZE = 8192


class CartoProvider(MapProvider):

    def __init__(self, username, api_key, map_id, server_url=DEFAULT_URL):
        super().__init__([server_url])
        self.username = username
        self.api_key = api_key
        self.map_id = map_id

    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        return (url + '/api/v1/map/static/named/{template}/{tile_size}/{tile_size}.png?zoom={zoom}&lat={lat}&lon={lon}&api_key={api_key}').format(username=self.username, template=self.map_id, tile_size=tile_size, zoom=zoom, lat=lat, lon=lon, api_key=self.api_key)

    def get_max_tile_size(self):
        return MAX_TILE_SIZE

    def should_retry(self):
        True

    def wait(self):
        return

    def get_name(self):
        return 'carto'
