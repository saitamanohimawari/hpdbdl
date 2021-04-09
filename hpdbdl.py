#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# hpdbdl.py - Hello! Project Digital Books DownLoader
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

# my
import misc
import scrape
import selectcp

# PyPI
from dateutil.relativedelta import relativedelta

# std
import argparse
import configparser
import datetime
import getpass
import logging
import os
import re
import shutil
import sys
import urllib.error

try:
    version = '0.02'
    description = 'hpdbdl - Hello! Project Digital Books DownLoader Version {}'.format(version)
    copyright = 'Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)'
    url = 'https://github.com/saitamanohimawari/hpdbdl/'
    error = False
    # 設定ファイル
    # パスワードが生で書かれるので、自分しか見れないアクセス権設定にしておくことをお勧めします
    config_filename = 'hpdbdl.ini'
    # 日本標準時での2か月前の年-月文字列
    YMString2MAgo = misc.GetYMStringNowJST(relativedelta(months=-2))
    # 日本標準時での現在の年-月文字列
    YMStringNowJST = misc.GetYMStringNowJST()
    # キャッシュディレクトリのベース
    cache_base_dir = 'cache'
    # 今月のキャッシュディレクトリ
    cache_dir = os.path.join(cache_base_dir, YMStringNowJST)
    # 今月の画像ディレクトリ
    image_dir = os.path.join('image', YMStringNowJST)
    
    # コマンドラインオプション定義
    parser = argparse.ArgumentParser()
    # デバッグ
    # -d [LEVEL]
    # オプションが無いときは 0, LEVEL の省略時は 10
    parser.add_argument('-d', '--debug', help=argparse.SUPPRESS, default=0, nargs='?', const=10)
    # 単純オプション
    parser.add_argument('-S', '--skip-input-account', help='アカウント情報入力を省略', action='store_true')
    # 排他グループ
    pause_group = parser.add_mutually_exclusive_group()
    pause_group.add_argument('-PE', '--pause-on-error', help='エラーがあれば最後に停止', action='store_true')
    pause_group.add_argument('-P', '--pause-at-end', help='最後に停止', action='store_true')
    # 排他グループ
    #plus_group = parser.add_mutually_exclusive_group()
    #plus_group.add_argument('-AP', '--also-plus', help='Plus もダウンロードする', action='store_true')
    #plus_group.add_argument('-OP', '--only-plus', help='Plus だけダウンロードする', action='store_true')
    # コマンドラインオプション処理
    args = parser.parse_args()
    if args.debug:
        if int(args.debug) >= 1:
            logging.getLogger().setLevel(logging.INFO)
        if int(args.debug) >= 10:
            logging.getLogger().setLevel(logging.DEBUG)
    
    # 設定ファイル読み込み
    config = configparser.ConfigParser()
    username = ''
    password = ''
    verified = ''
    config_dirty = True
    try:
        with open(config_filename, encoding='utf-8') as fp:
            config.read_file(fp)
            username = config['DEFAULT']['username']
            password = config['DEFAULT']['password']
            verified = config['DEFAULT']['verified']
            config_dirty = False
    except:
        pass # エラーは無視
    
    # スタート
    print(description)
    print(copyright)
    print(url)
    print('')
    
    # アカウント情報入力
    if not verified or not args.skip_input_account:
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
            verified = ''
            config['DEFAULT']['username'] = username
            config['DEFAULT']['password'] = password
            config['DEFAULT']['verified'] = verified
            with open(config_filename, encoding='utf-8', mode='w') as fp:
                config.write(fp)
            print('設定ファイルを書き込みました。')
    
    # ダウンロード
    account_error = False
    print('ダウンロード開始')
    try:
        scrape.scrape('http://www.helloproject-digitalbooks.com/',
                      'http://www.helloproject-digitalbooks.com/members/',
                      username, password, cache_dir, 4, 2,
                      YMStringNowJST)
        print('ダウンロード完了しました。')
    except urllib.error.HTTPError as e:
        if e.code == 401:
            logging.error('ユーザ認証エラーです。')
            account_error = True
        else:
            logging.exception('Error: {}'.format(e))
        error = True
    except scrape.EMonthChanged as e:
        logging.error('Error: {}'.format(e))
        error = True
    except Exception as e:
        logging.exception('Error: {}'.format(e))
        error = True

    # アカウントの確認がされてなく、アカウントのエラーが無ければ、アカウント確認済みの印をつける
    if not config['DEFAULT']['verified'] and not account_error:
        verified = '1'
        config['DEFAULT']['verified'] = verified
        with open(config_filename, encoding='utf-8', mode='w') as fp:
            config.write(fp)
        print('設定ファイルを書き込みました。')
    
    # 仕分け
    print('仕分け開始')
    selectcp.select_copy(image_dir, cache_dir)
    print('仕分け完了しました。')
    
    # 2か月前までのキャッシュ自動クリア
    if os.path.isdir(cache_dir):
        for dir in os.listdir(cache_base_dir):
            path = os.path.join(cache_base_dir, dir)
            if os.path.isdir(path) and re.match(r'(\d{4})-(\d{2})', dir) and dir <= YMString2MAgo:
                print('古いキャッシュディレクトリ {} を削除します。'.format(path))
                shutil.rmtree(path)
                print('古いキャッシュディレクトリ {} を削除しました。'.format(path))

except Exception as e:                
    logging.exception('Error: {}'.format(e))
    error = True
    
if args.pause_at_end or (error and args.pause_on_error):
    if error:
        print('エラーがありました。Enter キーを入力してください。', flush=True)
    else:
        print('終了しました。Enter キーを入力してください。', flush=True)
    str = input()
