# coding: utf-8
from mongoengine import *
import pandas as pd
#import os

connect('financial')


class stock_price(Document):
    stock_id = StringField(max_length=20, required=True, unique=True)
    data = DictField()
    meta = {
        'indexes': ['stock_id']
    }


def get_P_data(name):
    df = pd.read_csv(name, parse_dates=[1])
    df.columns = ["Ticker", "Date/Time", "Open", "High", "Low", "Close", "Volume"]
    df.sort_values("Ticker", inplace=True)
    df.set_index(["Ticker", "Date/Time"], inplace=True)
    df.sort_index(ascending=[True, False], inplace=True)
    return df


hose_p = get_P_data("home/data/CafeF.RAW_HSX.Upto17.03.2017.csv")
#hnx_p = get_P_data("home/data/CafeF.RAW_HNX.Upto17.03.2017.csv")


#p = pd.concat([hose_p,hnx_p])
for i in hose_p.index.get_level_values(0).unique():
    data = hose_p.ix[i].copy()
    last_p = data.ix[0]
    last_p = last_p.to_frame().T
    data.reset_index(inplace=True)
    data["month"] = data["Date/Time"].dt.month
    data["month"] = data["month"].shift(1)
    data = data[data["Date/Time"].dt.month > data["month"]]
    data.set_index("Date/Time", inplace=True)

    data = last_p.append(data)
    data.drop("month", axis=1, inplace=True)

    data.index = data.index.astype("str")
    for col in data.columns:
        data[col] = data[col].astype("str")
    try:
        stock_price_inst = stock_price(stock_id=i, data=data.to_dict())
        stock_price_inst.save()
    except Exception as e:
        print(e)
    print(i)
