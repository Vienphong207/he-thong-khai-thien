import os, re, json

public_dir = "public"
os.makedirs(public_dir, exist_ok=True)

# 1. Tìm file ảnh Avatar sẵn có
img_file = "avatar.jpg"
for f in os.listdir(public_dir):
    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_file = f
        break

print(f"-> Đã ghi nhận Avatar: /{img_file}")

# 2. Cấu hình Manifest cho PWA Lối tắt màn hình chính
manifest = {
  "short_name": "Phật Ma Đồng Thể",
  "name": "Phật Ma Đồng Thể - Hệ Thống Khai Thiên",
  "icons": [
    {
      "src": f"/{img_file}",
      "sizes": "192x192 512x512",
      "type": "image/png" if img_file.endswith(".png") else "image/jpeg",
      "purpose": "any maskable"
    }
  ],
  "start_url": "/",
  "background_color": "#0b0914",
  "theme_color": "#0b0914",
  "display": "standalone"
}

with open(os.path.join(public_dir, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# 3. Tiêm thẻ meta Icon vào index.html
html_path = os.path.join(public_dir, "index.html")
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Xóa các thẻ cũ nếu có
    content = re.sub(r'<link rel="(icon|apple-touch-icon|manifest)".*?>', '', content)
    content = re.sub(r'<title>.*?</title>', '', content)

    pwa_tags = f'''
  <title>Phật Ma Đồng Thể</title>
  <link rel="icon" type="image/x-icon" href="/{img_file}">
  <link rel="apple-touch-icon" href="/{img_file}">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#0b0914">
'''
    content = content.replace("</head>", f"{pwa_tags}\n</head>")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("-> Đã đồng bộ Icon & Title chuẩn Phật Ma Đồng Thể!")

