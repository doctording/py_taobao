爬取天猫商品详情

* 输入商品ID
* 输出商品的月销量，价格，促销价等

---

567266909631 【看不到商品信息】，不用理会

566974502132 【此商品已下架】, 取得：价格，促销价

566899243847 完整，【月销量为0】

567465803837 完整，但只有价格，没有促销价

566896911989 完整： 价格，促销价，月销量

567440214846 登录后才能判断是否有促销价

价格取进入页面看到的价格；如果有款式等导致价格不一样，也可以取最小的价格


---

headers for mac

```python
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.3',
    'Referer': 'https://detail.tmall.com/item.htm',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Connection': 'keep-alive',
}
```
