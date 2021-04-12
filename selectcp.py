#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# selectcp.py
# Copyright (C) 2021 saitamanohimawari (埼玉の向日葵)
# https://github.com/saitamanohimawari/hpdbdl/
#

# PyPI
from PIL import Image

# std
import logging
import os
import re
import shutil

def select_copy(target_dir, source_dir):
    os.makedirs(target_dir, exist_ok=True)
    for i in os.listdir(source_dir):
        try:
            path = os.path.join(source_dir, i)
            if not os.path.isfile(path):
                continue
            size = os.path.getsize(path) # 100KB 以下をサムネイルとみなしてスキップ
            if size < 100000:
                continue
            search_result = re.search(r'(\d+)\D+(\d+)$', i)
            if not search_result:
                continue
            g1 = search_result.group(1)
            g2 = search_result.group(2)
            if re.match(r'9+', g1) or re.match(r'9+', g2):
                continue
            img = Image.open(path) # 画像としてオープンできるか試す
            logging.debug(img)
            target_file = os.path.join(target_dir, '{}-{}.jpg'.format(g1, g2))
            print('画像ファイルコピー: {}'.format(target_file))
            shutil.copy2(path, target_file)
        except Exception as e:
            logging.info(e)

# module test
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    target_dir = 'tmp/img'
    source_dir = 'tmp/scraping_test'
    select_copy(target_dir, source_dir)
