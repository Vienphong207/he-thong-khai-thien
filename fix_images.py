import os
from PIL import Image, ImageEnhance, ImageFilter

print("⚡ Đang làm nét 4 Đại Dị Cảnh...")
for i in range(1, 5):
    file_path = f"public/bg{i}.jpg"
    if os.path.exists(file_path):
        img = Image.open(file_path)
        
        # Phóng to gấp 3 lần bằng thuật toán Lanczos
        new_size = (img.width * 3, img.height * 3)
        img_upscaled = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Khử mờ và tăng độ sắc nét
        img_sharp = img_upscaled.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        enhancer_sharp = ImageEnhance.Sharpness(img_sharp)
        img_final = enhancer_sharp.enhance(1.8)
        
        # Tăng nhẹ độ tương phản
        enhancer_contrast = ImageEnhance.Contrast(img_final)
        img_final = enhancer_contrast.enhance(1.1)
        
        img_final.save(file_path, "JPEG", quality=95)
        size_kb = round(os.path.getsize(file_path) / 1024, 1)
        print(f"✅ bg{i}.jpg -> Khổ mới: {img_final.size[0]}x{img_final.size[1]} px | Dung lượng: {size_kb} KB")
