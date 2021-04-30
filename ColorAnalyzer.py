import sys
import cv2
import numpy as np

#This class was written in order to detect the images' backgrounds, i.e: white / black bg
#Because our program worked fine for images with white bgs at first but not at all for images with black bgs
#Eventually, after the going through the openCV documentation we found out that our binarization, i.e: threshholding was incorrect.


class ColorAnalyzer():
    def __init__(self, imageLoc):
        self.src = cv2.imread(imageLoc, 1)
        self.colors_count = {}
    
    def count_colors(self):
        (channel_b, channel_g, channel_r) = cv2.split(self.src)
        channel_b = channel_b.flatten()
        channel_g = channel_g.flatten()
        channel_r = channel_r.flatten()

        for i in range(len(channel_b)):
            
            RGB = "(" + str(channel_r[i]) + "," + str(channel_g[i]) + "," + str(channel_b[i]) + ")"

            if RGB in self.colors_count:
                self.colors_count[RGB] +=1
            else:
                self.colors_count[RGB] = 1
        print("Colors counted!")

    def show_colors(self):
        for keys in sorted(self.colors_count, key=self.colors_count.__getitem__):
            print(keys, ": " + self.colors_count[keys])
    
