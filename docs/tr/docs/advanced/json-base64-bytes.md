# JSON'da Bytes'i Base64 Olarak Kullanma { #json-with-bytes-as-base64 }

Uygulamanız JSON veri alıp gönderiyorsa ve bunun içine ikili (binary) veri eklemeniz gerekiyorsa, veriyi base64 olarak encode edebilirsiniz.

## Base64 ve Dosyalar { #base64-vs-files }

İkili veriyi JSON içinde encode etmek yerine, yükleme için [Request Files](../tutorial/request-files.md) ve gönderim için [Custom Response - FileResponse](./custom-response.md#fileresponse--fileresponse-) kullanıp kullanamayacağınıza önce bir bakın.

JSON sadece UTF-8 ile encode edilmiş string'ler içerebilir, dolayısıyla ham bytes içeremez.

Base64 ikili veriyi string olarak encode edebilir, ancak bunu yapmak için orijinal ikili veriden daha fazla karakter kullanır; bu yüzden genellikle normal dosyalardan daha verimsiz olur.

Base64'ü sadece gerçekten JSON içine ikili veri koymanız gerekiyorsa ve bunun için dosya kullanamıyorsanız tercih edin.

## Pydantic `bytes` { #pydantic-bytes }

`bytes` alanları olan bir Pydantic model tanımlayabilir, ardından model config'inde `val_json_bytes` kullanarak giriş JSON verisini base64 ile doğrulamasını (validate) söyleyebilirsiniz; bu doğrulamanın bir parçası olarak base64 string'i bytes'a decode eder.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:9,29:35] hl[9] *}

`/docs`'a bakarsanız, `data` alanının base64 ile encode edilmiş bytes beklediğini görürsünüz:

<div class="screenshot">
<img src="/img/tutorial/json-base64-bytes/image01.png">
</div>

Şöyle bir request gönderebilirsiniz:

```json
{
    "description": "Some data",
    "data": "aGVsbG8="
}
```

/// tip | İpucu

`aGVsbG8=` değeri, `hello` kelimesinin base64 encoding'idir.

///

Sonrasında Pydantic base64 string'ini decode eder ve modelin `data` alanında size orijinal bytes'ı verir.

Şöyle bir response alırsınız:

```json
{
  "description": "Some data",
  "content": "hello"
}
```

## Çıkış Verisi için Pydantic `bytes` { #pydantic-bytes-for-output-data }

Çıkış verisi için de model config'inde `ser_json_bytes` ile `bytes` alanları kullanabilirsiniz; Pydantic JSON response üretirken bytes'ı base64 olarak serialize eder.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,12:16,29,38:41] hl[16] *}

## Giriş ve Çıkış Verisi için Pydantic `bytes` { #pydantic-bytes-for-input-and-output-data }

Elbette, aynı modeli base64 kullanacak şekilde yapılandırıp hem girişte (*validate*) `val_json_bytes` ile hem de çıkışta (*serialize*) `ser_json_bytes` ile JSON veri alıp gönderirken kullanabilirsiniz.

{* ../../docs_src/json_base64_bytes/tutorial001_py310.py ln[1:2,19:26,29,44:46] hl[23:26] *}
