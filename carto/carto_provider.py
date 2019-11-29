import datetime
from .map_provider import MapProvider
from .utils import sanitize

DEFAULT_URL = 'https://{username}.carto.com'
MAX_TILE_SIZE = 8192


class CartoProvider(MapProvider):

    def __init__(self, username, api_key, map_id, server_url=DEFAULT_URL):
        self.username = username
        self.api_key = api_key
        self.map_id = map_id
        self.server_url = server_url

    def prepare_url(self, tile_size, lon, lat, zoom):
        return (self.server_url + '/api/v1/map/static/named/{template}/{tile_size}/{tile_size}.png?zoom={zoom}&lat={lat}&lon={lon}&api_key={api_key}').format(username=self.username, template=self.map_id, tile_size=tile_size, zoom=zoom, lat=lat, lon=lon, api_key=self.api_key)

    def generate_filename(self):
        return '{username}_{map_id}_{date}'.format(username=self.username, map_id=sanitize(self.map_id), date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def get_max_tile_size(self):
        return MAX_TILE_SIZE

    def should_retry(self):
        True

    def wait(self):
        return
