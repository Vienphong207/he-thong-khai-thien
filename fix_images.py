import os
from PIL import Image, ImageEnhance, ImageFilter

print("⚡ Đang kích hoạt Trận Pháp Làm Nét Ảnh...")

for i in range(1, 5):
    file_path = f"public/bg{i}.jpg"
    if os.path.exists(file_path):
        img = Image.open(file_path)
        
        # Tăng gấp 3 lần kích thước ảnh bằng thuật toán Lanczos (chống vỡ hình)
        new_size = (img.width * 3, img.height * 3)
        img_upscaled = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Áp dụng bộ lọc làm nét sâu (Unsharp Mask)
        img_sharp = img_upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        # Tăng cường độ tương phản và độ sắc nét
        enhancer_sharp = ImageEnhance.Sharpness(img_sharp)
        img_final = enhancer_sharp.enhance(1.8)
        
        enhancer_contrast = ImageEnhance.Contrast(img_final)
        img_final = enhancer_contrast.enhance(1.1)
        
        # Lưu đè lại ảnh với chất lượng cao nhất (Quality 95)
        img_final.save(file_path, "JPEG", quality=95)
        print(f"✅ Đã tối ưu xong: bg{i}.jpg -> Kích thước mới: {img_final.size}")

print("✨ Hoàn tất tối ưu toàn bộ Dị Cảnh!")
