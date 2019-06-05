# -*- coding: utf-8 -*-
# @Author  : pasca
# @mailbox : 1196738787@qq.com
import math
import os
import random
import matplotlib.pyplot as plt
import itchat
from PIL import Image
import time
from concurrent.futures import ThreadPoolExecutor


# 分析微信联系人性别，并分别计数保存到字典。
def Sex_Analysis(data):
    """
    :param data: 全部联系人所有信息
    :return: 男、女和未知的字典集
    """
    sex = dict()
    for i in data:
        if i.get('Sex') == 1:
            sex['man'] = sex.get('man', 0) + 1
        elif i.get('Sex') == 0:
            sex['woman'] = sex.get('woman', 0) + 1
        else:
            sex['unknown'] = sex.get('unknown', 0) + 1

    for i, key in enumerate(sex):
        plt.bar(key, sex[key])
    plt.savefig("好友性别分析.png")
    plt.show()



    # 获取头像
def Get_HeadImg(data):
    start = time.time()
    end = time.time()
    pic_path = os.getcwd() + '/img/'
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)
    for count, head in enumerate(data):
        print('第' + str(count) + '张')
        # img = itchat.get_head_img(userName=head["UserName"])
        img = itchat.get_head_img(userName=head["UserName"])
        img_file = open(pic_path + str(count) + ' ' + str(head["NickName"]) + ".jpg", "wb")  # 需要先创建
        img_file.write(img)
        img_file.close()
        print(end - start)






# 将保存的本地头像填充成一个大图片
def HeadImg_Use():
    x = 0
    y = 0
    pic_path = os.getcwd()
    imgs = os.listdir('img')
    random.shuffle(imgs)
    newImage = Image.new('RGBA', (1024, 1024))   # 新建画布
    width = int(math.sqrt(1024 * 1024 / len(imgs)))
    numline = int(1024 / width)   # 一行需要填充图片的个数

    for i in imgs:
        if not i.endswith('jpg'):
            continue
        img = Image.open('img/' + i)
        img = img.resize((width, width), Image.ANTIALIAS)
        newImage.paste(img, (x * width, y * width))
        x += 1
        if x >= numline:
            x = 0
            y += 1
    newImage.save("all.png")


if __name__ == '__main__':
    itchat.auto_login()
    data = itchat.get_friends(update=True)  # update如果为Flase，返回目前本地值
    Sex_Analysis(data)
    with ThreadPoolExecutor(max_workers=1000) as executor:
        executor.submit(Get_HeadImg, data)

    HeadImg_Use()
