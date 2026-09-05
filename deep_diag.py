import os, json, time, urllib.request, subprocess

print("===================================================")
print("   CHẨN ĐOÁN NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ENGINE)")
print("===================================================")

repo_user = "Vienphong207"
repo_name = "he-thong-khai-thien"
domain = "https://he-thong-khai-thien.onrender.com"

# ---------------------------------------------------------
# TẦNG 1: KIỂM TRA CỤC BỘ (LOCAL TERMUX)
# ---------------------------------------------------------
print("\n[TẦNG 1: TỆP CỤC BỘ & COMMIT HASH LOCAL]")
try:
    local_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    print(f" -> Local Commit Hash : {local_commit[:7]}")
except Exception as e:
    local_commit = "UNKNOWN"
    print(f" -> Lỗi đọc Git Local : {e}")

local_avatar = None
if os.path.exists("public"):
    for f in os.listdir("public"):
        if "avatar" in f.lower() or f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            local_avatar = f
            size = os.path.getsize(os.path.join("public", f))
            print(f" -> File Avatar Local  : public/{f} ({size} bytes)")

# ---------------------------------------------------------
# TẦNG 2: KIỂM TRA GITHUB CLOUD (TRUY VẤN TRỰC TIẾP API)
# ---------------------------------------------------------
print("\n[TẦNG 2: GITHUB REMOTE REPOSITORY (CLOUD API)]")
gh_commit = None
gh_has_avatar = False
try:
    # 1. Kiểm tra Commit Hash mới nhất trên GitHub
    branch_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/branches/main"
    req = urllib.request.Request(branch_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as res:
        b_data = json.loads(res.read().decode())
        gh_commit = b_data['commit']['sha']
        print(f" -> GitHub Commit Hash: {gh_commit[:7]}")

    # 2. Kiểm tra Cấu trúc tệp thực tế trên GitHub Cloud
    tree_url = f"https://api.github.com/repos/{repo_user}/{repo_name}/git/trees/{gh_commit}?recursive=1"
    req_tree = urllib.request.Request(tree_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_tree, timeout=10) as res_tree:
        t_data = json.loads(res_tree.read().decode())
        public_files = [item['path'] for item in t_data.get('tree', []) if item['path'].startswith('public/')]
        print(f" -> Danh sách public/ trên GitHub Cloud:")
        for pf in public_files:
            print(f"    - {pf}")
            if "avatar" in pf.lower() or pf.endswith(('.jpg', '.png', '.jpeg')):
                gh_has_avatar = True
except Exception as e:
    print(f" -> Lỗi kết nối GitHub API: {e}")

# ---------------------------------------------------------
# TẦNG 3: KIỂM TRA TRẠNG THÁI MÁY CHỦ RENDER LIVE
# ---------------------------------------------------------
print("\n[TẦNG 3: PHẢN HỒI THỰC TẾ TỪ RENDER LIVE]")
avatar_ct = "UNKNOWN"
avatar_size = "UNKNOWN"
try:
    live_url = f"{domain}/avatar.jpg?_t={int(time.time())}"
    req_live = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_live, timeout=10) as res_live:
        avatar_ct = res_live.headers.get('Content-Type', 'unknown')
        body = res_live.read()
        avatar_size = len(body)
        print(f" -> Render Avatar Status: {res_live.status} OK")
        print(f" -> Content-Type Trả Về: {avatar_ct}")
        print(f" -> Dung Lượng Trả Về  : {avatar_size} bytes")
except Exception as e:
    print(f" -> Lỗi kết nối Render Live: {e}")

# ---------------------------------------------------------
# KẾT LUẬN NGUYÊN NHÂN GỐC RỄ
# ---------------------------------------------------------
print("\n===================================================")
print("             KẾT LUẬN NGUYÊN NHÂN GỐC RỄ            ")
print("===================================================")

if local_commit[:7] != (gh_commit[:7] if gh_commit else ""):
    print("❌ NGUYÊN NHÂN: Code chưa lên GitHub!")
    print("   -> Bạn chưa git push thành công hoặc bị nghẽn mạng.")
elif not gh_has_avatar:
    print("❌ NGUYÊN NHÂN: Tệp avatar.jpg KHÔNG TỒN TẠI trên GitHub!")
    print("   -> File bị .gitignore chặn hoặc chưa dùng lệnh 'git add -f public/avatar.jpg'.")
elif avatar_ct.startswith("text/html"):
    print("🚨 NGUYÊN NHÂN: ĐỊA CHỈ TRUY VẤN VẪN LÀ MÁY CHỦ CŨ (ĐANG BUILD)!")
    print("   -> GitHub đã nhận code, tệp ĐÃ CÓ trên Cloud.")
    print("   -> Render mất từ 90 - 150 giây để nhận Webhook -> Pull -> Build -> Restart Server.")
    print("   -> Việc kiểm tra ngay lập tức sau git push sẽ luôn trúng vào Server cũ chưa Restart.")
elif "image" in avatar_ct:
    print("✅ HOÀN HẢO: Máy chủ Render đã đồng bộ xong hoàn toàn bản build mới!")

print("===================================================")
