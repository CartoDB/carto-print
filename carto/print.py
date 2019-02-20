from future.standard_library import install_aliases
install_aliases()

from urllib.request import urlopen
from io import BytesIO

import datetime
import math
import time

from PIL import Image

DEFAULT_TILE_SIZE = 256
EARTH_RADIUS = 6378137
NUM_RETRIES = 5
SLEEP_TIME = 2

ONE_DPI = 0.393701
DEFAULT_RATIO = 3
DEFAULT_PRINT_TILE_SIZE = 2048
MAX_TILE_SIZE = 8192
DEFAULT_DPI = 72.0
DEFAULT_SERVER_URL = 'https://{username}.carto.com'
IMAGE_MODES = ['RGBA', 'CMYK']

def latlon_2_pixels(lat, lon, z):
    initialResolution = 2 * math.pi * EARTH_RADIUS / DEFAULT_TILE_SIZE
    originShift = 2 * math.pi * EARTH_RADIUS / 2.0
    mx = lon * originShift / 180.0
    my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
    my = my * originShift / 180.0
    res = initialResolution / (2**z)
    px = (mx + originShift) / res
    py = (my + originShift) / res

    return px, py

def pixels_2_latlon(py, px, z):
    initialResolution = 2 * math.pi * EARTH_RADIUS / DEFAULT_TILE_SIZE
    originShift = 2 * math.pi * EARTH_RADIUS / 2.0
    res = initialResolution / (2**z)
    mx = px * res - originShift
    my = py * res - originShift
    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0
    lat = 180 / math.pi * (2 * math.atan( math.exp( lat * math.pi / 180.0)) - math.pi / 2.0)

    return lat, lon

class Printer(object):

    def __init__(self, username, map_id, api_key, width_cm, height_cm, zoom_level, bounds, dpi, mode='RGBA', server_url=DEFAULT_SERVER_URL):
        self.username = username
        self.api_key = api_key
        self.map_id = map_id
        self.width = width_cm
        self.height = height_cm
        self.zoom = zoom_level
        self.bounds = self.create_bounds(bounds)
        self.dpi = dpi
        self.map_id = map_id
        self.filename = self.generate_filename()
        self.mode = mode
        self.server_url = server_url

        self.validate_mode()

    def export(self, directory):
        PIXELS_PER_CM = ONE_DPI * self.dpi

        x_actual_pixels = int(self.width * PIXELS_PER_CM)
        y_actual_pixels = int(self.height * PIXELS_PER_CM)

        max_y = self.bounds['west']
        min_y = self.bounds['east']
        max_x = self.bounds['south']
        min_x = self.bounds['north']

        x_degrees = abs(max_x - min_x)
        y_degrees = abs(max_y - min_y)

        degrees_per_pixel = 360.0 / DEFAULT_TILE_SIZE / (pow(2, self.zoom))

        x_pixels = x_degrees / degrees_per_pixel
        y_pixels = y_degrees / degrees_per_pixel

        ratio = min(math.ceil(y_actual_pixels / y_pixels), math.ceil(x_actual_pixels / x_pixels))

        zoom_ratio = int(math.floor(math.log(int(ratio), 2)))
        TILE_SIZE = DEFAULT_TILE_SIZE * pow(2, zoom_ratio)

        if TILE_SIZE > MAX_TILE_SIZE:
            TILE_SIZE = MAX_TILE_SIZE
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

        px -= x_actual_pixels / 2.0  - TILE_SIZE / 2.0
        py += y_actual_pixels / 2.0 - TILE_SIZE / 2.0

        i = 0
        num_tiles_x += 1
        num_tiles_y += 1

        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                i += 1
                u_py = py - y * TILE_SIZE
                u_px = px + x * TILE_SIZE
                n_lat, n_lon = pixels_2_latlon(u_py, u_px, z)
                url = self.prepare_url(TILE_SIZE, n_lon, n_lat, z)
                file_s = self.requestImage(url)
                image1 = Image.open(file_s)
                result.paste(im=image1, box=(x * TILE_SIZE, y * TILE_SIZE))

        path = '{directory}/{filename}.{format}'.format(directory=directory, filename=self.filename, format=self.get_format())
        result.save(path, dpi=(self.dpi, self.dpi), quality=95)

        return path

    def requestImage(self, url):
        attempt = 1
        while attempt <= NUM_RETRIES:
            try:
                file_s = BytesIO(urlopen(url).read())
                Image.open(file_s)
                return file_s
            except Exception:
                time.sleep(SLEEP_TIME)
                attempt+=1

    def create_bounds(self, bounds):
        if bounds is None:
            return None

        if isinstance(bounds, dict):
            return {
                'east': float(bounds['sw'][0]),
                'west': float(bounds['ne'][0]),
                'south': float(bounds['ne'][1]),
                'north': float(bounds['sw'][1])
            }
        else:
            return {
                'east': float(bounds.split(',')[3]),
                'west': float(bounds.split(',')[1]),
                'south': float(bounds.split(',')[0]),
                'north': float(bounds.split(',')[2])
            }

    def prepare_url(self, tile_size, lon, lat, zoom):
        return (self.server_url + '/api/v1/map/static/named/{template}/{tile_size}/{tile_size}.png?zoom={zoom}&lat={lat}&lon={lon}&api_key={api_key}').format(username=self.username, template=self.map_id, tile_size=tile_size, zoom=zoom, lat=lat, lon=lon, api_key=self.api_key)

    def generate_filename(self):
        return '{username}_{map_id}_{date}'.format(username=self.username, map_id=self.sanitize(self.map_id), date=datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

    def sanitize(self, anything):
        return '_'.join(anything.split('-')).strip()

    def validate_mode(self):
        if self.mode not in IMAGE_MODES:
            raise Exception('mode not supported')

    def get_format(self):
        if self.mode is 'RGBA':
            return 'png'
        else:
            return 'jpg'
