import sys, urllib.request
url, dest = sys.argv[1], sys.argv[2]
with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
    n = 0
    while True:
        b = r.read(1 << 20)
        if not b: break
        f.write(b); n += len(b)
print(dest, n, "bytes")
