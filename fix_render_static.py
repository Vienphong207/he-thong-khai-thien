import os, json, re

# 1. Kiểm tra và sửa .gitignore nếu vô tình chặn file ảnh
gitignore_path = ".gitignore"
if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        git_content = f.read()
    # Xóa các dòng chặn jpg/png/public
    new_git = re.sub(r'(\*\.jpg|\*\.png|public/avatar.*)', '', git_content)
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(new_git)

# 2. Tìm file avatar thực tế
public_dir = "public"
img_file = None
for f in os.listdir(public_dir):
    if f.lower().startswith("avatar") or f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        img_file = f
        break

if not img_file:
    print("❌ Không tìm thấy file avatar nào trong thư mục public!")
    exit(1)

print(f"-> Đã xác nhận file avatar thực tế: public/{img_file}")

# 3. Chuẩn hóa server.js để trả đúng Content-Type static
server_js = """const express = require('express');
const path = require('path');
const app = express();

// Phục vụ thư mục public làm static files
app.use(express.static(path.join(__dirname, 'public')));

// Trả về index.html cho các route còn lại
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
"""

with open("server.js", "w", encoding="utf-8") as f:
    f.write(server_js)

print("-> Đã tối ưu cấu hình server.js!")
