# step1：坐标归一化
# step2：缩放坐标
# step3：文字图形构建
# step4：文字识别
# step5：旋转识别

import numpy as np
import cv2 as cv
import pytesseract
from PIL import Image

# 坐标归一化，区间[0,1]
def normalize(points):
    minX=maxX=points[0][0][0][0]
    minY=maxY=points[0][0][0][0]
    for i in points:
        for j in i:
            for k in j:
                if k[0] < minX:
                    minX = k[0]
                if k[0] > maxX:
                    maxX = k[0]
                if k[1] < minY:
                    minY = k[1]
                if k[1] > maxY:
                    maxY = k[1]

    lengthX = maxX - minX
    lengthY = maxY - minY
    max = lengthX
    if lengthX < lengthY:
        max = lengthY
    # 偏移，最终放在lengthX，lengthY网格中
    # 缩放至[0,1]
    for i in points:
        for j in i:
            for k in j:
                k[0] = (k[0] - minX) / max
                k[1] = (k[1] - minY) / max

    return points

# 缩放至可视化区域 比如512*512
# 生成图片
def zoom(points):
    margin = 50
    size = 512
    for i in points:
        for j in i:
            for k in j:
                k[0] = (size - 2 * margin) * k[0] + margin
                k[1] = (size - 2 * margin) * k[1] + margin

    a = np.asarray(points, dtype=np.int32)
    # 白底
    img = np.zeros([size, size], dtype=np.uint8) + 255
    for i in a:
        count = 0
        for j in i:
            if count == 0:
                cv.fillPoly(img, [j], (0, 0, 0))
            else:
                cv.fillPoly(img, [j], (255, 255, 255))
            count += 1

    # cv.imshow("img", img)
    # cv.waitKey(0)
    return img

# 返回旋转图片
def rotate(image):
    return

# 识别
# 返回识别结果（文字）
def distinguish(image):
    # image = Image.open(file)
    # 解析图片，lang='chi_sim'表示识别简体中文，默认为English
    # 如果是只识别数字，可再加上参数config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
    content = pytesseract.image_to_string(image, lang='chi_sim')
    print("识别结果：", content)
    return content


# file = r"images/静夜思.png"
# image = Image.open(file)
# distinguish(image)
# 文字
# 某一文字[0] 比如：田
points = [
            [
                [[0, 0], [100, 0], [100, 100], [0, 100]],
                [[20, 20], [40, 20], [40, 40], [20, 40]],
                [[60, 20], [80, 20], [80, 40], [60, 40]],
                [[20, 60], [40, 60], [40, 80], [20, 80]],
                [[60, 60], [80, 60], [80, 80], [60, 80]]
             ]
          ]
points = normalize(points)
img = zoom(points)
content = distinguish(img)
cv.imshow("img", img)
cv.waitKey(0)