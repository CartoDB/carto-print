from abc import ABC, abstractmethod
import datetime
import time
from .utils import DEFAULT_TILE_SIZE


class MapProvider(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def prepare_url(self, tile_size, lon, lat, zoom):
        pass

    def generate_filename(self):
        return '{date}'.format(date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def get_max_tile_size(self):
        return DEFAULT_TILE_SIZE

    def should_retry(self):
        False

    def wait(self):
        time.sleep(1)
