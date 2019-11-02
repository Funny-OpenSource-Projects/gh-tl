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

    def do_GET(self):

        base_url = 'https://www.github.com/'
        user_param_pattern = re.compile(r'user\=([^\=\&]+)') 
        username = user_param_pattern.search(self.path).group(1)

        zoom_param_pattern = re.compile(r'zoom\=([^\=\&]+)') 
        try:
            zoom = zoom_param_pattern.search(self.path).group(1)
        except:
            zoom = 1

        color_param_pattern = re.compile(r'color\=([^\=\&]+)') 
        color_match = color_param_pattern.search(self.path)

        response = requests.get(base_url + username)

        svg_timeline_pattern = re.compile(r'\<svg[^>]*js\-calendar[^>]*\>(.*?)\<\/svg\>', re.MULTILINE | re.DOTALL)
        svg = svg_timeline_pattern.search(response.text)

        resized_width = str(722 * float(zoom))
        resized_height = str(112 * float(zoom))

        
        message = str(self.get_svg_template())
        message = re.sub(r'\[CONTENT\]', svg.group(1), message)
        message = re.sub(r'\[WIDTH\]', resized_width, message)
        message = re.sub(r'\[HEIGHT\]', resized_height, message)

        if (color_match is not None):
            color = color_match.group(1)
            message = re.sub(r'c6e48b', self.process_color(color, 0.2), message)
            message = re.sub(r'7bc96f', self.process_color(color, 0.4), message)
            message = re.sub(r'239a3b', self.process_color(color, 0.6), message)
            message = re.sub(r'196127', self.process_color(color, 0.8), message)

        self.send_response(200)
        self.send_header("Accept-Ranges","bytes")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Disposition","attachment")
        self.send_header("Content-Length",len(message))
        self.send_header('Content-type','image/svg+xml')
        self.end_headers()

        self.wfile.write(str(message).encode())
        return  