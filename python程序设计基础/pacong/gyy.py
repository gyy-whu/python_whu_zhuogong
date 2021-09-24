from lxml import etree
import json
import requests
import urllib.request
import re

# urllist中存储四大内容总的网页网址，dizhilist存储内容里面每个小网址
urllist1_1 = ['http://www.hbjc.gov.cn/qwfb/ajxx/index.shtml']
dizhilist1_1 = []
urllist1_2 = ['http://www.hbjc.gov.cn/qwfb/zdal/', 'http://www.hbjc.gov.cn/qwfb/zdal/index_1.shtml']
dizhilist1_2 = []
urllist2_1 = ['http://www.hbjc.gov.cn/gzbg/ndbg/index.shtml', 'http://www.hbjc.gov.cn/gzbg/ndbg/index_1.shtml']
dizhilist2_1 = []
urllist2_2 = ['http://www.hbjc.gov.cn/gzbg/bnbg/']
dizhilist2_2 = []


def gethtml(url):  # 通过url得到html
    res = requests.get(url)
    html = etree.HTML(res.content)
    return html


def getdizhi(html):  # 得到大的内容里面的每个小地址
    return html.xpath("//div[@class='conblock listpage']/ul/li/a/@href")


def gettitle1_1(html):  # 得到标题方法1
    return html.xpath("//h1[@class='arttitle']/text()")


def gettitle1_2(html):  # 得到标题方法2
    return html.xpath("//div[@class='detail_tit']/text()")


def gettext1_1(html):  # 得到文本方法1
    return html.xpath("//div[@class='article']//text()")


def gettext1_2(html):  # 得到文本方法22
    return html.xpath("//div[@class='detail_con']//text()")


def getimg(html):  # 得到图片
    return html.xpath("//div[@class='article']//img/@oldsrc")


def getdizhilist(urllist):  # 得到每个小地址
    for url in urllist:
        html = gethtml(url)
        dizhilist = []
        dizhilist.append(getdizhi(html))
    return dizhilist


for url in dizhilist1_1:
    for deepurl in url:
        deephtml = gethtml(deepurl)
        deeptitle = gettitle1_1(deephtml)[0]
        deepimg = getimg(deephtml)
        deeptext = gettext1_1(deephtml)


def decorator1(func):
    def wrapper(dizhilist):
        func()
        return wrapper


def printtext1_2(deepurl):  # 指导案例的一部分文本输出
    deepurl = 'http://www.hbjc.gov.cn/qwfb/zdal/' + deepurl
    deephtml = gethtml(deepurl)
    deeptitle = gettitle1_1(deephtml)[0]
    deeptext = gettext1_1(deephtml)
    # 输出文本
    with open(r'D:\text\权威发布\指导案例\{0}.txt'.format(deeptitle), 'w', encoding="utf-8") as file:
        for texts in deeptext:
            if (texts[0] == '\n' and (texts[-1] == ' ' or texts[-1] == '\n')):
                pass
            else:
                file.write(texts + '\n')


"""
#权威发布的案件信息的内容提取
"""
# 获得18页内所有案例（268个）的网址
for i in range(1, 18):
    m = 'http://www.hbjc.gov.cn/qwfb/ajxx/index_' + str(i) + '.shtml'
    urllist1_1.append(m)
dizhilist1_1 = getdizhilist(urllist1_1)
# 将每个网址里面对应的内容以TXT格式输出到对应文件夹中,并将jpg图片也输出到文件夹中
for url in dizhilist1_1:
    for deepurl in url:
        deephtml = gethtml(deepurl)
        deeptitle = gettitle1_1(deephtml)[0]
        deepimg = getimg(deephtml)
        deeptext = gettext1_1(deephtml)
        # 输出图片
        if deepimg == []:
            pass
        else:
            for img in deepimg:
                s = img[2:8]
                k = img[17]
                img = 'http://www.hbjc.gov.cn/ajjj/{0}/{1}'.format(s, img)
                try:
                    urllib.request.urlretrieve(img, r'D:\text\权威发布\案件信息\{0}{1}.jpg'.format(deeptitle, k))
                except:
                    pass
        # 输出文本
        with open(r'D:\text\权威发布\案件信息\{0}.txt'.format(deeptitle), 'w', encoding="utf-8") as file:
            for texts in deeptext:
                if (texts[0] == '\n' and (texts[-1] == ' ' or texts[-1] == '\n')):
                    pass
                else:
                    file.write(texts + '\n')

