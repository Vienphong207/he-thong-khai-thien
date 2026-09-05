import json, os

pkg_file = "package.json"
pkg = {}

if os.path.exists(pkg_file):
    with open(pkg_file, "r", encoding="utf-8") as f:
        try:
            pkg = json.load(f)
        except Exception:
            pkg = {}

pkg["name"] = pkg.get("name", "he-thong-khai-thien")
pkg["version"] = pkg.get("version", "1.0.0")
pkg["main"] = "server.js"

if "scripts" not in pkg:
    pkg["scripts"] = {}
pkg["scripts"]["start"] = "node server.js"

if "dependencies" not in pkg:
    pkg["dependencies"] = {}
pkg["dependencies"]["express"] = "^4.18.2"

with open(pkg_file, "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

print("✅ Đã bổ sung express vào dependencies trong package.json!")
