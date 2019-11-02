import colorsys

def hex_to_rgb(hex_str):
    """Returns a tuple representing the given hex string as RGB.
    
    >>> hex_to_rgb('CC0000')
    (204, 0, 0)
    """
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    return tuple([int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)])

def rgb_to_hex(rgb):
    """Converts an rgb tuple to hex string for web.
    
    >>> rgb_to_hex((204, 0, 0))
    'CC0000'
    """
    return ''.join(["%0.2X" % c for c in rgb])

def process_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys

    r, g, b = hex_to_rgb(color)
    r, g, b = [x/255.0 for x in (r, g, b)]

    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h, l, s = h, 1 - amount, s

    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r, g, b = [int(x*255.0) for x in (r, g, b)]

    return rgb_to_hex((r, g, b)) 
