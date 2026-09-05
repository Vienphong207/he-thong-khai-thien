import json, os, subprocess

# 1. Kiểm tra file package.json xem Render dùng lệnh gì để start
print("=== 1. KIỂM TRA ENTRY POINT TRONG PACKAGE.JSON ===")
if os.path.exists("package.json"):
    with open("package.json", "r", encoding="utf-8") as f:
        pkg = json.load(f)
    main_file = pkg.get("main", "index.js")
    start_cmd = pkg.get("scripts", {}).get("start", "")
    print(f" -> Main file : {main_file}")
    print(f" -> Start cmd : {start_cmd}")
    
    # Sửa start script đảm bảo trỏ đúng server.js
    pkg["scripts"] = pkg.get("scripts", {})
    pkg["scripts"]["start"] = "node server.js"
    pkg["main"] = "server.js"
    with open("package.json", "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2)
    print(" ✅ Đã chuẩn hóa package.json trỏ chuẩn vào node server.js!")

# 2. Tạo endpoint /version & /debug-dir trong server.js để vắt sạch thông tin từ Render
server_code = """const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();

const publicPath = path.join(__dirname, 'public');

// Route kiểm tra phiên bản mã nguồn đang sống trên Render
app.get('/version', (req, res) => {
    res.json({
        status: "LIVE_V3",
        time: new Date().toISOString(),
        public_exists: fs.existsSync(publicPath),
        files_in_public: fs.existsSync(publicPath) ? fs.readdirSync(publicPath) : []
    });
});

// Route phục vụ Avatar ưu tiên
app.get(['/avatar.jpg', '/avatar.png', '/avatar.jpeg', '/Avatar.jpg'], (req, res) => {
    if (fs.existsSync(publicPath)) {
        const files = fs.readdirSync(publicPath);
        const avatar = files.find(f => f.toLowerCase().startsWith('avatar'));
        if (avatar) {
            return res.sendFile(path.join(publicPath, avatar));
        }
    }
    res.status(404).send('Avatar missing in container');
});

app.use(express.static(publicPath));

app.get('*', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on ${PORT}`));
"""

with open("server.js", "w", encoding="utf-8") as f:
    f.write(server_code)

print(" ✅ Đã tiêm Route /version chẩn đoán sống vào server.js!")
