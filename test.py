import json
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


def application(environ, start_response):
    start_response('200 OK',[('Content-Type', 'text/html')])
    params = parse_qs(environ['QUERY_STRING'])
    #name = params.get('name', [''])[0]
    #no = params.get('no', [''])[0]

    dic = {'name': '', 'no':'2'}

    return [json.dumps(dic)]

if __name__ == "__main__":
    port = 5888
    httpd = make_server("0.0.0.0", port, application)
    print ("serving http on port {0}".format(str(port)))
    httpd.serve_forever()