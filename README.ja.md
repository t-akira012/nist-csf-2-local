# Coding Agent 向け NIST CSF 2.0 ローカル資料

[English](README.md)

このリポジトリは、取得元を固定した `sources.json`、`make run`、項目別 Markdown、JSON 索引、Agent 向け参照規則を備えます。取得元は NIST の英語版 CSF 2.0 Reference Tool のエクスポートと、公式日本語訳です。

## 原本の取得と索引の生成

必要なコマンドは `uv`、`curl`、`pdftotext`（Poppler）です。原本を取得する際に実行します。

```sh
make run
```

英語版と日本語版の原本を `generated/source/` に保存し、現行の CSF 2.0 の各 ID について英語 Markdown を `generated/sections/` に、索引を `generated/index.json` に生成します。英語版エクスポートに含まれる廃止済み ID は除外します。

`make validate` は、6 つの Function、22 の Category、106 の Subcategory、生成ファイル、原本のハッシュ値を確認します。原本と生成物はローカルに保存され、Git の追跡対象から除外されます。

## 必要な項目だけ日本語で読む

`generated/index.json` で ID を探し、英語版は `generated/sections/GV.OC-01.md` を読みます。日本語版が必要な場合は、対象 ID を指定します。

```sh
make ja ID=GV.OC-01
```

このコマンドは `ja/GV.OC-01.md` だけを作成します。CSF コアの文言は NIST の公式和訳 PDF から取得し、翻訳し直しません。英語の項目に実装例がある場合は、その実装例だけをローカルの Codex CLI で訳し、非公式訳と明記します。`make run` では一括翻訳を行いません。既存の日本語ファイルは上書きしません。再生成する場合は、対象ファイルを削除してから実行します。

`ja/` は Git の追跡対象から除外されます。非公式訳を引用・公開する前に内容を確認してください。公式和訳 PDF には権利留保の記載があるため、このリポジトリには PDF と抽出した本文をコミットしません。

## 取得元

原本の URL は `sources.json` に記載しています。公式日本語訳の公開ページは [NIST CSWP 29 jpn](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20-japanese-translation) です。
