import os, json, re

public_dir = "public"
os.makedirs(public_dir, exist_ok=True)

# 1. Quét Avatar
img_file = "avatar.jpg"
for f in os.listdir(public_dir):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_file = f
        break

img_type = "image/jpeg" if not img_file.endswith(".png") else "image/png"

# 2. Manifest: Tên lối tắt = Hệ Thống | Tên đầy đủ = Hệ Thống Toàn Năng
manifest = {
  "short_name": "Hệ Thống",
  "name": "Hệ Thống Toàn Năng",
  "icons": [
    {
      "src": f"/{img_file}",
      "sizes": "192x192",
      "type": img_type,
      "purpose": "any"
    },
    {
      "src": f"/{img_file}",
      "sizes": "512x512",
      "type": img_type,
      "purpose": "any"
    }
  ],
  "start_url": "/",
  "background_color": "#0b0914",
  "theme_color": "#0b0914",
  "display": "standalone"
}

with open(os.path.join(public_dir, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# 3. Cập nhật Tiêu đề trang HTML
html_path = os.path.join(public_dir, "index.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "<title>" in content:
        content = re.sub(r'<title>.*?</title>', '<title>Hệ Thống Toàn Năng</title>', content)
    else:
        content = content.replace("</head>", "  <title>Hệ Thống Toàn Năng</title>\n</head>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

print("-> Đã đổi tên hệ thống sang 'Hệ Thống Toàn Năng' thành công!")
