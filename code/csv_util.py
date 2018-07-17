# -*- coding=utf-8 -*-
import csv


class CsvUtil:
    """csv操作工具
    excel 打开 csv 文件时，识别 gb2312 编码，不能识别 utf-8
    """

    def __init__(self):
        self.source = "../data/ids.csv"
        self.destination = "../data/test.csv"

    def create_des(self):
        with open(self.destination, "wb") as f:
            write_f = csv.writer(f)
            title_list = " ".join(['商品ID', '商品名称', '月销量', '价格(￥)', '促销价(￥)']).decode("utf8").encode("gb2312").split()
            write_f.writerow(title_list)

    def write_to_des(self, data):
        with open(self.destination, "ab") as f:
            write_f = csv.writer(f)
            write_f.writerow(data)

    def read_source(self):
        with open(self.source, "r") as f:
            reader = csv.reader(f)
            rows = [row[0] for row in reader]
        return rows
