# -*- coding=utf-8 -*-
import requests
from bs4 import BeautifulSoup
import random


class IpProxy:

    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Connection': 'keep-alive',
        }
        # 'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',

    def get_ip_list(self):
        print("正在获取代理列表...")
        url = 'http://www.xicidaili.com/nn/'
        html = requests.get(url=url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        print("代理列表抓取成功.")
        return ip_list

    def get_random_ip(self, ip_list):
        print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        print("代理设置成功.")
        return proxies

    def get_proxy(self):
        ip_list = self.get_ip_list()
        proxy = self.get_random_ip(ip_list)
        print proxy
        return proxy

    @staticmethod
    def get_user_agent():
        user_agents = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
        ]
        return random.choice(user_agents)
