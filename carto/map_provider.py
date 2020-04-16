from abc import ABC, abstractmethod
import os
import time
from .utils import DEFAULT_TILE_SIZE, latlon_2_tile


class MapProvider(ABC):

    def __init__(self, urls, attribution=None):
        super().__init__()
        self.urls = urls
        self.current_url = 0
        self.attribution = attribution

    @abstractmethod
    def do_prepare_url(self, url, tile_size, lon, lat, zoom, x, y):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def get_attribution(self):
        return self.attribution

    def prepare_url(self, tile_size, lon, lat, zoom):
        x, y = latlon_2_tile(lat, lon, zoom)
        return self.do_prepare_url(self.next_url(), tile_size, lon, lat, zoom, x, y)

    def get_max_tile_size(self):
        return DEFAULT_TILE_SIZE

    def should_retry(self):
        False

    def wait(self):
        time.sleep(1)

    def next_url(self):
        url = self.urls[self.current_url % len(self.urls)]
        self.current_url += 1
        return url

    def is_cached(self, url, format):
        path = self.get_path(url, format)
        return os.path.isfile(path)

    def from_cache(self, url, format):
        if self.is_cached(url, format):
            return self.get_path(url, format)

    def save(self, url, image, dpi, format):
        path = self.get_path(url, format)
        image.save(path, dpi=(dpi, dpi), quality=95)

    def get_path(self, url, format):
        url_hash = hash(url)
        return '/tmp/' + str(url_hash) + '.{format}'.format(format=format)
