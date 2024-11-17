from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps, loads
from os import environ
from re import compile
from typing import Self
from urllib.parse import urljoin
from urllib.request import Request, urlopen

provider_base_url = environ.get('PROVIDER_BASE_URL', 'http://localhost/')
graphql_query_state_regex = compile(r'GraphQL query on (\S+)')

class HTTPRequestHandler(BaseHTTPRequestHandler):
  def do_POST(self: Self) -> None:
    try:
      if 'Content-Length' not in self.headers:
        raise Exception('Content-Length header not set in request')
      if 'Content-Type' not in self.headers:
        raise Exception('Content-Type header not set in request')
      if (content_type := self.headers['Content-Type']) != 'application/json':
        raise Exception('Content-Type header not set to application/json in request')

      data = loads(self.rfile.read(int(self.headers['Content-Length'])))

      if (matches := graphql_query_state_regex.fullmatch(data['state'])) is None:
        raise Exception(f'''State not supported: {data['state']}''')

      out_req = Request(
        urljoin(provider_base_url, matches[1]),
        method = 'POST',
        headers = {'Content-Type': 'application/json'},
        data = dumps({'query': data['params']['query']}).encode('ascii'),
      )

      try:
        with urlopen(out_req) as out_res:
          self.send_response(out_res.status)
          for name, val in out_res.getheaders(): self.send_header(name, val)
          self.end_headers()
          self.wfile.write(out_res.read())

      except Exception as e:
        self.respond(502, str(e))

    except Exception as e:
      self.respond(500, str(e))

  def respond(self: Self, status_code: int, body: str) -> None:
    raw_body = body.encode('utf-8')
    self.send_response(status_code)
    self.send_header('Content-Length', len(raw_body))
    self.send_header('Content-Type', 'text/plain; charset=utf-8')
    self.end_headers()
    self.wfile.write(raw_body)

if __name__ == '__main__':
  HTTPServer(
    ('', 8000),
    HTTPRequestHandler
  ).serve_forever()
