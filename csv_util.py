# -*- coding=utf-8 -*-
import csv

class CsvUtil:
    def __init__(self):
        fobj = open("test.csv","wb")
        write_f = csv.writer(fobj)
        title_list = " ".join(['商品ID', '商品名称', '月销量', '价格(￥)', '促销价(￥)']).decode("utf8").encode("gb2312").split()
        write_f.writerow(title_list)
        fobj.close()

    def writeData(self, data):
        fobj = open("test.csv", "ab")
        write_f = csv.writer(fobj)
        write_f.writerow(data)
        fobj.close()

    def readIds(self):
        rows = []
        with open("ids.csv", "r") as f:
            reader = csv.reader(f)
            rows = [row[0] for row in reader]
        return rows