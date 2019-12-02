import math
import time
import datetime

from io import BytesIO
from PIL import Image, ImageDraw
from urllib.request import urlopen, Request
from future.standard_library import install_aliases

from .carto_provider import DEFAULT_URL, CartoProvider
from .utils import DEFAULT_TILE_SIZE, latlon_2_pixels, pixels_2_latlon, create_bounds

install_aliases()


NUM_RETRIES = 5
SLEEP_TIME = 2

ONE_DPI = 0.393701
IMAGE_MODES = ['RGBA', 'CMYK']


class Printer(object):
    def __init__(self, username, map_id, api_key, width_cm, height_cm,
                 zoom_level, bounds, dpi, mode='RGBA',
                 server_url=DEFAULT_URL, provider=None):
        if provider:
            self.provider = provider
        else:
            self.provider = CartoProvider(username, api_key, map_id, server_url=server_url)
        self.width = width_cm
        self.height = height_cm
        self.zoom = zoom_level
        self.bounds = create_bounds(bounds)
        self.dpi = dpi
        self.mode = mode
        self.validate_mode()
        self.filename = self.generate_filename()

    def generate_filename(self):
        return '{name}_{date}'.format(name=self.provider.get_name(), date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def export(self, directory):
        PIXELS_PER_CM = ONE_DPI * self.dpi

        x_actual_pixels = int(self.width * PIXELS_PER_CM)
        y_actual_pixels = int(self.height * PIXELS_PER_CM)

        max_y = self.bounds['south']
        min_y = self.bounds['north']
        min_x = self.bounds['west']
        max_x = self.bounds['east']

        x_degrees = abs(max_x - min_x)
        y_degrees = abs(max_y - min_y)

        degrees_per_pixel = 360.0 / DEFAULT_TILE_SIZE / (pow(2, self.zoom))

        x_pixels = x_degrees / degrees_per_pixel
        y_pixels = y_degrees / degrees_per_pixel

        ratio = min(math.ceil(y_actual_pixels / y_pixels), math.ceil(x_actual_pixels / x_pixels))

        zoom_ratio = int(math.floor(math.log(int(ratio), 2)))
        TILE_SIZE = DEFAULT_TILE_SIZE * pow(2, zoom_ratio)

        if TILE_SIZE > self.provider.get_max_tile_size():
            TILE_SIZE = self.provider.get_max_tile_size()
            z = self.zoom + zoom_ratio
        else:
            z = self.zoom + zoom_ratio

        lon = max_x - ((max_x - min_x) / 2)
        lat = max_y - ((max_y - min_y) / 2)

        num_tiles_x = int(x_actual_pixels / TILE_SIZE)
        num_tiles_y = int(y_actual_pixels / TILE_SIZE)

        dpi_ratio = 1
        tile_ratio = 1
        degrees_per_pixel = dpi_ratio * tile_ratio * 360.0 / TILE_SIZE / (pow(2, z))
        px, py = latlon_2_pixels(lat, lon, z)

        result = Image.new(self.mode, (x_actual_pixels, y_actual_pixels))

        px -= x_actual_pixels / 2.0 - TILE_SIZE / 2.0
        py += y_actual_pixels / 2.0 - TILE_SIZE / 2.0

        i = 0
        num_tiles_x += 1
        num_tiles_y += 1

        print('total tiles: {}'.format(str(num_tiles_x * num_tiles_y)))
        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                i += 1
                print('tile {}'.format(str(i)))
                u_py = py - y * TILE_SIZE
                u_px = px + x * TILE_SIZE
                n_lat, n_lon = pixels_2_latlon(u_py, u_px, z)
                url = self.provider.prepare_url(TILE_SIZE, n_lon, n_lat, z)
                print(url)
                if self.provider.is_cached(url, self.get_format()):
                    print('from cache')
                    file_s = self.provider.from_cache(url, self.get_format())
                else:
                    print('from url')
                    file_s = self.requestImage(url)
                    self.provider.wait()
                image1 = Image.open(file_s)
                if not self.provider.is_cached(url, self.get_format()):
                    self.provider.save(url, image1, self.dpi, self.get_format())
                draw = ImageDraw.Draw(image1)
                draw.line([0, 0, 0, TILE_SIZE], fill='#ffffff', width=2)
                draw.line([0, TILE_SIZE, TILE_SIZE, TILE_SIZE], fill='#ffffff', width=2)
                draw.line([TILE_SIZE, TILE_SIZE, TILE_SIZE, 0], fill='#ffffff', width=2)
                draw.line([TILE_SIZE, 0, 0, 0], fill='#ffffff', width=2)
                # draw.line((0, image1.size[1], image1.size[0], image1.size[1]), fill=128, width=2)
                del draw
                result.paste(im=image1, box=(x * TILE_SIZE, y * TILE_SIZE))

        path = '{directory}/{filename}.{format}'.format(directory=directory, filename=self.filename, format=self.get_format())
        result.save(path, dpi=(self.dpi, self.dpi), quality=95)

        return path

    def requestImage(self, url):
        attempt = 1
        while attempt <= NUM_RETRIES:
            try:
                req = Request(
                    url,
                    headers={
                        'User-Agent': 'peem'
                    }
                )
                file_s = BytesIO(urlopen(req).read())
                Image.open(file_s)
                return file_s
            except Exception as e:
                print(e)
                if self.provider.should_retry():
                    time.sleep(SLEEP_TIME)
                    attempt += 1
                    if attempt >= NUM_RETRIES:
                        raise e
                else:
                    raise e

    def validate_mode(self):
        if self.mode not in IMAGE_MODES:
            raise Exception('mode not supported')

    def get_format(self):
        if self.mode == 'RGBA':
            return 'png'
        else:
            return 'jpg'
