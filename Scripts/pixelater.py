'''
Description: 图片像素化器
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-03-21 14:24:21
LastEditTime: 2022-05-13 22:05:32
'''
import os
import re

from PIL import Image

rawImgPath = ""  # 原始图像位置
targetPath = ""  # 目标图像位置
rawFilePath = ""  # 原始文件夹位置
targetFilePath = ""  # 目标文件夹位置
size = (32, 32)

rawFilePath = "D:\IDE\Programs\VS_Code_Programs\HammerWorkshop\HammerWorkshop-CookingCraft\Scripts\images\\raw"
targetFilePath = "D:\IDE\Programs\VS_Code_Programs\HammerWorkshop\HammerWorkshop-CookingCraft\Scripts\images\\target"

rawImgPath = "D:\IDE\Programs\VS_Code_Programs\HammerWorkshop\MedievalOverhaul\Textures\Meal\ApplePie\AppliePie_a.png"
targetPath = "D:\IDE\Programs\VS_Code_Programs\HammerWorkshop\HammerWorkshop-CookingCraft\Scripts\images\\target\\test.png"


def imgPixelater(image, size):
    """图片像素化
    :image: image 对象
    :size: 像素化大小
    """
    img = image.copy()
    img = img.resize(size)
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            r, g, b, a = img.getpixel((x, y))
            if (a == 255):
                continue
            if (a > 120):
                img.putpixel(
                    (x, y),
                    (r * 255 // a * 2, g * 255 // a * 2, b * 255 // a * 2, 255))
            else:
                img.putpixel((x, y), (r, g, b, 0))
    return img


def resetAlpha(image, originImage):
    """重设 alpha 值
    :image: image 对象 
    :originImage: 原始的 image 对象，含 alpha 通道
    """
    img = image.copy()
    originImg = originImage.copy()
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            r_origin, g_origin, b_origin, alpha_origin = originImg.getpixel(
                (x, y))
            r_img, g_img, b_img, alpha_img = img.getpixel((x, y))
            if (alpha_origin != alpha_img):
                img.putpixel((x, y), (r_img, g_img, b_img, alpha_origin))
    return img


dirs = os.listdir(rawFilePath)
for image in dirs:
    imageFile = rawFilePath + "\\" + image
    img = Image.open(imageFile)
    img = imgPixelater(img, size)
    newImageName = image.split("_")[0]
    img.save(targetFilePath + "\\" + newImageName + ".png")
    raw_img = img.convert("L").convert("RGBA")
    raw_img = resetAlpha(raw_img, img)
    raw_img.save(targetFilePath + "\\" + "raw_" + newImageName + ".png")

# imageFile = "C:\\Users\\msi\\Desktop\\cooking_table.png"
# img = Image.open(imageFile)
# img = imgPixelater(img,(256,256))
# img.save("C:\\Users\\msi\\Desktop\\cooking_table_32x.png")
