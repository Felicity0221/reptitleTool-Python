import os
import random
import re
import urllib
from urllib import request

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.request import urlretrieve
import chardet
import time


def getUrl(url, baseUrl, path):
    # 请求页面

    # 页面编码
    encoding = "utf-8"
    try:
        encoding = chardet.detect(request.urlopen(url).read())["encoding"]
    except Exception as error:
        print("encoding error",error)


    # 防止被发现
    # headers
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    ]
    headers = {
        'User-Agent': '',
        'Content-Type': 'application/json;charset=UTF-8',
        'Request Method': 'GET',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "Referer":url,
        "Host": urllib.parse.urlparse(url).hostname,


    }
    headers['User-Agent'] = random.choice(user_agent_list)
    # print("host",urllib.parse.urlparse(url).hostname)
    # ip
    proxy_list = [
        "http://P0000574:nMIoNdjE@143.198.223.224--:10000",
"http://P0000574:nMIoNdjE@143.198.223.224--:10000"


    ]
    proxies = {'http': random.choice(proxy_list), 'https': random.choice(proxy_list)}
    time.sleep(3)
    # ,proxies= proxiesproxies=proxies
    r = requests.get(url,verify=False, headers= headers )
    r.encoding = encoding



    if r.status_code == 200:
        # 提取页面所有的链接和需要下载的内容
        html = BeautifulSoup(r.text, 'html.parser')

    #      获取页面的所有链接
        list =  []

        # 获取css文件
        for k in html.find_all("link"):
            if  k.get("href") != url:
                list.append(urljoin(baseUrl,k.get("href")))

        # 获取js文件
        for k in html.find_all("script"):

            if k.get("src") != None and k.get("src") != url:
                list.append(urljoin(baseUrl,k.get("src")))

        # 获取图片文件
        for k in html.find_all("img"):
            if k.get("src") != None and (not k.get("src").startswith("data")):
                list.append(urljoin(baseUrl, k.get("src")))

        print("list",list)


        # 写入文件
        for k in list:
            file_path_2 = ''
            file_path_3 = ''
            file_path_4 = ""
            file_path_1 = ""
            # if ".com" in k:
            #     # /pro/hongxiu_pc/_prelease/css/
            #     file_path_1 = k.split(".com")[1]
            #     if file_path_1 != "":
            #         # module.c38f2.css
            #         file_path_2 = file_path_1.split("/")[-1]
            #         if "?" in file_path_2:
            #             file_path_2 = file_path_2.split("?")[0]
            #
            #         # / pro / hongxiu_pc / _prelease / css
            #         file_path_3 = file_path_1.split(file_path_2)[0].strip("/")
            #         # css
            #         file_path_4 = file_path_2.split(".")[-1]
            try:
                file_path_1 = k.split(".com")[1]
                try:
                    file_path_2 = file_path_1.split("/")[-1]
                    if "?" in file_path_2:
                        file_path_2 = file_path_2.split("?")[0]

                    try:
                        file_path_3 = file_path_1.split(file_path_2)[0].strip("/")
                        file_path_4 = file_path_2.split(".")[-1]
                    except Exception as error:
                        print("file_path_3/4 error",error)
                except Exception as error:
                    print("file_path_2 error",error)

            except Exception as error:
                print("file_path_1 error",error)

            filepath = path +"/" + file_path_3
            if not os.path.exists(filepath):
                os.makedirs(filepath)

            if file_path_2 != "":
                if file_path_4 in ["png","jpg","jpeg","gif","apng","avif","jfif","pjpeg","pjp","svg","webp","bmp","ico","cur","tif","tiff","qif"]:
                    try:
                        with open(filepath+"/"+file_path_2,"wb") as f:
                            imgFile = requests.get(k,verify=False,headers= headers)
                            f.write(imgFile.content)
                        # urlretrieve(k,filepath+"/"+file_path_2)
                    except Exception as error:
                        print("img error",error)
                else:
                    try:
                        with open(filepath+"/"+file_path_2,"w",encoding="utf-8") as f:
                            # ,proxies=proxies
                            file = requests.get(k,verify=False,headers= headers)
                            print("filepath",filepath)
                            print("file_path_1",file_path_1)
                            print("file_path_2",file_path_2)
                            print("file_path_3",file_path_3)
                            print("file_path_4",file_path_4)
                            if file.status_code==200:
                                f.write(file.text)
                                file.close()
                            else:
                                print("file error",file.status_code)
                    except Exception as error:
                        print("file error",error)


        # 将页面内容写入html
        index_file = open(path+"/"+"index.html","w",encoding="utf-8")
        index_file.write(r.text)
        index_file.close()
    else:
        print("fail")


if __name__ == "__main__":
    start_url = 'https://www.niaogebiji.com/'
    save_directory = 'www.niaogebiji.com'

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    getUrl(start_url, start_url, save_directory)