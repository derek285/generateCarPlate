#coding=utf-8

import os
# import sys
import numpy as np
import cv2
import argparse
# import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from math import *

from PlateCommon import *

TEMPLATE_IMAGE = "./template/template.bmp"

class GenPlateScene:
    def __init__(self, fontCh, fontEng, NoPlates):
        self.fontC = ImageFont.truetype(fontCh, 43, 0)    # 省简称使用字体
        self.fontE = ImageFont.truetype(fontEng, 60, 0)   # 字母数字字体
        # self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        # self.bg = cv2.resize(cv2.imread(TEMPLATE_IMAGE), (226, 70))
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        self.bg = cv2.resize(cv2.imread(TEMPLATE_IMAGE), (226, 70))
        self.noplates_path = []
        for parent, _, filenames in os.walk(NoPlates):
            for filename in filenames:
                self.noplates_path.append(parent + "/" + filename)

    def gen_plate_string(self, iter):
        plate_str = ""
        i = iter // IMG_COUNT_PER_PROVINCE
        iterChar = (iter % IMG_COUNT_PER_PROVINCE) // 9
        for cpos in range(7):
            if cpos == 0:
                plate_str += chars[i] #+r(31)]
            elif cpos == 1:
                plate_str += chars[41 + iterChar]#+r(24)]
            else:
                plate_str += chars[31 + r(34)]
        return plate_str

    def draw(self, val):
        offset= 2
        self.img[0:70, offset+8:offset+8+23] = GenCh(self.fontC, val[0])
        self.img[0:70, offset+8+23+6:offset+8+23+6+23] = GenCh1(self.fontE, val[1])
        for i in range(5):
            base = offset+8+23+6+23+17+i*23+i*6 
            self.img[0:70, base:base+23]= GenCh1(self.fontE, val[i+2])
        return self.img

    def generate(self,text):
        print text, len(text)

        fg = self.draw(text.decode(encoding="utf-8"))   # 得到白底黑字
        # cv2.imwrite('01.jpg', fg)
        fg = cv2.bitwise_not(fg)    # 得到黑底白字
        # cv2.imwrite('02.jpg', fg)
        com = cv2.bitwise_or(fg, self.bg)   # 字放到（蓝色）车牌背景中
        # cv2.imwrite('03.jpg', com)
        com = rot(com, r(20)-10, com.shape, 10) # 矩形-->平行四边形
        # cv2.imwrite('04.jpg', com)
        com = rotRandrom(com, 5, (com.shape[1], com.shape[0])) # 旋转
        # cv2.imwrite('05.jpg', com)
        com = tfactor(com) # 调灰度
        # cv2.imwrite('06.jpg', com)

        com, loc = random_scene(com, self.noplates_path)    # 放入背景中
        if com is None or loc is None:
            return None, None
        # cv2.imwrite('07.jpg', com)
        com = AddGauss(com, 0) # 加高斯平滑
        # cv2.imwrite('08.jpg', com)
        com = addNoise(com)         # 加噪声
        # cv2.imwrite('09.jpg', com)
        return com, loc

    def gen_batch(self, batchSize, outDir):

        for i in xrange(batchSize):
            outputPath = outDir + str(i // IMG_COUNT_PER_PROVINCE) + "/"
            if (not os.path.exists(outputPath)):
                os.mkdir(outputPath)
            plate_str = self.gen_plate_string(i)
            img, loc =  self.generate(plate_str)
            if img is None:
                continue
            cv2.imwrite(outputPath + "/" + plate_str + ".jpg", img)
            #with open(outputPath + "/" + plate_str + ".txt", 'w') as obj:
            #    line = ','.join([str(v) for v in loc]) + ',"' + plate_str + '"\n' 
            #    obj.write(line)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bg_dir', default='./Background', help='bg_img dir')
    parser.add_argument('--out_dir', default='./gen_data/', help='output dir')
    parser.add_argument('--make_num', default=IMG_COUNT_PER_PROVINCE*31-1, type=int, help='num')
    return parser.parse_args()

def main(args):
    G = GenPlateScene("./font/platech.ttf", './font/platechar.ttf', args.bg_dir)
    G.gen_batch(args.make_num, args.out_dir)


if __name__ == '__main__':
    IMG_COUNT_PER_PROVINCE = 16
    main(parse_args())




