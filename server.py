#!/usr/bin/env python3

from flask import Flask, request, Response
import urllib.request
import urllib.error
import os
import sys

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(BASE_DIR, "index.html")
REMOTE_API = "https://musicdata.rejoicemusic.org"


def log(msg):
    print(msg, flush=True)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.route("/")
def serve_index():
    if not os.path.exists(HTML_FILE):
        return (
            f"<h1>Error: index.html not found</h1>"
            f"<p>Expected it at: {HTML_FILE}</p>"
            f"<p>Make sure index.html is in the same folder as server.py.</p>",
            404,
        )

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Rewrite remote URLs so the browser hits our local proxy
    html = html.replace(REMOTE_API, "/proxy/musicdata")
    return html


@app.route("/proxy/musicdata/<path:path>")
def proxy_musicdata(path):
    target_url = f"{REMOTE_API}/{path}"
    if request.query_string:
        target_url += "?" + request.query_string.decode()

    log(f"PROXY → {target_url}")

    req = urllib.request.Request(
        target_url,
        headers={"User-Agent": request.headers.get("User-Agent", "Mozilla/5.0")},
    )

    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        # Forward error response body & status
        headers = {k: v for k, v in e.headers.items()}
        return Response(e.read(), status=e.code, headers=headers)
    except Exception as e:
        log(f"Proxy request failed: {e}")
        return Response(f"Proxy error: {e}", status=502)

    # Forward headers but strip Content-Encoding so the browser
    # does NOT auto-decompress. The JS DecompressionStream must handle it.
    hop_by_hop = {
        "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
        "te", "trailers", "transfer-encoding", "upgrade", "content-encoding",
    }
    fwd_headers = {}
    for key, value in resp.headers.items():
        if key.lower() not in hop_by_hop:
            fwd_headers[key] = value

    # Force raw-bytes treatment so the browser never tries to parse/decode
    fwd_headers["Content-Type"] = "application/octet-stream"

    log(f"PROXY ← {resp.status} ({fwd_headers.get('Content-Length', 'unknown')} bytes)")

    def generate():
        while True:
            chunk = resp.read(8192)
            if not chunk:
                break
            yield chunk

    return Response(generate(), status=resp.status, headers=fwd_headers)


if __name__ == "__main__":
    if not os.path.exists(HTML_FILE):
        print(f"\nERROR: {HTML_FILE} not found!\n")
        sys.exit(1)

    print("=" * 50)
    print(" Rejoicify Local Server")
    print("=" * 50)
    print(f" Serving:     http://localhost:8000")
    print(f" Proxying:    {REMOTE_API}")
    print(f" HTML file:   {HTML_FILE}")
    print("=" * 50)
    print(" IMPORTANT: Open http://localhost:8000 in your browser.")
    print(" Do NOT open index.html directly from your file explorer.\n")
    print(" Press CTRL+C to stop\n")
    app.run(host="0.0.0.0", port=8000, debug=False, threaded=True)
