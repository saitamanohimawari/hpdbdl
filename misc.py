#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# misc.py
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

import zoneinfo
import datetime

JST = datetime.timezone(datetime.timedelta(hours=9), 'JST') # ZoneInfo がエラーの時はこの定義を使用
try:
    JST = zoneinfo.ZoneInfo('Asia/Tokyo')
except:
    pass # エラーは無視

def GetYMStringNowJST():
    "日本標準時での現在の年-月文字列"
    return datetime.datetime.now(JST).strftime("%Y-%m")

# test
if __name__ == '__main__':
    print(GetYMStringNowJST())
