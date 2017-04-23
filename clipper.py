#! /usr/bin/env python

import os
import sys

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# Parameters =====================================================================
# File parameters
image_format="png"
filename_prefix="clipped_"
try:
    input_directory=sys.argv[1]
    if input_directory[:6]=="--dir=":
        directory=input_directory[6:]
        if directory[-1]!='/':
            directory+='/'
    else:
        print("Invalid label!")
except:
    directory="./data/"
# Window parameters
window_size=14
x=y=100                        # default position of the cursor  
height_to_width_ratio=2.0/1    # height-to-width ratio of the clipping box
width=270                      # width of the clipping box
height=height_to_width_ratio*width
step=5                         # speed of moving the image or changing the size
right_to_left_ratio=2          # the x-axis position of the person in the clipping box
body_to_head_ratio=8           # the y-axis position of the person in the clipping obx

# Variable ===================================================================
crop_img=[]

# Class and function ==============================================================
class Clipper:
    # Catch mouse event or key-press event
    # Clip and save the image
    def __init__(self,ax,img,fileName):
        # Catch events
        self.cod = plt.figure(1).canvas.mpl_connect('scroll_event', self)
        self.cud = plt.figure(1).canvas.mpl_connect('button_press_event', self)
        self.ced = plt.figure(1).canvas.mpl_connect('key_press_event', self)
        self.ax = ax
        self.img = img
        self.fileName = fileName

    def __call__(self, event):
        # move the box and save the image
        global height_to_width_ratio, width, height
        global crop_img, x, y, step, directory

        try:
            button=event.button
        except:
            button=None
        key=event.key
        Ex=event.xdata
        Ey=event.ydata

        if key=="e":
            plt.close()
        if key=="q":
            exit()
        if key=="w" or button==3:
            mpimg.imsave(directory+"clipped_"+self.fileName[:-len("."+image_format)]+"."+image_format,crop_img)
            plt.close()

        if button==1:
            if Ex:
                x=Ex-width/right_to_left_ratio
                y=Ey-height/body_to_head_ratio
                crop_img = self.img[int(y):int(y + height), int(x):int(x + width)]
                plt.imshow(crop_img, extent=(-385, -385 + 270, 600, 120))
        if key=="up":   y=y-step
        if key=="down": y=y+step
        if key=="left": x=x-step
        if key=="right":x=x+step
        if key=="i" or button=="down":    width=width-step;   x=x-2;  height=width*height_to_width_ratio
        if key=="o" or button=="up":    width=width+step;   y=y-2;  height=width*height_to_width_ratio

        try:    self.ax.lines.pop(0)
        except: pass
        lines=self.ax.plot([x,x+width,x+width,x,x],[y,y,y+height,y+height,y],"b")
        
        if key!="e" and key!="q" and key!="w" and button!=3:
            plt.figure(1).canvas.draw()


def clip(fileName):
    # Initiate the figure and plot
    # Show the help
    img=mpimg.imread(os.path.join(directory,fileName))

    fig=plt.figure(figsize=(window_size,float(window_size)/14*9),subplotpars=matplotlib.figure.SubplotParams(left=0.05,right=0.95,top=0.9,bottom=0.1))
    fig.set_size_inches(window_size,float(window_size)/14*9)
    ax=fig.add_subplot(111)
    ax.set_title(fileName)
    plt.xlim(-500,len(img[1]))
    plt.ylim(len(img),0)
    ax.imshow(img)
    # Show the help
    ax.text(-480, 800, '"Left Click": clip the picture', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 860, '"Direction Keys": move clipping box', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 920, 'Mouse Wheel: zoom the clipping box', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 980, '"i" & "o": zoom the clipping box', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 1040, '"Right Click": save clipped picture', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 1100, '"q": quit the program', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    ax.text(-480, 1160, '"e": skip this picture', style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 6})
    clipper = Clipper(ax,img,fileName)
    plt.show()

# main ========================================================================
startFile=raw_input("The file to start with('0' for default): ")
list=os.listdir(directory)
for file in list:
    if file==startFile or startFile=="0":
        startFile="0"
        if file[-len("."+image_format):]=="."+image_format:
            if file[:len(filename_prefix)]!=filename_prefix:
                clip(file)
