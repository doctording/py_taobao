# -*- coding=utf-8 -*-


class GoodsDto:
    """csv数据对象
    """

    def __init__(self, goods_id, title, quantity, price, promotion_price):
        self.goods_id = goods_id
        self.title = title
        self.quantity = quantity
        self.price = price
        self.promotion_price = promotion_price

    def display_goods(self):
        print "====="
        print "商品ID: ", self.goods_id
        print "名称: ", self.title.decode("gb2312").encode('utf-8')
        # print "名称: ", self.title
        print "月销量: ", self.quantity
        print "价格: ", self.price
        print "促销价格", self.promotion_price

    def get_csv_data(self):
        return [self.goods_id, self.title, self.quantity, self.price, self.promotion_price]
