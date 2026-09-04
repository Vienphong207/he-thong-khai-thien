import os, json, re, urllib.request

public_dir = "public"
html_path = os.path.join(public_dir, "index.html")
manifest_path = os.path.join(public_dir, "manifest.json")

# 1. Tìm file Avatar
img_file = "avatar.jpg"
if os.path.exists(public_dir):
    for f in os.listdir(public_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            img_file = f
            break

img_type = "image/png" if img_file.endswith(".png") else "image/jpeg"
print(f"-> Avatar phát hiện: /{img_file} ({img_type})")

# 2. Tiêm bộ thẻ Icon CHUẨN ĐÓNG BĂNG cho Chrome Android
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Dọn sạch thẻ icon cũ
    content = re.sub(r'<link rel="(shortcut icon|icon|apple-touch-icon|manifest)".*?>', '', content)
    
    # Ép Chrome quét chuẩn Avatar ở cả chế độ Shortcut lẫn PWA
    full_icon_tags = f'''
  <link rel="shortcut icon" href="/{img_file}" type="{img_type}">
  <link rel="icon" type="{img_type}" sizes="192x192" href="/{img_file}">
  <link rel="icon" type="{img_type}" sizes="512x512" href="/{img_file}">
  <link rel="apple-touch-icon" sizes="180x180" href="/{img_file}">
  <link rel="manifest" href="/manifest.json">
'''
    content = content.replace("</head>", f"{full_icon_tags}\n</head>")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("-> Đã nạp bộ thẻ HTML Icon đa tầng cho Chrome!")

# 3. Ép cấu hình Manifest chuẩn 100%
manifest = {
  "short_name": "Hệ Thống",
  "name": "Hệ Thống Toàn Năng",
  "icons": [
    {
      "src": f"/{img_file}",
      "sizes": "192x192",
      "type": img_type,
      "purpose": "any maskable"
    },
    {
      "src": f"/{img_file}",
      "sizes": "512x512",
      "type": img_type,
      "purpose": "any maskable"
    }
  ],
  "start_url": "/",
  "background_color": "#0b0914",
  "theme_color": "#0b0914",
  "display": "standalone"
}

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("-> Đã đồng bộ Manifest!")
