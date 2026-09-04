import os, json, urllib.request

print("=== 1. ĐỐI SOÁT CẤU HÌNH CỤC BỘ (TERMUX) ===")
public_dir = "public"
manifest_path = os.path.join(public_dir, "manifest.json")
html_path = os.path.join(public_dir, "index.html")

# 1. Kiểm tra Manifest
if os.path.exists(manifest_path):
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"-> Tên Lối Tắt: {data.get('short_name')}")
            icons = data.get("icons", [])
            if icons:
                icon_path = icons[0].get("src")
                print(f"-> Đường dẫn Icon trong Manifest: {icon_path}")
                real_img = os.path.join(public_dir, icon_path.lstrip("/"))
                if os.path.exists(real_img):
                    print(f"-> File ảnh thực tế: [CÓ TỒN TẠI] ({real_img})")
                else:
                    print(f"-> File ảnh thực tế: [THIẾU] (Không thấy {real_img})")
            else:
                print("-> Icon: [CẢNH BÁO] Chưa khai báo danh sách Icon!")
    except Exception as e:
        print(f"-> File Manifest lỗi cú pháp: {e}")
else:
    print("-> Manifest: [THIẾU] Chưa có file manifest.json!")

# 2. Kiểm tra HTML
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
        has_manifest = 'rel="manifest"' in html or "rel='manifest'" in html
        has_icon = 'rel="icon"' in html or "rel='icon'" in html
        print(f"-> Thẻ HTML Manifest: {'[ĐÃ CHÈN]' if has_manifest else '[THIẾU]'}")
        print(f"-> Thẻ HTML Icon: {'[ĐÃ CHÈN]' if has_icon else '[THIẾU]'}")

# 3. Kiểm tra Render Live
print("\n=== 2. ĐỐI SOÁT TRỰC TIẾP TRÊN RENDER SERVER ===")
domain = "https://he-thong-khai-thien.onrender.com"
try:
    req = urllib.request.Request(f"{domain}/manifest.json", headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=8) as res:
        if res.status == 200:
            m_data = json.loads(res.read().decode('utf-8'))
            print(f"-> Render Manifest Live: [ONLINE 200 OK]")
            print(f"-> Render Short Name: {m_data.get('short_name')}")
            
            # Kiểm tra file icon trên server
            icon_url = f"{domain}{m_data['icons'][0]['src']}"
            req_img = urllib.request.Request(icon_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_img, timeout=8) as res_img:
                if res_img.status == 200:
                    print(f"-> Render Icon File Live: [ONLINE 200 OK]")
except Exception as e:
    print(f"-> Render Server chưa cập nhật xong hoặc mất kết nối: {e}")

