#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Project hpdbdl
#
# build.py - 現在実行している python と同じ環境の pyinstaller を呼び出し
#
# usage: py -3.9-32 build.py hpdbdl.py --onefile --version-file VersionInfoFile.txt
#

import os
import subprocess
import sys

dir = os.path.dirname(sys.executable); # dir of python
cmd = os.path.join(dir, 'Scripts', 'pyinstaller') # full path of pyinstaller
cmdline = cmd + ' ' + ' '.join(sys.argv[1:]) # add arguments
print("build.py: call:", cmdline, flush=True)
subprocess.call(cmdline)
