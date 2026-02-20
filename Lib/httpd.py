"""
Minimal HTTP server for xv6.

Run:  python /usr/local/lib/python3.12/httpd.py
Then visit http://localhost:8080 on the host
(QEMU forwards host 8080 -> guest 80).
"""

import socket
import sys

HOST = "0.0.0.0"
PORT = 80

DEMO_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>xv6 &mdash; Python HTTP Server</title>
<style>
  :root { --bg: #0d1117; --fg: #c9d1d9; --accent: #58a6ff; --card: #161b22; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: var(--bg); color: var(--fg);
    display: flex; align-items: center; justify-content: center;
    min-height: 100vh;
  }
  .card {
    background: var(--card); border: 1px solid #30363d;
    border-radius: 12px; padding: 2.5rem 3rem;
    max-width: 540px; text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,.4);
  }
  h1 { font-size: 2rem; margin-bottom: .5rem; }
  h1 span { color: var(--accent); }
  .sub { color: #8b949e; margin-bottom: 1.5rem; }
  table { width: 100%%; border-collapse: collapse; margin: 1rem 0; text-align: left; }
  th, td { padding: .45rem .6rem; border-bottom: 1px solid #21262d; }
  th { color: var(--accent); font-weight: 600; }
  .emoji { font-size: 3rem; margin-bottom: 1rem; }
  .footer { margin-top: 1.5rem; font-size: .85rem; color: #484f58; }
  .badge {
    display: inline-block; background: #1f6feb22; color: var(--accent);
    padding: .2rem .6rem; border-radius: 6px; font-size: .8rem;
    border: 1px solid #1f6feb44;
  }
  .utf8-demo { margin-top: 1rem; font-size: 1.1rem; }
</style>
</head>
<body>
<div class="card">
  <div class="emoji">&#x1F680;</div>
  <h1>Hello from <span>xv6</span></h1>
  <p class="sub">Python %(version)s running on RISC-V &middot; served over TCP/IP</p>

  <table>
    <tr><th>Platform</th><td>%(platform)s</td></tr>
    <tr><th>Python</th><td>%(version)s</td></tr>
    <tr><th>Encoding</th><td>%(encoding)s</td></tr>
    <tr><th>FS Encoding</th><td>%(fs_encoding)s</td></tr>
    <tr><th>Server</th><td>%(host)s:%(port)s</td></tr>
  </table>

  <div class="utf8-demo">
    <span class="badge">UTF-8 Demo</span><br>
    &#x4F60;&#x597D;&#x4E16;&#x754C; &bull;
    &#x3053;&#x3093;&#x306B;&#x3061;&#x306F; &bull;
    Caf&#xe9; &bull; &#x00DC;bung &bull;
    &#x1F30D;&#x1F40D;&#x2728;
  </div>

  <p class="footer">&copy; 2025 xv6 Project</p>
</div>
</body>
</html>
"""


def build_page():
    """Render the demo page with live system info."""
    info = {
        "version": sys.version.split()[0],
        "platform": sys.platform,
        "encoding": sys.getdefaultencoding(),
        "fs_encoding": sys.getfilesystemencoding(),
        "host": HOST,
        "port": PORT,
    }
    return (DEMO_PAGE % info).encode("utf-8")


def handle_client(conn, addr):
    """Read one HTTP request, send the demo page, close."""
    try:
        data = b""
        while b"\r\n\r\n" not in data and len(data) < 4096:
            chunk = conn.recv(1024)
            if not chunk:
                return
            data += chunk

        body = build_page()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Content-Length: %d\r\n"
            "Connection: close\r\n"
            "\r\n" % len(body)
        )
        conn.sendall(response.encode("utf-8") + body)
    except Exception as e:
        print("  error:", e)
    finally:
        conn.close()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print("httpd: listening on %s:%d" % (HOST, PORT))
    print("httpd: visit http://localhost:8080 on the host")

    while True:
        conn, addr = srv.accept()
        print("  connection from %s:%d" % (addr[0], addr[1]))
        handle_client(conn, addr)


if __name__ == "__main__":
    main()
