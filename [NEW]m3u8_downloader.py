# 需要的第三方库：requests
# 对于部分.ts有跳跃的回放，可尝试使用此脚本下载。
# 面向对象编写，更易于使用。
from requests import session, packages
from os import makedirs, remove
from re import sub, match
from time import time

packages.urllib3.disable_warnings()
class Episode():
    def __init__(self, m3u8_url, save_path):
        self.save_path = save_path
        self.conn = session()
        self.pre = ''
        tmp = m3u8_url.split('/')
        for i in tmp:
            if '.m3u8' in i: break
            else: self.pre += i + '/'
        self.anonymous_urls = []
        self.recorded_urls = []
        self.head = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        response = self.conn.get(m3u8_url, headers=self.head, verify=False)
        self.m3u8 = response.text.split('\n')
        pattern = r'.*/\d+\.ts.*'
        for line in self.m3u8:
            if match(pattern, line): self.recorded_urls.append(line)
        pattern = r'\.ts\?auth_key=.*'
        for url in self.recorded_urls:
            self.anonymous_urls.append(sub(pattern, '.ts', url))
    def recorded_download(self):
        try:
            n = 0
            with open(self.save_path+str(int(time()))+'.ts', 'wb') as f:
                for url in self.recorded_urls:
                    print('下载'+str(n))
                    response = self.conn.get(self.pre+url, headers=self.head, verify=False)
                    f.write(response.content)
                    n += 1
        except Exception as e: print('在网址'+self.pre+url+'\n由于'+str(e)+'下载失败!')
    def anonymous_download(self):
        try:
            n = 0
            with open(self.save_path+str(int(time()))+'.ts', 'wb') as f:
                for url in self.anonymous_urls:
                    print('匿名下载'+str(n))
                    response = self.conn.get(self.pre+url, headers=self.head)
                    f.write(response.content)
                    n += 1
        except Exception as e: print('在网址'+self.pre+url+'\n由于'+str(e)+'下载失败!')

path = input('保存地址：')
try: makedirs(path)
except: pass
playback = Episode(input('URL:'), path)
playback.anonymous_download()
