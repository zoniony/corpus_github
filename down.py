import requests
import socket
import os

PATH = "/Users/zoniony/CVE/otf/in/"


# 设定一下无响应时间，防止有的坏图片长时间没办法下载下来
timeout = 20
socket.setdefaulttimeout(timeout)


# 从文件里面读urls
urls = []
with open('otf.txt') as f:
    for i in f.readlines():
        if i != '':
            i = i.strip()
            i = i.replace("blob","raw")
            urls.append(i)
        else:
            pass
        
# 为请求增加一下头，获取图片
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
headers = {'User-Agent': user_agent}
bad_url = []
count = 1
for url in urls:
    url.rstrip('\n')
    print(url)
    try:
        pic = requests.get(url, headers=headers)
        with open(PATH+'%d.otf' % count, 'wb') as f:
            f.write(pic.content)
            f.flush()
        print('otf %d' % count)
        count += 1
    except Exception as e:
        print(Exception, ':', e)
        bad_url.append(url)
    print('\n')
print('got all photos that can be got')

# 保存坏链接
with open('bad_url.data', 'w') as f:
    for i in bad_url:
        f.write(i)
        f.write('\n')
    print('saved bad urls')