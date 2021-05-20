[Hello! Project Digital Books](http://www.helloproject-digitalbooks.com/) のダウンロードツールを python で書いてみました。

ソース: https://github.com/saitamanohimawari/hpdbdl

Windows 32bit バイナリ: [hpdbdl-win-1.00.zip](https://github.com/saitamanohimawari/hpdbdl/releases/download/v1.0/hpdbdl-win-1.00.zip)


## 1. このツールの目的

[Hello! Project Digital Books](http://www.helloproject-digitalbooks.com/) のダウンロード作業を簡単にし、
Hello! Project の発展に僅かながら寄与する。

## 2. 使用方法

[Hello! Project Digital Books の入会](https://www.helloproject-digitalbooks.com/user/) が必要です。

### 2.1 Windows 32bit バイナリ使用

動作環境

        Windows 8 以降 (32bit, 64bit)

python のインストールは不要です。その代わり EXEファイルが 8MB弱あります。これは pyinstaller で作られています。

[hpdbdl-win-1.00.zip](https://github.com/saitamanohimawari/hpdbdl/releases/download/v1.0/hpdbdl-win-1.00.zip) をダウンロードし、
任意のディレクトリに解凍し、書き込み可能なディレクトリを作業ディレクトリ(カレントディレクトリ)にして hpdbdl.exe を起動してください。

[ショートカット設定例](https://github.com/saitamanohimawari/hpdbdl/wiki/%E3%82%B7%E3%83%A7%E3%83%BC%E3%83%88%E3%82%AB%E3%83%83%E3%83%88%E8%A8%AD%E5%AE%9A%E4%BE%8B)
を参照してショートカットを作成すると便利です。

あとは 2.2 は読み飛ばして 2.3 から読んでください。

### 2.2 ソース(python スクリプト)使用

* python をインストールしてる人
* Windows 以外で使いたい人
* 改造したい人
* 最新コミットを使いたい人

上記の人はこちらが良いです。

動作環境

        Python 3.9.4
        + beautifulsoup4 4.9.3
        + soupsieve 2.2.1
        + Pillow 8.2.0
        + tzdata 2021.1 (option)
        + python-dateutil 2.8.1

github から任意のディレクトリに clone 

        git clone --depth 1 https://github.com/saitamanohimawari/hpdbdl.git

し、python で hpdbdl.py を起動してください。

### 2.3 以下共通

CUI にてユーザ名(メールアドレス)とパスワードを入力してください。
あとは自動で、カレントディレクトリ下の cache ディレクトリを年月別に使用(例: cache/2021-04/)してファイルがダウンロードされ、
画像ファイルのみがカレントディレクトリ下の image ディレクトリに年月別(例: image/2021-04/)にコピーされます。

1週間分の画像あたり約7分かかります。
気長にお待ちください。

2回目からは Enter キーのみで前回の設定が使用されます。

カレントディレクトリに設定ファイル hpdbdl.ini が作成されますが、
パスワードもそのまま書かれているので、
自分以外にログインできる人がいる場合は
自分しか見れないアクセス権設定にしておくことをお勧めします。

cache ディレクトリの中は2か月後に削除されます。

### 2.4 コマンドラインオプション

        -PE, --pause-on-error エラーがあれば最後に停止
        -P, --pause-at-end 最後に停止

        -S, --skip-input-account アカウント情報入力を省略

### 2.5 設定ファイル hpdbdl.ini

セクション [DEFAULT] のみ使用します。

        user_agent : サーバに送る User-Agent の文字列を指定

            例:

            user_agent = Mozilla/1.0

        start_url : ダウンロード起点の URL を指定

            例 (plusで正常に動作するかは未確認):

            start_url = http://plus.helloproject-digitalbooks.com/members/

## 3. 使用条件

(1) このソフトウエアは無保証です。

(2) 著作権表示を削ってはいけません。

(3) Hello! Project Digital Books のサーバに必要以上に負荷を掛けてはいけません。
スクリプト中の time.sleep を削ったり値を減らしてはいけません。
このツールや同様のツールの使用が妨害されたり、禁止される事態は避けたいと思います。

上の条件を満たす限り使用・改変・配布は自由です。

## 4. バージョン履歴

* 2021/04/12 [Ver.1.00 - Windows 32bit バイナリリリース](https://github.com/saitamanohimawari/hpdbdl/releases/tag/v1.0)

    設定ファイル hpdbdl.ini のセクション [DEFAULT] キー user_agent, start_url を追加

* 2021/04/08 [Ver.0.02 - Windows 32bit バイナリリリース](https://github.com/saitamanohimawari/hpdbdl/releases/tag/v0.2)

    2か月前までのキャッシュ自動クリア

    コマンドラインオプション(-PE, --pause-on-error; -P, --pause-at-end; -S, --skip-input-account)を追加

* 2021/04/07 [Ver.0.01 - Windows 32bit バイナリリリース](https://github.com/saitamanohimawari/hpdbdl/releases/tag/v0.1)

    [[BUG] 月をまたぐ瞬間に実行していると誤動作の可能性 #2](https://github.com/saitamanohimawari/hpdbdl/issues/2)

* 2021/04/04 [Ver.0.00.1 - Windows 32bit バイナリリリース](https://github.com/saitamanohimawari/hpdbdl/releases/tag/v0.0.1)

* 2021/04/01 Ver.0.00 - 初回 Windows 64bit バイナリリリース (以降は 32bit バイナリリリースのみの予定です。64bit Windows でも 32bit 版をお使いください。)

## 5. バグ報告・要望

バグ報告・要望などは github の [Issues](https://github.com/saitamanohimawari/hpdbdl/issues) へお願いします。

## 6. リンク

<A HREF='http://www.helloproject-digitalbooks.com/'>Hello! Project Digital Books</A> 

<A HREF='http://plus.helloproject-digitalbooks.com/'>Hello! Project Digital Books Plus</A> ← 未確認
