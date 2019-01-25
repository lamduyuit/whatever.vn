# coding: utf-8
from mongoengine import *
import pandas as pd
import os
# Thay report_name va duong dan toi file
connect('financial')
report_type = "yearly"
report_name = "CSTC"
# CDKT,KQKD,LCTT,CSTC


class report_yearly(Document):
    stock_id = StringField(max_length=10, required=True)
    data = DictField()
    report_name = StringField(max_length=4, required=True)
    meta = {
        'indexes': ['stock_id', ('stock_id', 'report_name')]
    }


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home/data/')

#list_file in directory
"""
for file in os.listdir(data_path):
	print(data_path+file)
"""


class report_quaterly(Document):
    stock_id = StringField(max_length=10, required=True)
    data = DictField()
    report_name = StringField(max_length=4, required=True)
    meta = {
        'indexes': ['stock_id', ('stock_id', 'report_name')]
    }


# Khi doc quaterly khong can sap xep lai columns
# khi doc yearly can drop Attribute roi insert lai
df = pd.read_csv("home/data/cstc2.csv", index_col="stock_id")
print(report_type, "===", report_name)
for i in df.index.unique():
    mongodf = df.ix[i].copy()
    if report_type == "yearly":
        if "Unnamed: 1" in mongodf.columns:
            mongodf.rename(columns={"Unnamed: 1": "index"}, inplace=True)
    # mongodf.set_index("index",inplace=True)
    mongodf.reset_index(drop=True, inplace=True)
    mongodf.index = mongodf.index.astype("str")
    for col in mongodf.columns:
        mongodf[col] = mongodf[col].astype("str")
    if report_type == "yearly":
        report_yearly_inst = report_yearly(stock_id=str(i), report_name=report_name, data=mongodf.to_dict())
        report_yearly_inst.save()
    else:
        report_quaterly_inst = report_quaterly(stock_id=str(i), report_name=report_name, data=mongodf.to_dict())
        report_quaterly_inst.save()
    print(i)
