import json

class Response:
    def __init__(self, client):
        self.client = client
        self.status_code = 200
        self.headers = {"Content-Type": "text/html"}

    def status(self, code):
        self.status_code = code
        return self

    def set(self, key, value):
        self.headers[key] = value
        return self

    def send(self, content):
        if isinstance(content, dict) or isinstance(content, list):
            self.set("Content-Type", "application/json")
            content = json.dumps(content)

        if isinstance(content, str):
            body = content.encode()
        else:
            body = content

        head = f"HTTP/1.1 {self.status_code} OK\r\n"
        for k, v in self.headers.items():
            head += f"{k}: {v}\r\n"
        head += f"Content-Length: {len(body)}\r\n\r\n"

        self.client.sendall(head.encode() + body)
        self.client.close()

    def redirect(self, location, status=302):
        self.status(status)
        self.set("Content-Type", "text/html")
        self.send(f'<meta http-equiv="refresh" content="0; url={location}">')
        self.set("Location", location)
        self.send(f"Redirecting to {location}...")
        # print("REDIRECT " + location)

    def json(self, obj):
        return self.set("Content-Type", "application/json").send(json.dumps(obj))
