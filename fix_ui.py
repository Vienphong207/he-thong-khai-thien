import re

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Chèn CSS Kính Mờ & Focus Mode vào trước </head>
custom_css = """
<style>
  /* 1. Khung đen thành Kính Mờ xuyên thấu nhìn rõ Dị Cảnh */
  div[class*="bg-"], div[class*="card"], main > div, .max-w-md {
    background: rgba(15, 23, 42, 0.35) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
  }

  /* 2. Chế độ Thu Gọn chỉ chừa nút Vận Hành Thần Thức */
  .focus-active {
    background: transparent !important;
    border: none !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
  }
  .focus-active .hide-on-focus {
    opacity: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: none !important;
    transition: all 0.4s ease !important;
  }
</style>
"""

if "</head>" in html and "custom_css" not in html:
    html = html.replace("</head>", f"{custom_css}\n</head>")

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Đã nâng cấp Giao diện Kính Mờ & Chế độ Thu Gọn!")
