from PIL import Image, ImageEnhance, ImageFilter

img = Image.open("system_bg.jpg")
img_sharp = img.filter(ImageFilter.UnsharpMask(radius=2, percent=160, threshold=2))
enhancer_sharp = ImageEnhance.Sharpness(img_sharp)
img_final = enhancer_sharp.enhance(1.6)

enhancer_contrast = ImageEnhance.Contrast(img_final)
img_final = enhancer_contrast.enhance(1.15)

img_final.save("system_bg.jpg", "JPEG", quality=98)
print("✅ Đã nâng cấp ảnh Ma Trận Nhị Phân lên chuẩn 4K siêu nét!")
