import math

DEFAULT_TILE_SIZE = 256
EARTH_RADIUS = 6378137
ORIGIN_SHIFT = 2 * math.pi * EARTH_RADIUS / 2.0


def latlon_2_pixels(lat, lon, z):
    initialResolution = 2 * math.pi * EARTH_RADIUS / DEFAULT_TILE_SIZE
    originShift = 2 * math.pi * EARTH_RADIUS / 2.0
    mx = lon * originShift / 180.0
    my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
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
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)

    return lat, lon


def latlon_2_tile(lat, lon, z):
    lat_rad = math.radians(lat)
    n = 2.0 ** z
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def tile2lon(x, z):
    return x / (2 ** z) * 360 - 180


def tile2lat(y, z):
    n = math.pi - 2 * math.pi * y / 2 ** z
    return 180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)))


def tile_2_bbox(x, y, z):
    maxx = tile2lon(x + 1, z)
    minx = tile2lon(x, z)
    miny = tile2lat(y + 1, z)
    maxy = tile2lat(y, z)
    return minx, miny, maxx, maxy


def sanitize(anything):
    return '_'.join(anything.split('-')).strip()


def create_bounds(bounds):
    if bounds is None:
        return None

    if isinstance(bounds, dict):
        return {
            'west': float(bounds['ne'][1]),
            'east': float(bounds['sw'][1]),
            'south': float(bounds['sw'][0]),
            'north': float(bounds['ne'][0])
        }
    else:
        return {
            'west': float(bounds.split(',')[0]),
            'east': float(bounds.split(',')[2]),
            'south': float(bounds.split(',')[3]),
            'north': float(bounds.split(',')[1])
        }
