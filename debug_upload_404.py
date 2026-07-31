import urllib.request
import urllib.error

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

sample_chat = "[10/01/2026, 10:15:30] Ravi: Live test"
boundary = "----WebKitFormBoundaryDebug"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="Test.txt"\r\n'
    "Content-Type: text/plain\r\n\r\n"
    + sample_chat + "\r\n"
    f"--{boundary}--\r\n"
).encode('utf-8')

for url in ["https://chatlens-olmp.onrender.com/api/upload", "https://chatlens-olmp.onrender.com/api/upload/"]:
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    try:
        res = opener.open(req)
        print(f"Success on {url}: {res.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError on {url}: Code {e.code}, Reason: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Exception on {url}: {e}")
