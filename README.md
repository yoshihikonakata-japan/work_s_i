# URL2QR

URL一覧からQRコードを一括生成するツール

## 説明

`URL2QR.py` は、テキストファイル（1行に1つのURL）からURLを読み取り、3つの固定サイズ（270×270、360×360、450×450ピクセル）のPNG形式QRコードを生成するPythonスクリプトです。ファイル名はURL末尾の4文字（大文字）を使用します。

## 特長

* **一括処理**：複数のURLをまとめてQRコード生成
* **複数サイズ出力**：270×270 / 360×360 / 450×450 の3サイズ
* **誤り訂正レベル**：Reed–Solomon方式の4レベル（L, M, Q, H）を選択可能
* **入力／出力パス変更**：デフォルト以外のパスを指定可能
* **ログ出力**：処理状況をINFO/ERRORレベルで出力

## 必要要件

* Python 3.7 以上
* segno（QRコード生成用）
* Pillow（画像操作用）

```bash
pip install segno pillow
```

## 使い方

```bash
python URL2QR.py [オプション]
```

### オプション

* `-i`, `--input` `<パス>`

  * URL一覧テキストファイル（1行に1つのURL）
  * デフォルト：`C:\pyQR\URL_List\URL_List.txt`

* `-o`, `--output` `<フォルダ>`

  * QRコード画像の出力先フォルダ
  * デフォルト：`C:\pyQR\QR_generate`

* `-e`, `--error-level` `{l,m,q,h}`

  * 誤り訂正レベル

    * `l`（Low）
    * `m`（Medium、デフォルト）
    * `q`（Quartile）
    * `h`（High）

## 実例

1. デフォルト設定で実行

```bash
python URL2QR.py
```

2. カスタムファイルとフォルダ、誤り訂正レベルHで実行

```bash
python URL2QR.py -i urls.txt -o qr_codes -e h
```

## 出力

URL末尾4文字を大文字化したファイル名でPNGを出力します。

例：URL末尾が `abcd` の場合

* `ABCD_270x270.png`
* `ABCD_360x360.png`
* `ABCD_450x450.png`

指定フォルダに保存されます。

## ロギング

Python標準の `logging` モジュールを使用し、以下を出力します。

* 入力ファイル未検出や生成失敗時のERROR
* 生成成功時のINFO（ファイル名、保存先など）
