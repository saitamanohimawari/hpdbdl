# <makefile> -*-makefile-*-
#
# Project hpdbdl
#

# Windows 32bit の python 環境で pyinstaller により実行モジュールをビルド
dist\hpdbdl.exe : hpdbdl.py misc.py scrape.py selectcp.py makefile VersionInfoFile.txt
	py -3.9-32 build.py hpdbdl.py --onefile --version-file VersionInfoFile.txt

# Local variables:
# indent-tabs-mode: t
# End: 
