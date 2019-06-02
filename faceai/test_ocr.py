# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract

path = "data/text-img.png"
text = pytesseract.image_to_string(Image.open(path), lang='chi_sim')
print(text)