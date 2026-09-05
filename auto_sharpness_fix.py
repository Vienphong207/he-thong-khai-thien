import os
import urllib.request
import numpy as np
from PIL import Image, ImageFilter

# Danh sách URL nguồn ảnh Dị Cảnh / Tiên Hiệp 4K chất lượng cao
SCENERY_4K_URLS = [
    "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop", # bg1: Sơn phong sương mỏng
    "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=2000&auto=format&fit=crop", # bg2: Dị cảnh sông núi
    "https://images.unsplash.com/photo-1511497584788-8767611136f0?q=80&w=2000&auto=format&fit=crop", # bg3: Lên mây ngàn đỉnh
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=2000&auto=format&fit=crop"  # bg4: Tĩnh không tịch mịch
]

def check_sharpness_score(img_path):
    """Tính chỉ số sắc nét dựa trên mật độ và độ tương phản của đường biên (Edge Variance)"""
    img = Image.open(img_path).convert('L')
    edges = img.filter(ImageFilter.FIND_EDGES)
    edge_array = np.array(edges)
    return np.var(edge_array)

print("==================================================")
print(" 🔍 ĐANG KIỂM TRA CHỈ SỐ ĐỘ NẾT DỊ CẢNH (THRESHOLD = 150)")
print("==================================================")

for i in range(1, 5):
    path = f"public/bg{i}.jpg"
    if os.path.exists(path):
        score = check_sharpness_score(path)
        print(f"📊 bg{i}.jpg => Chỉ số sắc nét: {score:.1f}")
        
        # Ngưỡng sắc nét chuẩn (Nếu < 150 là ảnh mờ/vỡ pixel)
        if score < 150:
            print(f"⚠️ Phát hiện bg{i}.jpg bị vỡ/mờ! Đang kích hoạt tự động tải ảnh Dị Cảnh 4K...")
            try:
                urllib.request.urlretrieve(SCENERY_4K_URLS[i-1], path)
                new_score = check_sharpness_score(path)
                print(f"✅ Đã khắc phục thành công bg{i}.jpg! Chỉ số nét mới: {new_score:.1f}")
            except Exception as e:
                print(f"❌ Lỗi khi tải ảnh mới: {e}")
        else:
            print(f"✨ bg{i}.jpg đạt tiêu chuẩn sắc nét!")
    else:
        print(f"❌ Không tìm thấy {path}")

print("==================================================")
