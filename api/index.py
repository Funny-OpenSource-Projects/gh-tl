from http.server import BaseHTTPRequestHandler
import requests
import re

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        base_url = 'https://www.github.com/'
        user_param_pattern = re.compile(r'user\=([^\=\&]+)')
        response = requests.get(base_url)

        username = user_param_pattern.search(self.path).group(1)

        response = requests.get(base_url + username)

        print(base_url + username)

        svg_timeline_pattern = re.compile(r'\<svg[^>]*js\-calendar[^>]*\>(.*?)\<\/svg\>', re.MULTILINE | re.DOTALL)

        svg = svg_timeline_pattern.search(response.text)

        svg_tag =   """<?xml version="1.0" encoding="UTF-8"?>
                    <svg width="722" height="112" class="js-calendar-graph-svg" 
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

        message = re.sub(r'\[CONTENT\]', svg.group(1), svg_tag)

        self.send_response(200)
        self.send_header("Accept-Ranges","bytes")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Disposition","attachment")
        self.send_header("Content-Length",len(message))
        self.send_header('Content-type','image/svg+xml')
        self.end_headers()

        

        self.wfile.write(str(message).encode())
        return