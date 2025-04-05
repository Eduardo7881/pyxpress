import urllib.parse
import json

class Request:
    def __init__(self, method, full_path, headers, body):
        self.method = method
        self.headers = headers
        self.raw_body = body
        self.url = urllib.parse.urlparse(full_path)
        self.path = self.url.path
        self.query = urllib.parse.parse_qs(self.url.query)
        self.body = self._parse_body()
        self.params = {}

    def _parse_body(self):
        ct = self.headers.get("content-type", "")
        if "application/json" in ct:
            try:
                return json.loads(self.raw_body)
            except:
                return {}
        elif "application/x-www-form-urlencoded" in ct:
            return urllib.parse.parse_qs(self.raw_body)
        return self.raw_body
