# -*- coding=utf-8 -*-
import re
import urllib2
import json
from bs4 import BeautifulSoup
from proxy import IpProxy
from csv_util import CsvUtil
import const
from data_dto import GoodsDto

const.SOLD_OUT = "Sold_Out"
const.NOT_FOUND = "Goods_Not_Found"
const.NO_PROMOTION = "No_Promotion"
const.NONE = "Nan"


def spider_taobao(goods_id):
    """
    爬虫方法
    :param goods_id: 
    :return: 
    """

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.3',
        'Referer': 'https://detail.tmall.com/item.htm',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Connection': 'keep-alive',
    }

    url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.57.25a11005L60sXF&id={}&skuId=3759128262116&areaId=310100&user_id=1695300927&cat_id=53412001&is_b=1&rn=c859285b1d0f5de17c3f2c3666916175'.format(str(goods_id))
    # print "=====商品ID:", goods_id

    # 设置代理
    ip_proxy = IpProxy()

    try:
        req = urllib2.Request(url=url, headers=headers)
        # 使用 opener.open()方法，代理
        proxy_handler = urllib2.ProxyHandler(ip_proxy.get_proxy())
        opener = urllib2.build_opener(proxy_handler)
        res = opener.open(req).read().decode('gbk', 'ignore')
    except Exception as e:
        print 'Failed:', e

    # 1. 商品名称
    soup = BeautifulSoup(res, "html.parser")
    try:
        title = soup.find("input", attrs={'name': "title"})['value']
    except Exception as e:
        try:
            title = soup.find("div", attrs={'class': "tb-detail-hd"})
            h1 = title.h1.string
            h1 = h1.replace("\r", "").replace("\n", "").replace("\t", "")

            title = h1
        except Exception as e:
            print "Not found such goods", e.message
            goods = GoodsDto(str(goods_id), const.NOT_FOUND, const.NONE, const.NONE, const.NONE)
            return goods.get_csv_data()

    title = "".join(title)
    title = title.replace(" ", "_")
    # print "名称: ", title

    # 2. 是否下架
    sold_out = soup.find("div", attrs={'class': "sold-out-left"})

    try:
        purl = "https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=true&isSecKill=false&tmallBuySupport=true&isAreaSell=true&tryBeforeBuy=false&offlineShop=false&itemId={}&showShopProm=false&cachedTimestamp=1531703147517&isPurchaseMallPage=false&isRegionLevel=true&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=3&isForbidBuyItem=false&callback=setMdskip&timestamp=1531713077230&isg=null&isg2=BAgI7R06x2foMCvkXVYVGGag2Xa2oW0PVPAVOMK5cQN2nagHasE8S54UETVIrSST&areaId=310100&cat_id=53412001".format(str(goods_id))

        price_req = urllib2.Request(url=purl, headers=headers)
        # 使用 opener.open()方法，代理
        price_res = opener.open(price_req).read().decode('gb2312').encode('utf-8')

        # 3. 详细商品信息对象
        p1 = re.compile(r'[(](.*)[)]', re.S)
        rs = re.findall(p1, price_res)
        rs = rs[0]
        # 转换为 json 对象
        json_data = json.loads(rs)

        # 月销量
        # print '月销量: ', json_data['defaultModel']['sellCountDO']['sellCount']

        # 库存
        sku_quantity = json_data['defaultModel']['inventoryDO']['skuQuantity']

        # 4. 每个类目的所有分类商品的信息
        its = []
        dic = json_data['defaultModel']['itemPriceResultDO']['priceInfo']
        # Id， 价格， 促销价， 库存
        for d, x in dic.items():
            # 是否促销
            if 'promotionList' in x:
                it = {'id': d,
                      'price':  x['price'],
                      'promotion_price': x['promotionList'][0]['price'],
                      'quantity': sku_quantity[d]['quantity']}
            else:
                it = {'id': d,
                      'price': x['price'],
                      'promotion_price': const.NO_PROMOTION,
                      'quantity': sku_quantity[d]['quantity']}
            its.append(it)
        # print '价格: ', its[0]['price']
        # print '促销价: ', its[0]['promotion_price']

        # 5. 构造csv对象
        if sold_out is None:
            goods = GoodsDto(str(goods_id),
                             title.encode('gb2312'),
                             str(json_data['defaultModel']['sellCountDO']['sellCount']),
                             str(its[0]['price']),
                             str(its[0]['promotion_price']))
        else:
            goods = GoodsDto(str(goods_id),
                             title.encode('gb2312'),
                             const.SOLD_OUT,
                             str(its[0]['price']),
                             str(its[0]['promotion_price']))
        # 显示结果
        goods.display_goods()
        return goods.get_csv_data()

    except Exception as e:
        print 'Program Failed:', e.message

    return None


def test_proxy():
    ip_proxy = IpProxy()
    proxies = ip_proxy.get_proxy()
    proxy_s = urllib2.ProxyHandler(proxies)
    opener = urllib2.build_opener(proxy_s)
    urllib2.install_opener(opener)
    content = urllib2.urlopen('http://ip.catr.cn/').read()
    print content


def test_spider_one(goods_id):
    csvs = CsvUtil()
    csvs.create_des()
    data = spider_taobao(goods_id)
    if data is None:
        data = [goods_id, const.NOT_FOUND, const.NONE, const.NONE, const.NONE]
    csvs.write_to_des(data)


def spider_data():
    csvs = CsvUtil()
    csvs.create_des()
    goods_ids = csvs.read_source()
    i = 1
    for goods_id in goods_ids:
        data = spider_taobao(goods_id)
        if data is None:
            data = [goods_id, const.NOT_FOUND, const.NONE, const.NONE, const.NONE]
        csvs.write_to_des(data)
        print i, "finished"
        i += 1


if __name__ == '__main__':
    # test_proxy()
    # test_spider_one(566896911989)
    spider_data()
