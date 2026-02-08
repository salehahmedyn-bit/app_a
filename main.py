import cv2
import numpy as np

# 1. تحميل الصورة
img = cv2.imread("fdss.png")
# ملاحظة: يفضل تصغير الصورة إذا كانت كبيرة جداً لأن CSS سيتجمد مع آلاف البكسلات
# img = cv2.resize(img, (50, 50)) 

# 2. تحويل الصورة من BGR (الافتراضي في OpenCV) إلى RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

height, width, _ = img.shape

# 3. فتح ملف نصي لحفظ الكود
with open("pixel_art_css.txt", "w") as f:
    f.write(".pixel-art {\n")
    f.write("  width: 1px;\n")
    f.write("  height: 1px;\n")
    f.write("  box-shadow:\n")

    shadows = []
    
    # 4. الدوران على كل بكسل واستخراج إحداثياته ولونه
    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb[y, x]
            
            # تنسيق بكسل واحد: x-offset y-offset color
            # نستخدم x+1 و y+1 لتجنب الصفر
            pixel_css = f"    {x+1}px {y+1}px rgb({r},{g},{b})"
            shadows.append(pixel_css)

    # 5. دمج كل البكسلات بفاصلة وكتابتها
    f.write(",\n".join(shadows))
    f.write(";\n}")

print("تم بنجاح! افتح ملف pixel_art_css.txt لنسخ الكود.")
