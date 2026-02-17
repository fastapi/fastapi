# リクエストフォームとファイル { #request-forms-and-files }

`File`と`Form`を同時に使うことでファイルとフォームフィールドを定義することができます。

/// info | 情報

アップロードされたファイルやフォームデータを受信するには、まず<a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a>をインストールします。

[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成し、それを有効化してから、例えば次のようにインストールしてください:

```console
$ pip install python-multipart
```

///

## `File`と`Form`のインポート { #import-file-and-form }

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[3] *}

## `File`と`Form`のパラメータの定義 { #define-file-and-form-parameters }

ファイルやフォームのパラメータは`Body`や`Query`の場合と同じように作成します:

{* ../../docs_src/request_forms_and_files/tutorial001_an_py310.py hl[10:12] *}

ファイルとフォームフィールドがフォームデータとしてアップロードされ、ファイルとフォームフィールドを受け取ります。

また、いくつかのファイルを`bytes`として、いくつかのファイルを`UploadFile`として宣言することができます。

/// warning | 注意

*path operation*で複数の`File`と`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストのボディは`application/json`の代わりに`multipart/form-data`を使ってエンコードされているからです。

これは **FastAPI** の制限ではなく、HTTPプロトコルの一部です。

///

## まとめ { #recap }

同じリクエストでデータやファイルを受け取る必要がある場合は、`File` と`Form`を一緒に使用します。
