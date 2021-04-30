import cv2
import numpy as np
import os




def stack_images(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_ava = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_ava:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape [:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]), None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y]= cv2.cvtColor( img_array[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank]*rows
        hor_con = [image_blank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None,scale, scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(img_array)
        ver = hor
    return ver

# Read The input image
path = "dataset//ahte_train_pixel_label/book1_page19.png"
img = cv2.imread(path)
imgDraw = cv2.imread(path)
# Convert the image to gray scale
imgGray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)




# Blureing the image using kernel
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 0)


#image_binarization
ret, thresh1 = cv2.threshold(imgBlur, 0, 255, cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU )



    
# declare a kernel
kernel = np.ones((3, 4), np.int8)

#morpology
img_morpo = cv2.morphologyEx(imgGray, op=cv2.MORPH_ERODE,  kernel=kernel)

# Apply erosion
img_erosion = cv2.erode(thresh1, kernel, iterations=6, borderType=0, borderValue=255)

# Apply dilation
img_dilation = cv2.dilate(thresh1, kernel, iterations=4, borderType=1 ,borderValue=0)
blur2 = cv2.GaussianBlur(img_erosion, (1, 1), 0)

# draw a rectangle around the paragraph
cnts = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

# select the paragraphs in hand line
cntsDraw = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cntsDraw = cntsDraw[0] if len(cntsDraw) == 2 else cntsDraw[1]

for c in cntsDraw:
    cv2.drawContours(imgDraw, c, -1, (0, 255, 0), 4)


# Resize the image
imgResult = cv2.resize(img, (int(img.shape[1]*0.3), int(img.shape[0]*0.3)))
imgDraw = cv2.resize(imgDraw, (int(imgDraw.shape[1]*0.3), int(imgDraw.shape[0]*0.3)))
myblur = cv2.resize(imgBlur, (int(imgBlur.shape[1]*0.3), int(imgBlur.shape[0]*0.3)))
# join more than one figure with many channel
imgStack = stack_images(1, ([img, imgDraw, imgBlur],[img_erosion,img_dilation,imgGray]))



# cv2.absdiff(img, mask, "out.png")
cv2.imshow('Output draw', imgDraw)
cv2.imwrite("output.png", imgDraw)
cv2.waitKey(0)
cv2.destroyAllWindows()