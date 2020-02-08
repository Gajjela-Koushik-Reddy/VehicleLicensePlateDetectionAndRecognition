from tkinter import messagebox
import tkinter
from tkinter import *
import numpy as np
import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
#path = ''
path = str(input("enter the image path: "))

def imag_read(path):
    image = cv2.imread(path)
    return image
def img_preprocessing(image):
    image = imutils.resize(image, width=500)
    cv2.imshow("Original Image", image)
    cv2.waitKey(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale", gray)
    cv2.waitKey(0)
    gray = cv2.bilateralFilter(gray,11,17,17)
    cv2.imshow("Bilateral filter",gray)
    cv2.waitKey(0)
    edged = cv2.Canny(gray, 170, 200)
    cv2.imshow("Canny edged", edged)
    cv2.waitKey(0)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)
    cv2.imshow("All contours", img1)
    cv2.waitKey(0)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)
    cv2.imshow("Top 30 contours", img2)
    cv2.waitKey(0)
    count = 0
    idx = 1
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx  # approx no plate contour

            #crop those contours and store it in cropped images folder
            x, y, w, h = cv2.boundingRect(c)  # this will find coords of plate
            new_img = image[y:y + h, x:x + w]  # create a new image
            cv2.imwrite('Cropped.png', new_img)  # store new image
            idx += 1

            break

    #Drawing the selected contour on the original image
    cv2.drawContours(image, [NumberPlateCnt], -1, (0, 255, 0), 3)
    cv2.imshow("Final image with number plate detected", image)
    cv2.waitKey(0)
    cropped_img_loc = 'Cropped.png'
    cv2.imshow("cropped Image", cv2.imread(cropped_img_loc))
    img_cnvted_img = cv2.imread("Cropped.png")
    cropped_image_gray = cv2.cvtColor(img_cnvted_img, cv2.COLOR_BGR2GRAY)
    gaus_smooth = cv2.bilateralFilter(cropped_image_gray, 11, 17, 17)
    cv2.imshow("Gassian_fikter", gaus_smooth)
    cv2.waitKey(0)

    invert = cv2.bitwise_not(gaus_smooth)
    cv2.imshow("canny", invert)
    return invert

def detect(imag):
    text = pytesseract.image_to_string(imag)
    return text


def process(path):
    img = imag_read(path)
    img2 = img_preprocessing(img)
    tex = detect(img2)
    print(tex)
    progress(tex)

    

#UI
top = tkinter.Tk()
top.title("LICENSE PLATE DETECTION APPLICATION")
canvas = Canvas(top, width=3000, height=500, bg="skyblue")


canvas.pack(expand=YES, fill=BOTH)
pi = PhotoImage(file="Ukraine123.png")
canvas.create_image(000, 000, image=pi, anchor=NW)


def progress(tex):
    print("Number is :", tex)
    cv2.waitKey(0)
    #print("WORK IN PROGRESS")
    messagebox.showinfo("Information",tex)

B = Button(top, text="DETECT", width=300, height=1, bg="skyblue",font=('Helvetica', '20'), command=process(path))
B.pack(side=RIGHT)
top.mainloop()


