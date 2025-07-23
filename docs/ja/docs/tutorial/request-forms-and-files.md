# リクエストフォームとファイル

`File`と`Form`を同時に使うことでファイルとフォームフィールドを定義することができます。

/// info | 情報

アップロードされたファイルやフォームデータを受信するには、まず<a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>をインストールします。

例えば、`pip install python-multipart`のように。

///

## `File`と`Form`のインポート

{* ../../docs_src/request_forms_and_files/tutorial001.py hl[1] *}

## `File`と`Form`のパラメータの定義

ファイルやフォームのパラメータは`Body`や`Query`の場合と同じように作成します:

{* ../../docs_src/request_forms_and_files/tutorial001.py hl[8] *}

ファイルとフォームフィールドがフォームデータとしてアップロードされ、ファイルとフォームフィールドを受け取ります。

また、いくつかのファイルを`bytes`として、いくつかのファイルを`UploadFile`として宣言することができます。

/// warning | 注意

*path operation*で複数の`File`と`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストのボディは`application/json`の代わりに`multipart/form-data`を使ってエンコードされているからです。

これは **FastAPI** の制限ではなく、HTTPプロトコルの一部です。

///

## まとめ

同じリクエストでデータやファイルを受け取る必要がある場合は、`File` と`Form`を一緒に使用します。
