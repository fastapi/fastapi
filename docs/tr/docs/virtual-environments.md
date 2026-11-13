# Virtual Environment'ler { #virtual-environments }

Python projeleriyle çalışırken, her proje için kurulan package'leri izole etmek adına bir **virtual environment** kullanmalısınız.

FastAPI projeleri için projeyi, bağımlılıklarını ve virtual environment'ini yönetmek üzere [uv](https://docs.astral.sh/uv/) kullanmanızı öneririm.

## Proje Oluşturun { #create-a-project }

`uv`'yi [resmi kurulum rehberini](https://docs.astral.sh/uv/getting-started/installation/) kullanarak kurun ve ardından bir proje oluşturun:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"
```

</div>

`uv`, proje için virtual environment'i otomatik olarak oluşturur. Kendiniz oluşturmanız veya aktive etmeniz gerekmez.

Komutları projenin environment'i içinde `uv run` ile çalıştırın, örneğin:

<div class="termy">

```console
$ uv run fastapi dev
```

</div>

## Daha Fazla Bilgi Edinin { #learn-more }

Virtual environment'lerin altta nasıl çalıştığını, activation'ı ve alternatif `python -m venv` ile `pip` workflow'unu öğrenmek için [Virtual Environments rehberini](https://tiangolo.com/guides/virtual-environments/) okuyun.
