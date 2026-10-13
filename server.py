import json, urllib.request, urllib.parse, urllib.error, http.server, threading, webbrowser, pathlib, time, socket
ROOT=pathlib.Path(__file__).resolve().parent
BASE="https://api.elections.kalshi.com/trade-api/v2"
cache={}
def upstream(path,params):
    key=(path,tuple(sorted(params.items())))
    if key in cache and time.time()-cache[key][0]<12:return cache[key][1]
    query=urllib.parse.urlencode(params)
    url=BASE+path+("?"+query if query else "")
    req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"EdgeFinderAI/0.1 (read-only research dashboard)"})
    with urllib.request.urlopen(req,timeout=18) as r:
        data=json.loads(r.read(12_000_000))
    cache[key]=(time.time(),data)
    return data
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p=urllib.parse.urlsplit(self.path)
        if p.path=="/":
            b=(ROOT/"index.html").read_bytes();typ="text/html; charset=utf-8"
        elif p.path.startswith("/api/"):
            route=p.path[4:]
            if route not in ("/markets","/events","/series"):
                return self.send_json({"error":"Unsupported read-only endpoint"},404)
            args=dict(urllib.parse.parse_qsl(p.query,keep_blank_values=False))
            allowed={"limit","cursor","status","event_ticker","series_ticker","ticker","category","with_nested_markets"}
            args={k:v for k,v in args.items() if k in allowed}
            args["limit"]=str(min(1000,max(1,int(args.get("limit","100"))))) if args.get("limit","100").isdigit() else "100"
            try:
                return self.send_json(upstream(route,args))
            except urllib.error.HTTPError as e:
                return self.send_json({"error":f"Kalshi HTTP {e.code}","detail":e.read(400).decode("utf-8","replace")},502)
            except Exception as e:
                return self.send_json({"error":str(e)},502)
        else:return self.send_json({"error":"Not found"},404)
        self.send_response(200);self.send_header("Content-Type",typ);self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
    def send_json(self,obj,status=200):
        b=json.dumps(obj).encode()
        self.send_response(status);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
    def log_message(self,fmt,*args):print(fmt%args)
class Server(http.server.ThreadingHTTPServer):daemon_threads=True
if __name__=="__main__":
    s=Server(("127.0.0.1",0),Handler)
    url=f"http://127.0.0.1:{s.server_port}"
    print("EdgeFinder AI running at",url,flush=True)
    threading.Timer(.8,lambda:webbrowser.open(url)).start()
    try:s.serve_forever()
    except KeyboardInterrupt:pass
