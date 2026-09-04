import os
import glob
import base64
import json

print("🔍 Đang truy xuất hình ảnh Phật Ma Đồng Thể...")

patterns = [
    "/sdcard/Download/*.jpg", "/sdcard/Download/*.jpeg", "/sdcard/Download/*.png", "/sdcard/Download/*.webp",
    "/sdcard/Pictures/*.jpg", "/sdcard/Pictures/*.jpeg", "/sdcard/Pictures/*.png",
    "./*.jpg", "./*.png"
]

files = []
for p in patterns:
    files.extend(glob.glob(p))

b64_img = ""
if files:
    files.sort(key=os.path.getmtime, reverse=True)
    target_img = files[0]
    print(f"✅ Đã tìm thấy linh ảnh Phật Ma: {target_img}")
    with open(target_img, "rb") as f:
        img_bytes = f.read()
    ext = os.path.splitext(target_img)[1].lower()
    mime = "image/png" if ext == ".png" else "image/webp" if ext == ".webp" else "image/jpeg"
    b64_img = f"data:{mime};base64," + base64.b64encode(img_bytes).decode('utf-8')
    
    os.makedirs("public", exist_ok=True)
    with open("public/avatar.jpg", "wb") as f:
        f.write(img_bytes)

# 5. Tạo PWA Manifest chuẩn (Tên ngắn: Hệ Thống)
manifest = {
  "name": "Hệ Thống Thần Cấp Toàn Năng",
  "short_name": "Hệ Thống",
  "description": "Trạm Trợ Lực Thần Thức - Viễn Phong",
  "start_url": "/?v=2026",
  "display": "standalone",
  "background_color": "#030712",
  "theme_color": "#030712",
  "icons": [
    { "src": "/avatar.jpg", "sizes": "192x192", "type": "image/jpeg" },
    { "src": "/avatar.jpg", "sizes": "512x512", "type": "image/jpeg" }
  ]
}

