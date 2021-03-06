#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# scrape.py
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

# my
import misc

# PyPI
from bs4 import BeautifulSoup

# std
import configparser
import http.cookiejar
import logging
import os
import re
import time
import urllib.parse
import urllib.request

class EMonthChanged(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "ダウンロード中に月が変わりました。"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

def set_user_agent(ua):
    global user_agent
    user_agent = ua
    
def scrape(starturl, # スクレイピングを開始する URL
           username, # BASIC認証ユーザ名
           password, # BASIC認証パスワード
           outdir, # 出力ディレクトリ
           limit_level, # 開始 URL からの参照回数の上限
           force_download_level, # 開始 URL からの参照回数がこの値未満の場合ローカルファイルがあっても取得する
           YMStringNowJST # スタート時点の日本標準時での年-月文字列
           ):

    baseurl = starturl
    # パスワードマネージャ生成
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    # username と password を追加
    password_mgr.add_password(None, baseurl, username, password)
    # ハンドラ作成
    cert_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    # クッキー処理のハンドラを作成
    cookie_handler = urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    # オープナーを生成 "opener" (OpenerDirector のインスタンス)
    opener = urllib.request.build_opener(cert_handler, cookie_handler)
    # オープナーを使用する URL を指定
    opener.open(baseurl)
    # オープナーをインストール
    # これで urllib.request.urlopen の呼び出しはこのオープナーを使用する
    urllib.request.install_opener(opener)

    # User-Agent を含むヘッダを作る
    logging.info('user_agent={}'.format(user_agent))
    headers = {'User-Agent': user_agent}

    # ローカルディレクトリの準備
    os.makedirs(outdir, exist_ok=True)

    # ダウンロード済み URL
    downloaded_urls = set()
    
    urls = set([starturl])
    for level in range(0,limit_level):
        logging.info('level {}'.format(level))
        next_urls = set()
        for url in sorted(urls):
            try:
                if url in downloaded_urls:
                    continue
                logging.info('url={}'.format(url))
                # url をパース
                parse_result = urllib.parse.urlparse(url)
                logging.debug('path={},params={},query={}'.format(parse_result.path, parse_result.params, parse_result.query))
                # ローカルファイル名を決める
                localfile = parse_result.path.replace('/', '_')
                if parse_result.query:
                    localfile += '_' + parse_result.query
                logging.debug('localfile={}'.format(localfile))
                # ローカルパス名
                localpath = '/'.join([outdir, localfile])
                logging.info('localpath={}'.format(localpath))
                # 取得
                if not os.path.isfile(localpath) or level < force_download_level:
                    print('ダウンロード中: {}'.format(url))
                    time.sleep(2.0)
                    req = urllib.request.Request(url, headers = headers)
                    with urllib.request.urlopen(req) as response:
                        the_page = response.read()
                    if YMStringNowJST != misc.GetYMStringNowJST():
                        raise EMonthChanged
                    with open(localpath, mode='wb') as fp:
                        fp.write(the_page)
                downloaded_urls.add(url)
                # 解析
                doc = []
                clines = 0
                with open(localpath, encoding='utf-8') as fp:
                    while fp.readable():
                        try:
                            line = fp.readline()
                        except Exception as e:
                            # 解析エラーは握りつぶしていい
                            logging.debug('{} : {}'.format(localpath, e))
                        doc.append(line)
                        clines += 1
                        logging.debug('{}:{}'.format(clines, line))
                        if not line:
                            break
                logging.debug('clines={}'.format(clines))
                soup = BeautifulSoup(''.join(doc), features='html.parser')
                a_tags = soup.findAll('a')
                logging.debug('a_tags={}'.format(len(a_tags)))
                for i in a_tags:
                    href = i.get('href')
                    if not href:
                        continue
                    logging.debug('href={}'.format(href))
                    parse_result = urllib.parse.urlparse(href)
                    if parse_result.scheme or parse_result.netloc:
                        logging.debug('other site');
                        continue
                    new_url = urllib.parse.urljoin(url, href)
                    logging.debug('new_url={}'.format(new_url))
                    next_urls.add(new_url)
                img_tags = soup.findAll('img')
                logging.debug('img_tags={}'.format(len(img_tags)))
                for i in img_tags:
                    src = i.get('src')
                    logging.debug('src={}'.format(src))
                    new_url = urllib.parse.urljoin(url, src)
                    logging.debug('new_url={}'.format(new_url))
                    next_urls.add(new_url)
            except EMonthChanged as e:
                raise e
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    raise e
                if e.code == 404 and re.search(r'spacer\.gif$', url): # こいつだけはいつもエラーになるので
                    logging.info('urllib.error.HTTPError: {} at {} : spacer.gif のエラーは無視します'.format(e, url))
                else:
                    logging.exception('urllib.error.HTTPError: {} at {}'.format(e, url))
            except Exception as e:
                raise e
        urls = next_urls
        
# module test
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    # 認証情報を個別ファイルに書いておくこと
    #
    # 例: 
    #     ; -*- coding: utf-8 -*-
    #     [DEFAULT]
    #     UserName=meiru@adore.su
    #     Password=pasuwaado
    #
    config_filename = 'private/scrape.ini'
    #
    config = configparser.ConfigParser()
    with open(config_filename, encoding='utf-8') as fp:
        config.read_file(fp)
    username = config['DEFAULT']['UserName']
    logging.info('username={}'.format(username))
    password = config['DEFAULT']['Password']
    logging.info('password={}'.format(password))
    scrape('http://www.helloproject-digitalbooks.com/members/',
           username, password, 'tmp/scraping_test', 4, 2, misc.GetYMStringNowJST)
