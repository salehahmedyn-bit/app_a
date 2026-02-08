import os
import cv2
import numpy as np
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def image_to_css(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None: return False
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    with open(output_path, "w") as f:
        f.write(".pixel-art {\n  width: 1px;\n  height: 1px;\n  box-shadow:\n")
        pixels = [f"    {x+1}px {y+1}px rgb({img_rgb[y,x,0]},{img_rgb[y,x,1]},{img_rgb[y,x,2]})" 
                  for y in range(h) for x in range(w)]
        f.write(",\n".join(pixels) + ";\n}")
    return True

def css_to_image(input_path, output_path):
    with open(input_path, 'r') as f:
        content = f.read()
    pattern = r"(\d+)px\s+(\d+)px\s+rgb\((\d+),(\d+),(\d+)\)"
    pixels = re.findall(pattern, content)
    if not pixels: return False
    max_x = max(int(p[0]) for p in pixels)
    max_y = max(int(p[1]) for p in pixels)
    img = np.zeros((max_y + 1, max_x + 1, 3), dtype=np.uint8)
    for x, y, r, g, b in [map(int, p) for p in pixels]:
        img[y, x] = [b, g, r]
    cv2.imwrite(output_path, img)
    return True

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("in.png")
        if image_to_css("in.png", "out.txt"):
            await update.message.reply_document(document=open("out.txt", "rb"), filename="pixel_art.txt")
            
    elif update.message.document and update.message.document.file_name.endswith(".txt"):
        file = await update.message.document.get_file()
        await file.download_to_drive("in.txt")
        if css_to_image("in.txt", "out.png"):
            await update.message.reply_photo(photo=open("out.png", "rb"))

if __name__ == '__main__':
    if not TOKEN:
        exit(1)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, handle_msg))
    app.run_polling()
