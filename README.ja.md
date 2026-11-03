# Coding Agent 向け NIST CSF 2.0 ローカル資料

[English](README.md)

このリポジトリは、取得元を固定した `sources.json`、`make run`、英語の項目別 Markdown、JSON 索引、NIST 公式日本語訳へのリンク一覧を備えます。

## 原本の取得と索引の生成

必要なコマンドは `uv` と `curl` です。英語版の原本を取得する際に実行します。

```sh
make run
```

英語版 Reference Tool のエクスポートを `generated/source/` に保存し、現行の CSF 2.0 の各 ID について Markdown を `generated/sections/` に、索引を `generated/index.json` に生成します。エクスポートに含まれる廃止済み ID は除外します。

`make validate` は、6 つの Function、22 の Category、106 の Subcategory、生成ファイル、英語原本のハッシュ値、日本語リンクを確認します。取得した原本と生成物はローカルに保存され、Git の追跡対象から除外されます。

## 項目を読む

`generated/index.json` で ID を探し、英語版は `generated/sections/GV.OC-01.md` を読みます。日本語版は [`ja/index.md`](ja/index.md) で同じ ID を探し、NIST の公式和訳 PDF の該当ページを開きます。複数の項目が同じページにあるため、ページ内で ID を確認してください。

公式和訳 PDF は CSF コアを対象とし、英語版 Reference Tool の実装例は含みません。このリポジトリでは日本語本文の複製や翻訳を行いません。

## 取得元

原本の URL は `sources.json` に記載しています。公式日本語訳の公開ページは [NIST CSWP 29 jpn](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20-japanese-translation) です。
