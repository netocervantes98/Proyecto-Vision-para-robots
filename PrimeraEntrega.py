# Primera entrega parcial
# Visión para robots
# Prof. Gabriel González Sahagún

# A01196642 Ernesto Cervantes Juárez
# A00820188 Eduardo Angulo Martínez
# A00821541 Miguel Morales de la Vega
# A00820662 Sergio Canto Arizpe
# A00823445 Jesús Francisco Anaya González

from copy import copy
import numpy as np
import cv2 as cv
import sys

# Variables globales
img_path = 'gundam.jpg'
coords = []

# Colores
color_azul = (255, 0, 0)
color_verde = (0, 255, 0)
color_rojo = (0, 0, 255)
color_click = (0, 0, 0)

# Tamaño de grafica
n = 540
m = 560
iniciox = 20
finx = 545
inicioy = 40
finy = 515

# Variables auxiliares
blue_image = np.zeros([n, m, 3], dtype=np.uint8)
red_image = np.zeros([n, m, 3], dtype=np.uint8)
green_image = np.zeros([n, m, 3], dtype=np.uint8)
clean_blue = 0
clean_red = 0
clean_green = 0

image_hsv = None   # global ;(
image_src = None
pixel = (20, 60, 80)  # some stupid default


def click(event, x, y, flags, param):
    global coords
    if event == cv.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        if len(coords) == 2:
            submatrix = img[coords[0][0]: coords[1]
                            [0], coords[0][1]: coords[1][1]]

            minn = np.amin(submatrix)
            maxx = np.amax(submatrix)
            median = np.median(submatrix)
            average = np.average(submatrix)
            std = np.std(submatrix)

            print("mínimo: ", minn)
            print("máximo: ", maxx)
            print("mediana: ", '{:.3f}'.format(median))
            print("promedio: ", '{:.3f}'.format(average))
            print("desviación estandar: ", '{:.3f}'.format(std))
            cv.destroyAllWindows()
            f = open("stats.txt", "w" if flag else "a")
            f.write(f'{coords[0][0]} {coords[1][0]} {coords[0][1]} {coords[1][1]} {minn} {maxx} {median} {average} {std}\n')
            f.close()
            coords = []


def stats():
    global flag, img
    print("\nESTADÍSTICAS\nSeleecione área (dos puntos)")
    flag = int(input("¿Quiere sobreescribir? 1 sí | 0 no: "))
    img = cv.imread('gundam.jpg')
    img2 = cv.resize(img, (540, 540))
    img = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    cv.imshow('original', img)
    cv.setMouseCallback('original', click)
    cv.waitKey(0)
    cv.destroyAllWindows()


def binarizar():
    print("\nBINARIZACIÓN")
    img = cv.imread('gundam.jpg')
    img2 = cv.resize(img, (540, 540))
    img = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    info = int(input("Digite valor de umbral (0 - 255): "))
    _, binimg = cv.threshold(img, info, 255, cv.THRESH_BINARY)
    cv.imshow('binarizada', binimg)
    cv.waitKey(0)
    cv.destroyAllWindows()


# Rutina para calcular las frequencias y mapear de frequencias a alturas.
def CalcFreq(arr):
    ans = np.zeros(256, dtype=int)
    for x in arr:
        ans[x] += 1
    global maxi
    maxi = max(ans)
    for i in range(len(ans)):
        ans[i] = int(ans[i] * (finy - inicioy) / maxi)
    return ans

# Crear rutina para el mouse


def click_event(event, x, y, flags, param):
    global blue_image, green_image, red_image, clean_blue, clean_red, clean_green, img
    if event == cv.EVENT_LBUTTONDOWN:
        # Obtener colores de la imagen para pintar en el histograma.
        colorsB = img[y, x, 0]
        colorsG = img[y, x, 1]
        colorsR = img[y, x, 2]
        colors = img[y, x]
        # Seleccionar pixel en la imagen y dibujar circulo sobre el.
        if colorsB > 130 and colorsG > 130 and colorsR > 130:
            color_circulo = [0, 0, 0]
        else:
            color_circulo = [255, 255, 255]
        img2 = copy(img)
        img = cv.circle(img, (x, y), 5, color_circulo, 2)
        print("BRG Format: ", colors)
        # pintar azul
        drawRectangle(blue_image, (iniciox+2) + clean_blue * 2,
                      color_blue_frequency[clean_blue], color_azul)
        drawRectangle(blue_image, (iniciox+2) + colorsB * 2,
                      color_blue_frequency[colorsB], color_rojo)
        clean_blue = colorsB
        # pintar verde.
        drawRectangle(green_image, (iniciox+2) + clean_green * 2,
                      color_green_frequency[clean_green], color_verde)
        drawRectangle(green_image, (iniciox+2) + colorsG * 2,
                      color_green_frequency[colorsG], (0, 0, 0))
        clean_green = colorsG
        # pintar rojo.
        drawRectangle(red_image, (iniciox+2) + clean_red * 2,
                      color_red_frequency[clean_red], color_rojo)
        drawRectangle(red_image, (iniciox+2) + colorsR * 2,
                      color_red_frequency[colorsR], color_azul)
        clean_red = colorsR
        # Mostrar imagenes
        cv.imshow('original', img)
        cv.imshow('blue_histogram', blue_image)
        cv.imshow('green_histogram', green_image)
        cv.imshow('red_histogram', red_image)
        img = copy(img2)


