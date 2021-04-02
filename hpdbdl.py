#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# hpdbdl.py - Hello! Project Digital Books DownLoader
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

import configparser
import datetime
import getpass
import os
import scrape
import selectcp
import sys

version = '0.00'
# 設定ファイル
# パスワードが生で書かれるので、自分しか見れないアクセス権設定にしておくことをお勧めします
config_filename = 'hpdbdl.ini'
# 今月のキャッシュディレクトリ
cache_dir = 'cache/' + datetime.date.today().strftime("%Y-%m")
# 今月の画像ディレクトリ
image_dir = 'image/' + datetime.date.today().strftime("%Y-%m")

# 設定ファイル読み込み
config = configparser.ConfigParser()
username = ''
password = ''
config_dirty = True
try:
    with open(config_filename, encoding='utf-8') as fp:
        config.read_file(fp)
        username = config['DEFAULT']['username']
        password = config['DEFAULT']['password']
        config_dirty = False
except:
    pass # エラーは無視

# スタート
print('hpdbdl - Hello! Project Digital Books DownLoader Version {}'.format(version))
print('Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)')
print('https://github.com/saitamanohimawari/hpdbdl/')
print('')

# 入力
print('ユーザ名 [{0}]: '.format(username), end='', flush=True)
str = input()
if str != '':
    username = str
    config_dirty = True
password_entered = ''
if password:
    password_entered = '入力済み'
print('パスワード [{0}]: '.format(password_entered), end='', flush=True)
str = getpass.getpass('')
if str != '':
    password = str
    config_dirty = True

# ファイル書き込み
if config_dirty:
    config['DEFAULT']['username'] = username
    config['DEFAULT']['password'] = password
    with open(config_filename, encoding='utf-8', mode='w') as fp:
        config.write(fp)
    print('設定ファイルを書き込みました。')

# ダウンロード
print('ダウンロード開始')
scrape.scrape('http://www.helloproject-digitalbooks.com/',
              'http://www.helloproject-digitalbooks.com/members/',
              username, password, cache_dir, 4, 2)
print('ダウンロード完了しました。')

# 仕分け
print('仕分け開始')
selectcp.select_copy(image_dir, cache_dir)
print('仕分け完了しました。')