"""
#权威发布的指导案例的内容提取
"""
# 获得2页内所有指导案例的网址
dizhilist1_2 = getdizhilist(urllist1_2)
# 将每个网址里面对应的内容以TXT格式输出到对应文件夹中
for deepurl in dizhilist1_2[0][:9]:
    deephtml = gethtml(deepurl)
    deeptitle = gettitle1_2(deephtml)[0]
    deeptext = gettext1_2(deephtml)
    # 输出文本
    with open(r'D:\text\权威发布\指导案例\{0}.txt'.format(deeptitle), 'w', encoding="utf-8") as file:
        for texts in deeptext:
            if (texts[0] == '\r'):
                if (texts[-1] == '\n'):
                    file.write(texts)
                else:
                    pass
            else:
                file.write(texts)
for deepurl in dizhilist1_2[0][9:]:
    printtext1_2(deepurl)
for deepurl in dizhilist1_2[1]:
    printtext1_2(deepurl)

"""
#工作报告的年度报告的内容提取
"""
# 获得2页内所有年度报告的网址
dizhilist2_1 = getdizhilist(urllist2_1)
for i in range(0, 18):
    if i == 0:
        dizhilist2_1[0][0] = 'http://www.hbjc.gov.cn/' + str(dizhilist2_1[0][0])
    else:
        s = 0 if i < 15 else 1
        dizhilist2_1[s][i - s * 15] = 'http://www.hbjc.gov.cn/gzbg/ndbg/' + str(dizhilist2_1[s][i - s * 15])
# 将每个网址里面对应的内容以TXT格式输出到对应文件夹中,图片以jpg格式输出到对应文件夹
for url in dizhilist2_1:
    for deepurl in url:
        deephtml = gethtml(deepurl)
        deeptitle = gettitle1_1(deephtml)[0]
        deepimg = getimg(deephtml)
        deeptext = gettext1_1(deephtml)
        print(deeptext)
        # 输出图片
        if deepimg == []:
            pass
        else:
            for img in deepimg:
                s = img[2:8]
                k = img[17]
                img = 'http://www.hbjc.gov.cn/jcyw/{0}/{1}'.format(s, img)
                try:
                    urllib.request.urlretrieve(img, r'D:\text\工作报告\年度报告\{0}{1}.jpg'.format(deeptitle, k))
                except:
                    pass
        # 输出文本
        with open(r'D:\text\工作报告\年度报告\{0}.txt'.format(deeptitle), 'w', encoding="utf-8") as file:
            for texts in deeptext:
                file.write(texts)

"""
工作报告的半年报告的内容提取
"""
# 获得所有半年报告的网址
dizhilist2_2 = getdizhilist(urllist2_2)
# 将每个网址里面对应的内容以TXT格式输出到对应文件夹中
for i in range(0, 5):
    if (i == 4):
        dizhilist2_2[0][i] = 'http://www.hbjc.gov.cn/gzbg/bnbg/' + str(dizhilist2_2[0][i])
    else:
        dizhilist2_2[0][i] = 'http://www.hbjc.gov.cn/' + str(dizhilist2_2[0][i])
for url in dizhilist2_2:
    for deepurl in url:
        print(deepurl)
        deephtml = gethtml(deepurl)
        deeptitle = gettitle1_1(deephtml)[0]
        deepimg = getimg(deephtml)
        deeptext = gettext1_1(deephtml)
        print(deeptext)
        # 输出图片
        if deepimg == []:
            pass
        else:
            for img in deepimg:
                s = img[2:8]
                k = img[17]
                img = 'http://www.hbjc.gov.cn/jcyw/{0}/{1}'.format(s, img)
                try:
                    urllib.request.urlretrieve(img, r'D:\text\工作报告\半年报告\{0}{1}.jpg'.format(deeptitle, k))
                except:
                    pass
        # 输出文本
        with open(r'D:\text\工作报告\半年报告\{0}.txt'.format(deeptitle), 'w', encoding="utf-8") as file:
            for texts in deeptext:
                if (texts[0] == '\r'):
                    if (texts[-1] == '\n'):
                        file.write(texts)
                    else:
                        pass
                else:
                    file.write(texts)

def getdizhilist(urllist):  #得到每个小地址
    for url in urllist:
        html = gethtml(url)
        dizhilist.append(getdizhi(html))
    return dizhilist
