import os, json, re

public_dir = "public"
os.makedirs(public_dir, exist_ok=True)

# 1. Tìm file Avatar
img_file = "avatar.jpg"
for f in os.listdir(public_dir):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_file = f
        break

img_type = "image/jpeg" if not img_file.endswith(".png") else "image/png"

# 2. Cấu hình Manifest chuẩn Chrome Android (Giữ tên "Hệ Thống")
manifest = {
  "short_name": "Hệ Thống",
  "name": "Hệ Thống Khai Thiên",
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

# 3. Cập nhật thẻ Icon trong index.html
html_path = os.path.join(public_dir, "index.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'<link rel="(icon|apple-touch-icon|manifest)".*?>', '', content)
    
    pwa_tags = f'''
  <link rel="icon" type="{img_type}" href="/{img_file}">
  <link rel="apple-touch-icon" href="/{img_file}">
  <link rel="manifest" href="/manifest.json">
'''
    content = content.replace("</head>", f"{pwa_tags}\n</head>")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

print("-> Đã cập nhật Manifest chuẩn Avatar, giữ nguyên tên 'Hệ Thống'!")
