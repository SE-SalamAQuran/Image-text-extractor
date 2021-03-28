import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract"
print(pytesseract.image_to_string(r"./h.png"))
lang = pytesseract.get_languages()
print(lang)
ar = lang.__getitem__(1)
pytesseract.image_to_string(r"./h.PNG", lang=ar)
