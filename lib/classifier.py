import cv2
import numpy as np
from lib.data import ORB_DATA
from lib.board import Board
from lib.piece import Fire, Wood, Water, Dark, Light, Heart

sift = cv2.xfeatures2d.SIFT_create()
matcher = cv2.BFMatcher(cv2.NORM_L2)


def count_matches(matches, ratio=0.75):
    count = 0
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            count += 1
    return count


def fix_colors(img):
    """ convert bgr to rgb """
    return np.fliplr(img.reshape(-1, 3)).reshape(img.shape)


def crop_center_square(arr, s):
    h, w, _ = arr.shape
    return arr[
           int((h - s) / 2):int((h + s) / 2),
           int((w - s) / 2):int((w + s) / 2),
           :]


def classify_orbs(frame):
    """ classifies the orbs in a given BGR frame and returns a board object """

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    plus = cv2.imread(r'C:\Users\saiyann\Desktop\clpadauto\pndsolver\resources\plus.png', 0)
    kpp, desp = sift.detectAndCompute(plus, None)

    xstart, xend, ystart, yend, size= get_canvas_position(frame)

    data = []
    for y in range(5):
        for x in range(6):
            ycor = int(y * size + ystart)
            xcor = int(x * size + xstart)
            cellhsv = hsv[ycor:ycor + size, xcor:xcor + size, slice(None)]
            cellgray = gray[ycor:ycor + size, xcor:xcor + size]

            # assign cell base value
            cut = crop_center_square(cellhsv, size / 3)
            avg = np.mean(cut[:, :, 0])
            # print(x,y,avg)
            for k, v in ORB_DATA.items():
                if v.huerange:
                    lower, upper = v.huerange
                    if lower < avg < upper:
                        cellvalue = k
                        break
            else:
                raise Exception("Unidentifiable Cell (%s, %s). Hue: %s" % (x, y, avg))

            # determine cell + status
            kp2, des2 = sift.detectAndCompute(cellgray, None)
            matches = matcher.knnMatch(desp, trainDescriptors=des2, k=2)
            if count_matches(matches) > 10:
                cellvalue |= 0x10

            data.append(cellvalue)

    assert len(data) == 30
    piece_dic = {1: Fire, 2: Water, 3: Wood, 4: Light, 5: Dark, 6: Heart}
    piece_list = [piece_dic[n] for n in data]
    number_of_rows = 5
    number_of_columns = 6
    board = Board(piece_list, number_of_rows, number_of_columns)
    return board


def get_canvas_position(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    height, width, _ = hsv.shape

    # compute true baseline from the bottom (necessary for some form-factors)
    yend = height
    while True:
        yend -= 1
        if max(hsv[yend, int(width / 5)]) > 0:
            break

    xend = width
    while True:
        xend -= 1
        if max(hsv[int(height * 4 / 5), xend]) > 0:
            break
    xstart = 0
    while True:
        xstart += 1
        if max(hsv[int(height * 4 / 5), xstart]) > 0:
            break
    size = int((xend - xstart) / 6)

    ystart = yend - size * 5
    return xstart, xend, ystart, yend, size
