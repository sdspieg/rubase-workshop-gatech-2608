# CDP-NO-FOCUS-OK: open a basic-auth page in SDS's visible Chrome, answering the auth challenge over CDP
# Usage: python3 open_authed.py URL [PORT]   (creds loaded silently, never printed)
import json, sys, time, urllib.request, websocket, os, re
from dotenv import dotenv_values
url = sys.argv[1]; port = sys.argv[2] if len(sys.argv) > 2 else "9224"
cfg = dotenv_values(os.environ["CRED_FILE"])
user = (cfg.get("RUBASE_BASIC_USER") or "").strip(); pw = (cfg.get("RUBASE_BASIC_PASS") or "").strip()
assert user and pw, "RUBASE_BASIC_USER/PASS missing"
host = re.match(r"https?://([^/]+)", url).group(1)
ver = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version").read())
ws = websocket.create_connection(ver["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
n = [0]; sess = [None]
def send(method, params=None, session=None):
    n[0] += 1; msg = {"id": n[0], "method": method, "params": params or {}}
    if session: msg["sessionId"] = session
    ws.send(json.dumps(msg)); return n[0]
def handle(r):
    m = r.get("method"); p = r.get("params", {})
    if m == "Fetch.authRequired":
        send("Fetch.continueWithAuth", {"requestId": p["requestId"], "authChallengeResponse":
             {"response": "ProvideCredentials", "username": user, "password": pw}}, sess[0])
    elif m == "Fetch.requestPaused":
        send("Fetch.continueRequest", {"requestId": p["requestId"]}, sess[0])
def call(method, params=None, session=None):
    i = send(method, params, session)
    while True:
        r = json.loads(ws.recv())
        if r.get("id") == i: return r
        handle(r)
tid = call("Target.createTarget", {"url": "about:blank"})["result"]["targetId"]
sess[0] = call("Target.attachToTarget", {"targetId": tid, "flatten": True})["result"]["sessionId"]
call("Fetch.enable", {"handleAuthRequests": True, "patterns": [{"urlPattern": f"https://{host}/*"}]}, sess[0])
call("Page.enable", {}, sess[0])
send("Page.navigate", {"url": url}, sess[0])
end = time.time() + 45; loaded = False
while time.time() < end:
    r = json.loads(ws.recv()); handle(r)
    if r.get("method") == "Page.loadEventFired" and r.get("sessionId") == sess[0]:
        loaded = True; break
ws.settimeout(1); t2 = time.time() + 5
while time.time() < t2:
    try: handle(json.loads(ws.recv()))
    except Exception: pass
ws.settimeout(60)
call("Fetch.disable", {}, sess[0])
r = call("Runtime.evaluate", {"expression": "JSON.stringify({t:document.title,u:location.href,slides:(typeof slides!=='undefined'?slides.length:null),rev:!!document.querySelector('script[src^=\"/review.js\"]')})", "returnByValue": True}, sess[0])
print("loaded:", loaded, r["result"]["result"].get("value"))
call("Target.activateTarget", {"targetId": tid})
