import socket
import threading
import re
import os
import mimetypes
from ._request import Request
from ._response import Response

class Pyxpress:
    def __init__(self):
        self.routes = {"GET": [], "POST": []}
        self.middlewares = []

    def use(self, func):
        self.middlewares.append(func)

    def get(self, path):
        def decorator(handler):
            self.routes["GET"].append((self._compile(path), handler))
            return handler
        return decorator

    def post(self, path):
        def decorator(handler):
            self.routes["POST"].append((self._compile(path), handler))
            return handler
        return decorator

    def _compile(self, path):
        pattern = "^" + re.sub(r":(\w+)", lambda m: f"(?P<{m.group(1)}>[^/]+)", path) + "$"
        return re.compile(pattern)
    
    def static(self, route_path, folder_path):
        route_prefix = route_path.rstrip("/")
        folder = os.path.abspath(folder_path)

        def static_middleware(req, res, next):
            if req.path.startswith(route_prefix):
                rel_path = rel_path = req.path[len(route_prefix):].lstrip("/")
                file_path = os.path.join(folder, rel_path)

                if os.path.exists(file_path) and os.path.isfile(file_path):
                    mime, _ = mimetypes.guess_type(file_path)
                    res.set("Content-Type", mime or "application/octet-stream")
                    with open(file_path, "rb") as f:
                        res.send(f.read())
                    return
            next()

        self.use(static_middleware)

    def _parse_raw(self, data):
        lines = data.split("\r\n")
        method, full_path, _ = lines[0].split()
        headers = {}
        body = ""
        is_body = False
        for line in lines[1:]:
            if line == "":
                is_body = True
                continue
            if not is_body:
                if ": " in line:
                    k, v = line.split(": ", 1)
                    headers[k.lower()] = v
                else:
                    body += line + "\n"

        return method, full_path, headers, body.strip()
    
    def _match(self, method, path):
        for pattern, handler in self.routes.get(method, []):
            match = pattern.match(path)
            if match:
                return handler, match.groupdict()
        return None, {}

    def _handle(self, client):
        try:
            data = client.recv(8102).decode(errors="ignore")
            if not data:
                client.close()
                return
            
            method, full_path, headers, body = self._parse_raw(data)
            req = Request(method, full_path, headers, body)
            res = Response(client)

            def next_middleware(index):
                if index < len(self.middlewares):
                    self.middlewares[index](req, res, lambda: next_middleware(index + 1))
                else:
                    handler, params = self._match(method, req.path)
                    if handler:
                        req.params = params
                        handler(req, res)
                    else:
                        res.status(404).send("404 Not Found")
            
            next_middleware(0)

        except Exception as e:
            print("Error:", e)
            try:
                client.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Error")
            except:
                pass
            client.close()

    def listen(self, port=3000):
        print(f"Server listening in: http://localhost:{port}/")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", port))
        s.listen(5)
        s.settimeout(1.0)
        try:
            while True:
                try:
                    client, _ = s.accept()
                    threading.Thread(target=self._handle, args=(client,), daemon=True).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            s.close()
