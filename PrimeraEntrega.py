# Primera entrega parcial
# Visión para robots
# Prof. Gabriel González Sahagún

# A01196642 Ernesto Cervantes Juárez
# A00820188 Eduardo Angulo Martínez
# A00821541 Miguel Morales de la Vega
# A00820662 Sergio Canto Arizpe
# A01196642 Ernesto Cervantes Juárez

import numpy as np
import cv2 as cv

coords = []

def click(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        coords.append((x,y))
        if len(coords) == 2:
            submatrix = img[coords[0][0] : coords[1][0], coords[0][1] : coords[1][1]]
            print("min:", np.amin(submatrix))
            print("max:", np.amax(submatrix))
            print("median:", '{:.3f}'.format(np.median(submatrix)))
            print("average:", '{:.3f}'.format(np.average(submatrix)))
            print("std dev:", '{:.3f}'.format(np.std(submatrix)))
            cv.destroyAllWindows()

# Punto 6
img = cv.imread('gundam.jpg')
img2 = cv.resize(img, (540, 540))
img = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
cv.imshow('original', img)
cv.setMouseCallback('original', click)
cv.waitKey(0)

# Punto 7
_, binimg = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
cv.imshow('binarizada', binimg)
cv.waitKey(0)
