import cv2
import numpy as np

image_hsv = None   # global ;(
image_src = None
pixel = (20,60,80) # some stupid default

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]
        #you might want to adjust the ranges(+-10, etc):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)

        image_mask = cv2.inRange(image_hsv,lower,upper)
        res = cv2.bitwise_and(image_src, image_src, mask=image_mask)

        cv2.imshow("mask",image_mask)
        cv2.imshow("image filtered", res)


def main():
    import sys
    global image_hsv, pixel, image_src # so we can use it in mouse callback

    image_src = cv2.imread("Red_light_2.jpg")  # pick.py my.png
    if image_src is None:
        print ("the image read is None............")
        return
    cv2.imshow("bgr",image_src)

    ## NEW ##
    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    # now click into the hsv img , and look at values:
    sub = cv2.cvtColor(image_src,cv2.COLOR_BGR2RGB)
    bilateral = cv2.bilateralFilter(sub, 15, 75, 75)
    image_hsv = cv2.cvtColor(bilateral,cv2.COLOR_RGB2HSV)
    cv2.imshow("hsv",image_hsv)
    cv2.imshow("image filter BILATERAL", bilateral)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()