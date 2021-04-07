#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# misc.py
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

# PyPI
from dateutil.relativedelta import relativedelta

# std
import datetime
import zoneinfo

JST = datetime.timezone(datetime.timedelta(hours=9), 'JST') # ZoneInfo がエラーの時はこの定義を使用
try:
    JST = zoneinfo.ZoneInfo('Asia/Tokyo')
except:
    pass # エラーは無視

def GetYMStringNowJST(delta = relativedelta(months=0)):
    "日本標準時での現在の年-月文字列"
    return (datetime.datetime.now(JST) + delta).strftime("%Y-%m")

# test
if __name__ == '__main__':
    print(GetYMStringNowJST())
    print(GetYMStringNowJST(relativedelta(months=-1)))
    print(GetYMStringNowJST(relativedelta(months=-2)))
    print(GetYMStringNowJST(relativedelta(months=-3)))
    print(GetYMStringNowJST(relativedelta(months=-4)))
