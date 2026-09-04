import os, json, urllib.request, subprocess

print("============================================")
print("   THẦN THỨC ĐỐI SOÁT - HỆ THỐNG KHAI THIÊN")
print("============================================")

# 1. KIỂM TRA FILE CỤC BỘ (TERMUX)
print("\n[1] KIỂM TRA FILE CỤC BỘ (LOCAL)")
files = {
    "server.js": os.path.exists("server.js"),
    "package.json": os.path.exists("package.json"),
    "public/index.html": os.path.exists("public/index.html"),
    "public/manifest.json": os.path.exists("public/manifest.json"),
}

avatar_found = None
if os.path.exists("public"):
    for f in os.listdir("public"):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            avatar_found = f
            break

for f_name, exists in files.items():
    status = "✔️ OK" if exists else "❌ THIẾU"
    print(f" -> {f_name.ljust(22)}: {status}")

print(f" -> {'public/' + (avatar_found if avatar_found else 'avatar'):<22}: {'✔️ OK' if avatar_found else '❌ THIẾU'}")

# 2. KIỂM TRA CHI TIẾT MANIFEST
print("\n[2] SOI CẤU HÌNH MANIFEST")
if os.path.exists("public/manifest.json"):
    try:
        with open("public/manifest.json", "r", encoding="utf-8") as f:
            m_data = json.load(f)
            print(f" -> Tên hiển thị (short_name): {m_data.get('short_name')}")
            print(f" -> Tên đầy đủ (name)       : {m_data.get('name')}")
            icons = m_data.get("icons", [])
            print(f" -> Số Icon đã khai báo    : {len(icons)}")
            if icons:
                print(f" -> Đường dẫn Icon chính   : {icons[0].get('src')}")
    except Exception as e:
        print(f" -> Lỗi đọc Manifest       : {e}")

# 3. TRẠNG THÁI GIT
print("\n[3] TRẠNG THÁI GIT REPOSITORY")
try:
    commit = subprocess.check_output(["git", "log", "-1", "--online"]).decode().strip()
    print(f" -> Commit mới nhất        : {commit}")
except Exception as e:
    print(f" -> Git Error              : {e}")

# 4. TRUY VẤN RENDER LIVE SERVER
print("\n[4] TRUY VẤN MÁY CHỦ RENDER LIVE")
domain = "https://he-thong-khai-thien.onrender.com"

# Check Manifest Live
try:
    req = urllib.request.Request(f"{domain}/manifest.json", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as res:
        live_m = json.loads(res.read().decode('utf-8'))
        print(f" -> Render Manifest Live   : ✔️ ONLINE (Tên: '{live_m.get('short_name')}')")
except Exception as e:
    print(f" -> Render Manifest Live   : ❌ THẤT BẠI ({e})")

# Check Avatar Live
if avatar_found:
    try:
        req_img = urllib.request.Request(f"{domain}/{avatar_found}", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_img, timeout=10) as res_img:
            print(f" -> Render Avatar File Live: ✔️ ONLINE ({res_img.status} OK)")
    except Exception as e:
        print(f" -> Render Avatar File Live: ❌ THẤT BẠI ({e})")

print("\n============================================")
