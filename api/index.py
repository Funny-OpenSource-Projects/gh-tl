from http.server import BaseHTTPRequestHandler
import requests
import re
import os
import colorsys

class handler(BaseHTTPRequestHandler):
    def get_svg_template(self):
        return """<?xml version="1.0" encoding="UTF-8"?>
                <svg width="[WIDTH]" height="[HEIGHT]" viewBox="0 0 722 112" class="js-calendar-graph-svg" 
                version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <style type="text/css" >
                        <![CDATA[
                            .month {
                                font-size: 10px;
                                font-family: helvetica;
                            }
                            .wday {
                                font-size: 10px;
                                font-family: helvetica;
                            }
                        ]]>
                    </style>
                    [CONTENT]
                </svg>
                """
    
    def process_color(self, color, amount=0.5):
        color = color.lstrip("#") 
        r, g, b = tuple([int(color[i:i + 2], 16) for i in range(0, len(color), 2)])
        r, g, b = [x/255.0 for x in (r, g, b)]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        h, l, s = h, 1 - amount, s
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = [int(x*255.0) for x in (r, g, b)] 
        return ''.join(["%0.2X" % c for c in (r,g, b)])
    
    def get_param(self, name, path, default=None):
        pattern = re.compile(r""+name+"\=([^\=\&]+)")
        match = pattern.search(path)
        if match is not None:
            return match.group(1)
        else:
            return default

    def do_GET(self):

        username = self.get_param('user', self.path)
        zoom     = float(self.get_param('zoom', self.path, default=1))
        color    = self.get_param('color', self.path)
        shape    = self.get_param('shape', self.path)
        dark     = self.get_param('dark', self.path, 'false').lower() == 'true'

        response = requests.get(f'https://www.github.com/{username}')
        res_width, res_height = str(722 * zoom), str(112 * zoom)

        svg_pattern = re.compile(r'\<svg[^>]*js\-calendar[^>]*\>(.*?)\<\/svg\>', re.MULTILINE | re.DOTALL)
        svg = svg_pattern.search(response.text)
        message = str(self.get_svg_template())
        message = re.sub(r'\[CONTENT\]', svg.group(1), message)
        message = re.sub(r'\[WIDTH\]', res_width, message)
        message = re.sub(r'\[HEIGHT\]', res_height, message)

        if (shape is not None):
            if (shape == 'circle'):
                message = re.sub(r'<rect', fr'<rect rx="{res_width}" ry="{res_height}"', message)
        
        # Remove coloring classes
        message = re.sub(r'class="ContributionCalendar-day"', "", message)

        if (dark):
            if (color is None):
                color = '7bc96f'

            message = re.sub(r'<text', r'<text fill="#fff"', message)
            message = re.sub('data-level="0"', f"fill='{self.process_color(color, 0.143)}'", message)

        if (color is not None):
            message = re.sub('data-level="1"', f"fill='{self.process_color(color, 0.2)}'", message)
            message = re.sub('data-level="2"', f"fill='{self.process_color(color, 0.4)}'", message)
            message = re.sub('data-level="3"', f"fill='{self.process_color(color, 0.6)}'", message)
            message = re.sub('data-level="4"', f"fill='{self.process_color(color, 0.8)}'", message)

        self.send_response(200)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Disposition", "attachment")
        self.send_header("Content-Length", len(message))
        self.send_header("Content-type", "image/svg+xml")
        self.end_headers()
        self.wfile.write(str(message).encode())
        return  
