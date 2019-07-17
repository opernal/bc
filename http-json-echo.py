#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import cgi
import urllib.request
import base64

def is_json(data):
    try:
        jsonobj = json.loads(data)
    except ValueError as e:
        return False
    return True

def posttoblockchain(jsondata):
    if not is_json(jsondata):
        return False

    APT_ENDPOINT = "http://192.168.0.51:8888/store"
    req = urllib.request.Request(APT_ENDPOINT)
    data = {
        'Data': str(base64.b64encode(jsondata),"utf-8")

    }
    data = json.dumps(data)
    data = data.encode('utf-8')
    req.add_header('Content-Type','application/json; charset=utf-8')
    req.add_header('Content-Length',len(data))

    # print(data)

    response = urllib.request.urlopen(req, data)
    return True

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version
        }).encode())
        return

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-length'])
        post_body = self.rfile.read(int(ctype))
        # print(post_body)
        # print(len(post_body))
        # print(json.loads(post_body))
        #print(ctype)
        #post_body = bytes(pdict['boundary'], 'utf-8')

        try:

            data = json.loads(post_body)
            print(data)
            posttoblockchain(post_body)
            #parsed_path = urlparse(self.path)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                'status':'successful'
            }).encode())
        except json.decoder.JSONDecodeError:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({
                'status':'failed',
                'reason':'JSON format Error!'
            }).encode())


        return

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8000), RequestHandler)
    print('Starting server at http://localhost:8000')
    server.serve_forever()
