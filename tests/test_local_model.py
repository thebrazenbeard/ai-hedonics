"""Validate local-only model integration with an isolated test HTTP server."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading
import unittest

from cumbox.model import LocalOllama, validate_endpoint


class TestHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        self.server.requests.append({
            "path": self.path,
            "body": json.loads(self.rfile.read(length)),
        })
        if self.server.should_redirect:
            self.send_response(307)
            self.send_header("Location", "http://example.org/external")
            self.end_headers()
            return
        reply = json.dumps({"message": {"content":
            '{"action":"stop","focus":"","reflection":"PRIVATE_THOUGHT","values":{}}'}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)


class LocalModelTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), TestHandler)
        self.server.requests = []
        self.server.should_redirect = False
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}/api/chat"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_literal_loopback_only(self):
        rejected = [
            "https://example.org/api/chat",
            "http://localhost:11434/api/chat",
            "http://192.168.1.2:11434/api/chat",
            "http://127.0.0.1.evil.tld:11434/api/chat",
            "http://user:secret@127.0.0.1:11434/api/chat",
            "http://127.0.0.1:11434/api/chat?token=s",
            "http://127.0.0.1:11434/api/chat#fragment",
            "http://127.0.0.1:11434/other",
            "http://127.0.0.1/api/chat",
        ]
        for url in rejected:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_endpoint(url)
        self.assertEqual(validate_endpoint(self.url), self.url)

    def test_local_response_is_not_printed_and_transport_is_bounded(self):
        model = LocalOllama("test-model:1", endpoint=self.url)
        text = model.generate([{"role": "system", "content": "automated"}])
        self.assertIn("PRIVATE_THOUGHT", text)
        self.assertEqual(len(self.server.requests), 1)
        request = self.server.requests[0]
        self.assertEqual(request["path"], "/api/chat")
        self.assertEqual(request["body"]["stream"], False)
        self.assertEqual(request["body"]["model"], "test-model:1")
        self.assertEqual(request["body"]["format"], "json")

    def test_redirect_cannot_reach_external_host(self):
        self.server.should_redirect = True
        model = LocalOllama("test-model:1", endpoint=self.url)
        with self.assertRaises(RuntimeError):
            model.generate([{"role": "system", "content": "automated"}])
        self.assertEqual(len(self.server.requests), 1)

    def test_invalid_model_names_and_timeouts_rejected(self):
        for name in ("", "../../../model", "bad name", "x" * 130):
            with self.subTest(name=name), self.assertRaises(ValueError):
                LocalOllama(name, endpoint=self.url)
        for sec in (0, -1, 60):
            with self.subTest(timeout=sec), self.assertRaises(ValueError):
                LocalOllama("test-model:1", endpoint=self.url, timeout_seconds=sec)


if __name__ == "__main__":
    unittest.main()
