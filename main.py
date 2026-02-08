import cv2
import numpy as np

# 1. تحميل الصورة الأصلية
img = cv2.imread("fdss.png")

# 2. إعداد القناع والمصفوفات لخوارزمية GrabCut
mask = np.zeros(img.shape[:2], np.uint8)
bg = np.zeros((1, 65), np.float64)
fg = np.zeros((1, 65), np.float64)

# 3. تحديد المستطيل المحيط بالكائن (نفس إحداثيات الصورة)
rect = (10, 10, img.shape[1]-20, img.shape[0]-20)

# 4. تشغيل خوارزمية العزل
cv2.grabCut(img, mask, rect, bg, fg, 5, cv2.GC_INIT_WITH_RECT)

# 5. تحويل القناع إلى قيم ثنائية (0 للخلفية و 1 للمقدمة)
mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')

# 6. إضافة قناة الشفافية (Alpha Channel)
# نقوم بضرب القناع في 255 لتحويل القيم من (0 و 1) إلى (0 و 255)
alpha = mask2 * 255

# 7. فصل قنوات الألوان الأصلية (B, G, R) ودمجها مع قناة ألفا الجديدة
b_channel, g_channel, r_channel = cv2.split(img)
result = cv2.merge((b_channel, g_channel, r_channel, alpha))

# 8. حفظ الصورة النهائية بصيغة PNG لدعم الشفافية
cv2.imwrite("output_transparent.png", result)