os.makedirs("public", exist_ok=True)
with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
with open("public/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# 6. Mã nguồn HTML Đại Trận Thần Cấp Mới
html_code = f'''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hệ Thống Thần Cấp Toàn Năng</title>
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" type="image/jpeg" href="/avatar.jpg">
  <meta name="theme-color" content="#030712">
  
  <!-- TỰ ĐỘNG DIỆT CLEAN CACHE CŨ NGHÊM NGHẶT -->
  <script>
    if ('serviceWorker' in navigator) {{
      navigator.serviceWorker.getRegistrations().then(regs => {{
        for(let r of regs) r.unregister();
      }});
    }}
    if ('caches' in window) {{
      caches.keys().then(keys => {{
        for(let k of keys) caches.delete(k);
      }});
    }}
  </script>

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background: #030712; color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
      overflow: hidden; position: relative;
    }}
    
    .bg-layer {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background-image: radial-gradient(circle at 50% 30%, rgba(168, 85, 247, 0.25), transparent 70%),
                        radial-gradient(circle at 50% 80%, rgba(234, 179, 8, 0.2), transparent 70%),
                        url('{b64_img}');
      background-size: cover; background-position: center;
      filter: blur(20px) brightness(0.4); transform: scale(1.1); z-index: 0;
    }}

    #magic-canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}

    .main-card {{
      position: relative; z-index: 10;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
      border: 1px solid rgba(234, 179, 8, 0.5);
      border-radius: 32px; padding: 40px 24px; max-width: 440px; width: 92%;
      text-align: center;
      box-shadow: 0 0 70px rgba(168, 85, 247, 0.35), inset 0 0 25px rgba(56, 189, 248, 0.15);
    }}

    .avatar-container {{
      position: relative; width: 160px; height: 160px; margin: 0 auto 24px;
      display: flex; align-items: center; justify-content: center;
    }}

    .aura-ring {{
      position: absolute; top: -14px; left: -14px; right: -14px; bottom: -14px;
      border-radius: 50%;
      background: conic-gradient(from 0deg, #eab308, #a855f7, #ec4899, #38bdf8, #eab308);
      animation: spinAura 5s linear infinite; filter: blur(12px); opacity: 0.95;
    }}

    @keyframes spinAura {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

    .avatar-frame {{
      position: relative; z-index: 2; width: 100%; height: 100%;
      border-radius: 50%; border: 3px solid #fef08a; background: #030712;
      overflow: hidden; display: flex; align-items: center; justify-content: center;
      box-shadow: 0 0 30px rgba(234, 179, 8, 0.8);
    }}

    .avatar-frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}

    .title-main {{
      font-size: 22px; font-weight: 900; letter-spacing: 2px;
      background: linear-gradient(135deg, #fef08a 0%, #eab308 35%, #c084fc 70%, #38bdf8 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      margin-bottom: 16px; text-shadow: 0 0 25px rgba(234, 179, 8, 0.4);
      text-transform: uppercase;
    }}

    .greeting-box {{
      background: rgba(2, 6, 23, 0.65);
      border: 1px solid rgba(192, 132, 252, 0.3);
      border-radius: 18px; padding: 16px 18px; margin-bottom: 22px;
      font-size: 14px; line-height: 1.6; color: #e2e8f0;
      font-style: italic; box-shadow: inset 0 0 15px rgba(168, 85, 247, 0.2);
    }}

    .highlight-text {{ color: #fef08a; font-weight: 700; font-style: normal; }}

    .status-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 20px; background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.4); color: #38bdf8;
      border-radius: 30px; font-size: 13px; font-weight: 700; margin-bottom: 20px;
    }}

    .pulse-dot {{ width: 8px; height: 8px; background: #34d399; border-radius: 50%; box-shadow: 0 0 12px #34d399; }}

    .btn-action {{
      background: linear-gradient(135deg, #6b21a8, #0369a1);
      border: 1px solid #eab308; color: #ffffff; padding: 14px 28px;
      border-radius: 18px; font-size: 14px; font-weight: 800; cursor: pointer;
      box-shadow: 0 6px 30px rgba(168, 85, 247, 0.5); transition: all 0.2s ease;
      width: 100%;
    }}

    .btn-action:active {{ transform: scale(0.96); }}
  </style>
</head>
<body>
  <div class="bg-layer"></div>
  <canvas id="magic-canvas"></canvas>

  <div class="main-card">
    <div class="avatar-container">
      <div class="aura-ring"></div>
      <div class="avatar-frame">
        {"<img src='" + b64_img + "' alt='Phật Ma Đồng Thể'>" if b64_img else "<div style='color:#fef08a;font-weight:bold;'>PHẬT MA<br>ĐỒNG THỂ</div>"}
      </div>
    </div>

    <div class="title-main">HỆ THỐNG THẦN CẤP TOÀN NĂNG</div>

    <div class="greeting-box">
      "Đạo hữu, chào mừng đến với thế giới của những kẻ mạnh, <span class="highlight-text">Tiểu Phong</span> luôn sẵn sàng đồng hành thăng cấp cùng ngươi!"
    </div>

    <div class="status-badge">
      <span class="pulse-dot"></span> Thần Thức Kết Nối • Viễn Phong
    </div>

    <div id="scene-text" style="font-size:13px; color:#c084fc; font-weight:700; margin-bottom:14px;">
      ☯️ Kỳ Cảnh: Phật Ma Lưỡng Nghi Trận
    </div>

    <button class="btn-action" onclick="toggleMagic()">⚔️ VẬN HÀNH THẦN THỨC</button>
  </div>

  <script>
    const canvas = document.getElementById('magic-canvas');
    const ctx = canvas.getContext('2d');
    function resize() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
    window.addEventListener('resize', resize); resize();

    let mode = 0;
    const modes = [
      "☯️ Kỳ Cảnh: Phật Ma Lưỡng Nghi Trận",
      "⚔️ Kỳ Cảnh: Vạn Kiếm Quy Tông (Kiếm Khí)",
      "🏔️ Kỳ Cảnh: Tiên Sơn Tử Khí Hoàng Kim",
      "🔥 Kỳ Cảnh: Thái Cổ Lôi Độc Thần Hỏa"
    ];

    function toggleMagic() {{
      mode = (mode + 1) % 4;
      document.getElementById('scene-text').innerText = modes[mode];
    }}

    const particles = Array.from({{ length: 90 }}, () => ({{
      x: Math.random() * window.innerWidth, y: Math.random() * window.innerHeight,
      size: Math.random() * 3.5 + 1, speedX: (Math.random() - 0.5) * 1.8, speedY: (Math.random() - 0.5) * 1.8,
      length: Math.random() * 45 + 15
    }}));

    function draw() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const cx = canvas.width / 2;

      particles.forEach(p => {{
        if (mode === 0) {{
          p.x += p.speedX * 0.6; p.y += p.speedY * 0.6;
          ctx.fillStyle = p.x < cx ? 'rgba(234, 179, 8, 0.7)' : 'rgba(168, 85, 247, 0.7)';
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
        }} else if (mode === 1) {{
          p.y -= 4;
          if (p.y < -20) p.y = canvas.height + 20;
          ctx.strokeStyle = 'rgba(56, 189, 248, 0.7)'; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x, p.y + p.length); ctx.stroke();
        }} else if (mode === 2) {{
          p.y -= 1.2;
          if (p.y < 0) p.y = canvas.height;
          ctx.fillStyle = 'rgba(251, 191, 36, 0.8)';
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size * 1.3, 0, Math.PI * 2); ctx.fill();
        }} else {{
          p.y -= 3; p.x += (Math.random() - 0.5) * 5;
          if (p.y < 0) p.y = canvas.height;
          ctx.fillStyle = Math.random() > 0.5 ? '#f97316' : '#a855f7';
          ctx.beginPath(); ctx.arc(p.x, p.y, p.size * 1.6, 0, Math.PI * 2); ctx.fill();
        }}

        if (p.x < 0) p.x = canvas.width; if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height; if (p.y > canvas.height) p.y = 0;
      }});

      requestAnimationFrame(draw);
    }}
    draw();
  </script>
</body>
</html>'''

# Ghi file html vao ca root va public
with open("index.html", "w", encoding="utf-8") as f: f.write(html_code)
with open("public/index.html", "w", encoding="utf-8") as f: f.write(html_code)

# 7. Tao file server Node.js va package.json cho Render
server_js = '''const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 10000;

http.createServer((req, res) => {
  let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
  if (!fs.existsSync(filePath)) filePath = path.join(__dirname, 'index.html');
  
  const ext = path.extname(filePath);
  let contentType = 'text/html';
  if (ext === '.js') contentType = 'text/javascript';
  if (ext === '.css') contentType = 'text/css';
  if (ext === '.json') contentType = 'application/json';
  if (ext === '.png') contentType = 'image/png';
  if (ext === '.jpg') contentType = 'image/jpeg';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(500); res.end('Server Error');
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
}).listen(PORT, () => console.log('Server running on port ' + PORT));
'''

package_json = '''{
  "name": "he-thong-than-cap",
  "version": "2.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "build": "echo 'Build Complete'"
  }
}'''

with open("server.js", "w", encoding="utf-8") as f: f.write(server_js)
with open("package.json", "w", encoding="utf-8") as f: f.write(package_json)

print("✨ Tải tạo mã nguồn Hệ Thống Thần Cấp thành công!")
