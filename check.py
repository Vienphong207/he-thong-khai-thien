import os, urllib.request, subprocess

print("=== 1. ĐỐI SOÁT MÃ NGUỒN CỤC BỘ (TERMUX) ===")
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "THẦN CẤP TOÀN NĂNG" in content:
            print(" -> LOCAL INDEX.HTML: [CHUẨN V2.0]")
        else:
            print(" -> LOCAL INDEX.HTML: [VẪN LÀ CODE CŨ]")

if os.path.exists("public/index.html"):
    with open("public/index.html", "r", encoding="utf-8") as f:
        content = f.read()
        if "THẦN CẤP TOÀN NĂNG" in content:
            print(" -> PUBLIC INDEX.HTML: [CHUẨN V2.0]")
        else:
            print(" -> PUBLIC INDEX.HTML: [CẢNH BÁO: CHỨA CODE CŨ!]")

print("\n=== 2. ĐỐI SOÁT TRẠNG THÁI GIT ===")
try:
    commit = subprocess.check_output(["git", "log", "-1", "--oneline"]).decode().strip()
    print(f" -> Commit mới nhất: {commit}")
except Exception as e:
    print(f" -> Lỗi Git: {e}")

print("\n=== 3. TRUY VẤN TRỰC TIẾP TỚI RENDER (BỎ QUA CACHE TRÌNH DUYỆT) ===")
url = "https://he-thong-khai-thien.onrender.com"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    if "THẦN CẤP TOÀN NĂNG" in html:
        print(" -> RENDER SERVER: [ĐÃ CẬP NHẬT V2.0 THÀNH CÔNG!]")
        print(" => NGUYÊN NHÂN: Do trình duyệt Chrome trên điện thoại lưu Cache/PWA cũ.")
    else:
        print(" -> RENDER SERVER: [VẪN TRẢ VỀ CODE CŨ!]")
        print(" => NGUYÊN NHÂN: Render build chưa xong hoặc bị lỗi deployment.")
except Exception as e:
    print(f" -> Không thể kết nối Render: {e}")
