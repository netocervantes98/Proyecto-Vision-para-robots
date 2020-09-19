# Primera entrega parcial - Histograma
# Visión para robots
# Prof. Gabriel González Sahagún

# A01196642 Ernesto Cervantes Juárez
# A00823445 Jesus Francisco Anaya Gonzalez
# A00820662 Sergio Alejandro Canto Arizpe 
# A00821541 Miguel Alejandro Morales de la Vega
# A00820188 Eduardo Angulo Martínez

import cv2 as cv
import numpy as np
from copy import copy

#Variables globales
img_path = 'gundam.jpg'

#Colores
color_azul  = (255,0,0)
color_verde = (0,255,0)
color_rojo  = (0,0,255)
color_click = (0,0,0)

#Tamaño de grafica
n = 540
m = 560
iniciox = 20
finx = 545
inicioy = 40
finy = 515

#Variables auxiliares
blue_image = np.zeros([n, m, 3], dtype=np.uint8)
red_image = np.zeros([n, m, 3], dtype=np.uint8)
green_image = np.zeros([n, m, 3], dtype=np.uint8)
clean_blue = 0
clean_red = 0
clean_green = 0

#Rutina para calcular las frequencias y mapear de frequencias a alturas.
def CalcFreq(arr):
    ans = np.zeros(256, dtype=int)
    for x in arr:
        ans[x] += 1
    global maxi
    maxi = max(ans)
    for i in range(len(ans)):
        ans[i] = int(ans[i] * (finy - inicioy) / maxi)
    return ans

#Crear rutina para el mouse
def click_event(event, x, y, flags, param):
    global blue_image, green_image, red_image, clean_blue, clean_red, clean_green, img
    if event == cv.EVENT_LBUTTONDOWN:
        #Obtener colores de la imagen para pintar en el histograma.
        colorsB = img[y,x,0]
        colorsG = img[y,x,1]
        colorsR = img[y,x,2]
        colors = img[y,x]
        #Seleccionar pixel en la imagen y dibujar circulo sobre el.
        if colorsB > 130 and colorsG > 130 and colorsR > 130:
            color_circulo = [0,0,0]
        else:
            color_circulo = [255, 255, 255]
        img2 = copy(img)
        img = cv.circle(img, (x, y), 5, color_circulo, 2)
        print("BRG Format: ",colors)
        # pintar azul
        drawRectangle(blue_image, (iniciox+2) + clean_blue * 2, color_blue_frequency[clean_blue], color_azul)
        drawRectangle(blue_image, (iniciox+2) + colorsB * 2, color_blue_frequency[colorsB], color_rojo)
        clean_blue = colorsB
        # pintar verde.
        drawRectangle(green_image, (iniciox+2) + clean_green * 2, color_green_frequency[clean_green], color_verde)
        drawRectangle(green_image, (iniciox+2) + colorsG * 2, color_green_frequency[colorsG], (0,0,0))
        clean_green = colorsG
        # pintar rojo.
        drawRectangle(red_image, (iniciox+2) + clean_red * 2, color_red_frequency[clean_red], color_rojo)
        drawRectangle(red_image, (iniciox+2) + colorsR * 2, color_red_frequency[colorsR], color_azul)
        clean_red = colorsR
        #Mostrar imagenes
        cv.imshow('original', img)
        cv.imshow('blue_histogram', blue_image)
        cv.imshow('green_histogram', green_image)
        cv.imshow('red_histogram', red_image)
        img = copy(img2)


#Dibujar un rectangulo de altura h con base en el punto x1.
def drawRectangle(mat, x1, h, color):
    for x in range(x1, x1+1):
        for y in range(finy, finy-h, -1):
            mat[y][x] = color

#Crear un histograma recorriendo las alturas dadas.
def createImage(name, color_, arr):
    #Crear imagen blanca
    mat = np.zeros([n, m, 3], dtype=np.uint8)
    mat.fill(255)
    #Titulo
    # Eje (x, y)
    cv.arrowedLine(mat, (iniciox, finy), (finx, finy), color=1, tipLength=0.02)
    cv.arrowedLine(mat, (iniciox, finy), (iniciox, inicioy), color=1, tipLength=0.02)
    cv.putText(mat, "max = " + str(maxi), (200, 40), cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color = color_)
    #dibujar rectangulos
    for x in range(256):
            drawRectangle(mat,(iniciox+2) + x * 2,arr[x], color_)
    cv.imshow(name, mat)
    return mat

#Leer imagen y cambiar tamaño.
img = cv.imread(img_path)
img = cv.resize(img, (540, 540))

#Obtener frequencias de colores y crear histogramas
color_blue_frequency = CalcFreq(img[:,:,0].flatten().tolist())
blue_image = createImage('blue_histogram', color_azul, color_blue_frequency)

color_green_frequency = CalcFreq(img[:,:,1].flatten().tolist())
green_image = createImage('green_histogram', color_verde, color_green_frequency)

color_red_frequency = CalcFreq(img[:,:,2].flatten().tolist())
red_image = createImage('red_histogram', color_rojo, color_red_frequency)

cv.imshow('original', img)
cv.setMouseCallback('original', click_event)

cv.waitKey(0)