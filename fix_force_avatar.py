import os, json, re

# 1. Chuẩn hóa server.js với Route ưu tiên tuyệt đối cho Avatar
server_js = """const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();

const publicPath = path.join(__dirname, 'public');

// Phục vụ tĩnh public
app.use(express.static(publicPath));

# Route quét trực tiếp avatar chấp nhận mọi kiểu viết hoa/thường
app.get(['/avatar.jpg', '/avatar.png', '/avatar.jpeg', '/Avatar.jpg'], (req, res) => {
    try {
        if (fs.existsSync(publicPath)) {
            const files = fs.readdirSync(publicPath);
            const avatarFile = files.find(f => f.toLowerCase().startsWith('avatar'));
            if (avatarFile) {
                return res.sendFile(path.join(publicPath, avatarFile));
            }
        }
        res.status(404).send('Avatar file missing on disk');
    } catch (err) {
        res.status(500).send(err.message);
    }
});

// Catch-all route cho SPA
app.get('*', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
"""

with open("server.js", "w", encoding="utf-8") as f:
    f.write(server_js)

print("-> Đã tiêm Route ưu tiên bắt tệp Avatar vào server.js!")
