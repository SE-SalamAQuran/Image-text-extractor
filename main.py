import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract"
print(pytesseract.image_to_string(r"./a.PNG"))

arr = cv2.imread("a.png")
print(arr)
with open("Cover-letter.txt", "w") as f:
    print(pytesseract.image_to_string(r"./cover-letter.PNG"), file=f)
    

