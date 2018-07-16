# -*- coding=utf-8 -*-

import re
import urllib2
import json
from bs4 import BeautifulSoup
from csv_util import CsvUtil

def spider_taobao(goods_id):

    # 注意 User-Agent（mac下是不同的，需要修改）
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Accept-Language':'zh-CN,zh;q=0.3',
        'Referer':'https://detail.tmall.com/item.htm',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Connection':'keep-alive',
    }

    url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.57.25a11005L60sXF&id={}&skuId=3759128262116&areaId=310100&user_id=1695300927&cat_id=53412001&is_b=1&rn=c859285b1d0f5de17c3f2c3666916175'.format(goods_id)
    print "=====商品ID:", goods_id

    try:
        req = urllib2.Request(url=url, headers=headers)
        res = urllib2.urlopen(req).read().decode('gbk', 'ignore')
    except Exception as e:
        print ':', e.reason

    soup =  BeautifulSoup(res, "html.parser")
    try:
        title = soup.find("input", attrs={'name': "title"})['value']
    except Exception as e:
        try:
            title = soup.find("div", attrs={'class': "tb-detail-hd"})
            h1 = title.h1.string
            h1 = h1.replace("\r","").replace("\n","").replace("\t","")

            title = h1
        except Exception as e:
            print "Not fouund such goods"
            data = [id, "goods not found", "NaN", "NaN", "NaN"]
            return data

    title = "".join(title)
    title = title.replace(" ", ":") # 不允许出现空格
    print "名称: ", title

    try:
        purl = "https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=true&isSecKill=false&tmallBuySupport=true&isAreaSell=true&tryBeforeBuy=false&offlineShop=false&itemId={}&showShopProm=false&cachedTimestamp=1531703147517&isPurchaseMallPage=false&isRegionLevel=true&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=3&isForbidBuyItem=false&callback=setMdskip&timestamp=1531713077230&isg=null&isg2=BAgI7R06x2foMCvkXVYVGGag2Xa2oW0PVPAVOMK5cQN2nagHasE8S54UETVIrSST&areaId=310100&cat_id=53412001".format(goods_id)

        price_req = urllib2.Request(url=purl, headers=headers)
        price_res = urllib2.urlopen(price_req).read()
        price_res = price_res.decode('gb2312').encode('utf-8')

        # 商品已经下架的判断
        soup2 = BeautifulSoup(res, "html.parser")
        flag = soup2.find("div", attrs={'class': "sold-out-left"})
        #print flag

        p1 = re.compile(r'[(](.*)[)]', re.S)   #贪婪匹配
        rs = re.findall(p1, price_res)
        rs = rs[0]
        # 转换为 json 对象
        json_data = json.loads(rs)

        # 月销量
        print '月销量: ', json_data['defaultModel']['sellCountDO']['sellCount']

        # 库存
        skuQuantity = json_data['defaultModel']['inventoryDO']['skuQuantity']

        # 每个类目的所有分类商品的信息
        its = []
        dic = json_data['defaultModel']['itemPriceResultDO']['priceInfo']
        for d, x in dic.items():
            # Id， 价格， 促销价， 库存
            if 'promotionList' in x: # 是否促销
                it = {
                    'id' : d,
                    'price' :  x['price'],
                    'promotion_price' : x['promotionList'][0]['price'],
                    'quantity' : skuQuantity[d]['quantity']
                }
            else:
                it = {
                    'id': d,
                    'price': x['price'],
                    'promotion_price': 'No_Promotion',
                    'quantity': skuQuantity[d]['quantity']
                }
            #print d, x['price'], x['promotionList'][0]['price'], skuQuantity[d]['quantity']
            its.append(it)
        print '价格: ', its[0]['price']
        print '促销价: ', its[0]['promotion_price']

        # 是否下架
        if flag is None:
            csv_data = [str(goods_id),
                        title.encode('gb2312'),
                        str(json_data['defaultModel']['sellCountDO']['sellCount']),
                        str(its[0]['price']),
                        str(its[0]['promotion_price'])
                        ]
        else:
            csv_data = [str(goods_id),
                        title.encode('gb2312'),
                        'Sold_Out',
                        str(its[0]['price']),
                        str(its[0]['promotion_price'])
                        ]
        return " ".join(csv_data).split()

    except Exception as e:
        print 'program failed!!!'

    return None

if __name__ == '__main__':
    csvUtil = CsvUtil()
    #data = spider_taobao(567440214846)
    #spider_taobao(567469686093)
    #csvUtil.writeData(data)

    ids = csvUtil.readIds()
    i = 1
    for id in ids:
        data = spider_taobao(id)
        if data is None:
            data = [id, "NaN", "NaN", "NaN", "NaN"]
        csvUtil.writeData(data)
        print i, "finished"
        i += 1