import cv2, dlib, sys
import numpy as np
import datetime as dt


class ImageProcessing:
    def __init__(self):
        self.run()

    # brightness track bar
    def onChangeBright(self, pos):
        t = (pos * 5, pos * 5, pos * 5)
        arr = np.full(img.shape, t, dtype=np.uint8)
        dst = cv2.add(img, arr)
        cv2.imshow('process', dst)

    # contrast track bar
    def onChangeContrast(self, pos):
        t = (pos * 5, pos * 5, pos * 5)
        arr = np.full(img.shape, t, dtype=np.uint8)
        dst = cv2.subtract(img, arr)
        cv2.imshow('process', dst)

    # blur track bar
    def onChangeBlur(self, pos):
        if pos % 2 == 1:
            dst = cv2.GaussianBlur(img, (pos, pos), 0)
            cv2.imshow('process', dst)

    def run(self):
        print('ImageProcessing')
        global img
        img = cv2.imread('./image/photo.jpg')
        cv2.imshow('process', img)
        cv2.createTrackbar('bright', 'process', 0, 20, self.onChangeBright)
        cv2.createTrackbar('contrast', 'process', 0, 20, self.onChangeContrast)
        cv2.createTrackbar('blur', 'process', 0, 20, self.onChangeBlur)
        while True:
            if cv2.waitKey(1) == ord('q'):
                x = dt.datetime.now()
                t = x.strftime('%Y%m%d%H%M%S')
                cv2.imwrite('./image/photo%s.jpg' % t, img)
                break
