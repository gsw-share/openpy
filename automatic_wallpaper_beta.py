#-*- coding: UTF-8 -*-
from urllib import error
from bs4 import BeautifulSoup
import datetime
import win32gui
import win32con
import win32api
import ctypes
import ctypes.wintypes
import threading
import urllib.request
import requests
import random
import time
import os
import re

num = 0
numPicture=30
file_dir = "./imagecache"
List = []
appfile= []

def parse_url(url):
    global List
    print('Please wait.....')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s

def get_file_size_kb(filePath):
	fsize = os.path.getsize(filePath)
	fsize = fsize/float(1024)
	return fsize

def download(html, keyword):
    global num
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    print('Query keywords:' + keyword + ',Start downloading...',len(pic_url))
    for each in pic_url:
        print(numPicture,'download ' + str(num + 1) + ',addr:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            pic_name=keyword.replace('*','');
            string = file_dir + '/' + pic_name + '_' + str(num) + '.jpg'
            print(string,'Error, the current picture cannot be downloaded')
            continue
        else:
            pic_name=keyword.replace('*','');
            string = file_dir + '/' + pic_name + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            size_kb=get_file_size_kb(string)
            if(size_kb<12):
                os.remove(string);
            num += 1
        if num >= numPicture:
            print("Get terminated.",num,numPicture)
            return

def get_wallpaper(keysword):
    url = "https://image.baidu.com/search/index?ct=&z=0&tn=baiduimage&ipn=r&word="+keysword+"&pn=0&istype=2&ie=utf-8&oe=utf-8&cl=&lm=-1&st=-1&fr=&fmq=1576182804036_R&ic=0&se=&sme=&width=1920&height=1080&face=0&hd=0&latest=0&copyright=0";
    tot = parse_url(url)
    print('%s Class pictures in total:%d' % (keysword, tot))
    y = os.path.exists(file_dir)
    if y == 1:
        print('The file already exists')
    else:
        os.mkdir(file_dir)
    t = 0
    path222 = "./imagecache/"
    tmp = url
    while 1:
        appfile = search_file_name(path222)
        if(len(appfile)>=(numPicture*0.8)):
            print(t,numPicture,"end_ok")
            return
        try:
            url = tmp + str(t)
            result = requests.get(url, timeout=4)
            print(url)
        except error.HTTPError as e:
            print('Network error, please adjust the network and try again')
            t = t+ 80
        else:
            download(result.text, keysword)
            t = t + 80
    print(t,numPicture,"end")

def search_file_name(file_dir):
    files=[]
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)
        print('sub_dirs:', dirs)
        print('files:', files)
    return files

def check_need_update():
    ymd=int(datetime.datetime.now().year)+int(datetime.datetime.now().month)+int(datetime.datetime.now().day)
    print("check_need_update",ymd)
    if((ymd%3)==0):
        return 1
    return 0;

def main_app():
    keysword="猫咪"
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    global appfile
    path = "./imagecache/"
    path2=path
    wallpaper_default=os.getcwd()+"//wallpaper_default.jpg"
    if(check_need_update()):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_default, 0)
        print('It needs to be updated today. No reason. Do you understand')
        get_wallpaper(keysword);
    appfile = search_file_name(path)
    if(len(appfile)<int(20)):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_default, 0)
        get_wallpaper(keysword);
    appfile = search_file_name(path)
    while True:
        n = random.randint(0,len(appfile)-1)
        filepath = os.getcwd()+path2+appfile[n]
        print(filepath)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)
        time.sleep(120)
if __name__ == '__main__':
    main_app()