# Dibujar un rectangulo de altura h con base en el punto x1.
def drawRectangle(mat, x1, h, color):
    for x in range(x1, x1+1):
        for y in range(finy, finy-h, -1):
            mat[y][x] = color

# Crear un histograma recorriendo las alturas dadas.


def createImage(name, color_, arr):
    # Crear imagen blanca
    mat = np.zeros([n, m, 3], dtype=np.uint8)
    mat.fill(255)
    # Titulo
    # Eje (x, y)
    cv.arrowedLine(mat, (iniciox, finy), (finx, finy), color=1, tipLength=0.02)
    cv.arrowedLine(mat, (iniciox, finy), (iniciox, inicioy),
                   color=1, tipLength=0.02)
    cv.putText(mat, "max = " + str(maxi), (200, 40),
               cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=color_)
    # dibujar rectangulos
    for x in range(256):
        drawRectangle(mat, (iniciox+2) + x * 2, arr[x], color_)
    cv.imshow(name, mat)
    return mat


def histograma():
    print("\nHISTOGRAMA")
    # Leer imagen y cambiar tamaño.
    global blue_image, green_image, red_image, color_blue_frequency, color_red_frequency, color_green_frequency, img
    img = cv.imread(img_path)
    img = cv.resize(img, (540, 540))

    # Obtener frequencias de colores y crear histogramas
    color_blue_frequency = CalcFreq(img[:, :, 0].flatten().tolist())
    blue_image = createImage(
        'blue_histogram', color_azul, color_blue_frequency)

    color_green_frequency = CalcFreq(img[:, :, 1].flatten().tolist())
    green_image = createImage(
        'green_histogram', color_verde, color_green_frequency)

    color_red_frequency = CalcFreq(img[:, :, 2].flatten().tolist())
    red_image = createImage('red_histogram', color_rojo, color_red_frequency)

    cv.imshow('original', img)
    cv.setMouseCallback('original', click_event)

    cv.waitKey(0)
    cv.destroyAllWindows()


# mouse callback function
def pick_color(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("f")
        pixel = image_hsv[y, x]
        # you might want to adjust the ranges(+-10, etc):
        upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)

        image_mask0 = cv.inRange(image_hsv, lower, upper)

        res = cv.bitwise_and(image_src, image_src, mask=image_mask0)

        cv.imshow("mask", image_mask0)
        cv.imshow("image filtered", res)


def filtro():
    print("\nFILTRO")
    global image_hsv, pixel, image_src  # so we can use it in mouse callback

    image_src = cv.imread("men.jpg")  # pick.py my.png
    if image_src is None:
        print("the image read is None............")
        return
    cv.imshow("image_src", image_src)

    ## NEW ##
    cv.namedWindow('image_src')
    cv.setMouseCallback('image_src', pick_color)

    # now click into the hsv img , and look at values:
    #sub = cv.cvtColor(image_src,cv.COLOR_BGR2RGB)
    kernel = np.ones((5, 5), np.float32) / 25

    bilateral = cv.bilateralFilter(image_src, 15, 75, 75)
    image_hsv = cv.cvtColor(bilateral, cv.COLOR_BGR2HSV)
    #image_hsv = cv.morphologyEx(image_hsv0, cv.MORPH_CLOSE, kernel)
    #image_hsv = cv.erode(image_hsv0, kernel, iterations=1)
    cv.imshow("hsv", image_hsv)
    cv.imshow("image filter BILATERAL", bilateral)

    cv.waitKey(0)
    cv.destroyAllWindows()


def menu():
    info = 1
    while info:
        print("\nMENU")
        print("0 - Salir ")
        print("1 - Histograma ")
        print("2 - Filtro ")
        print("3 - Estadísticas ")
        print("4 - Binarizar ")
        info = int(input("Seleccione: "))

        if info == 1:
            histograma()
        elif info == 2:
            filtro()
        if info == 3:
            stats()
        elif info == 4:
            binarizar()


if __name__ == '__main__':
    menu()
