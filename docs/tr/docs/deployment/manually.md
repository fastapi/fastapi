# Bir Sunucuyu Manuel Olarak Çalıştırın { #run-a-server-manually }

## `fastapi run` Komutunu Kullanın { #use-the-fastapi-run-command }

Kısacası, FastAPI uygulamanızı sunmak için `fastapi run` kullanın:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>2306215</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
```

</div>

Bu, çoğu durumda işinizi görür. 😎

Örneğin bu komutu, **FastAPI** app'inizi bir container içinde, bir sunucuda vb. başlatmak için kullanabilirsiniz.

## ASGI Sunucuları { #asgi-servers }

Şimdi biraz daha detaya inelim.

FastAPI, Python web framework'leri ve sunucularını inşa etmek için kullanılan <abbr title="Asynchronous Server Gateway Interface - Asenkron Sunucu Ağ Geçidi Arayüzü">ASGI</abbr> adlı bir standardı kullanır. FastAPI bir ASGI web framework'üdür.

Uzak bir sunucu makinesinde **FastAPI** uygulamasını (veya herhangi bir ASGI uygulamasını) çalıştırmak için gereken ana şey, **Uvicorn** gibi bir ASGI server programıdır. `fastapi` komutuyla varsayılan olarak gelen de budur.

Buna alternatif birkaç seçenek daha vardır, örneğin:

* <a href="https://www.uvicorn.dev/" class="external-link" target="_blank">Uvicorn</a>: yüksek performanslı bir ASGI server.
* <a href="https://hypercorn.readthedocs.io/" class="external-link" target="_blank">Hypercorn</a>: diğer özelliklerin yanında HTTP/2 ve Trio ile uyumlu bir ASGI server.
* <a href="https://github.com/django/daphne" class="external-link" target="_blank">Daphne</a>: Django Channels için geliştirilmiş ASGI server.
* <a href="https://github.com/emmett-framework/granian" class="external-link" target="_blank">Granian</a>: Python uygulamaları için bir Rust HTTP server.
* <a href="https://unit.nginx.org/howto/fastapi/" class="external-link" target="_blank">NGINX Unit</a>: NGINX Unit, hafif ve çok yönlü bir web uygulaması runtime'ıdır.

## Sunucu Makinesi ve Sunucu Programı { #server-machine-and-server-program }

İsimlendirme konusunda akılda tutulması gereken küçük bir detay var. 💡

"**server**" kelimesi yaygın olarak hem uzak/bulut bilgisayarı (fiziksel veya sanal makine) hem de o makinede çalışan programı (ör. Uvicorn) ifade etmek için kullanılır.

Dolayısıyla genel olarak "server" dendiğinde, bu iki şeyden birini kast ediyor olabilir.

Uzak makineden bahsederken genelde **server** denir; ayrıca **machine**, **VM** (virtual machine), **node** ifadeleri de kullanılır. Bunların hepsi, genellikle Linux çalıştıran ve üzerinde programlarınızı çalıştırdığınız bir tür uzak makineyi ifade eder.

## Sunucu Programını Yükleyin { #install-the-server-program }

FastAPI'yi kurduğunuzda, production sunucusu olarak Uvicorn da beraberinde gelir ve bunu `fastapi run` komutuyla başlatabilirsiniz.

Ancak bir ASGI server'ı manuel olarak da kurabilirsiniz.

Bir [sanal ortam](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan, etkinleştirdiğinizden emin olun; ardından server uygulamasını kurabilirsiniz.

Örneğin Uvicorn'u kurmak için:

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

Benzer bir süreç, diğer ASGI server programlarının tamamı için de geçerlidir.

/// tip | İpucu

`standard` eklediğinizde Uvicorn, önerilen bazı ek bağımlılıkları kurar ve kullanır.

Bunlara, `asyncio` için yüksek performanslı bir drop-in replacement olan ve concurrency performansını ciddi şekilde artıran `uvloop` da dahildir.

FastAPI'yi `pip install "fastapi[standard]"` gibi bir şekilde kurduğunuzda `uvicorn[standard]` da zaten kurulmuş olur.

///

## Sunucu Programını Çalıştırın { #run-the-server-program }

Bir ASGI server'ı manuel olarak kurduysanız, FastAPI uygulamanızı import edebilmesi için genellikle özel bir formatta bir import string geçirmeniz gerekir:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 80

<span style="color: green;">INFO</span>:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

</div>

/// note | Not

`uvicorn main:app` komutu şunları ifade eder:

* `main`: `main.py` dosyası (Python "module").
* `app`: `main.py` içinde `app = FastAPI()` satırıyla oluşturulan nesne.

Şununla eşdeğerdir:

```Python
from main import app
```

///

Her alternatif ASGI server programı için benzer bir komut bulunur; daha fazlası için ilgili dokümantasyonlarına bakabilirsiniz.

/// warning | Uyarı

Uvicorn ve diğer sunucular, geliştirme sırasında faydalı olan `--reload` seçeneğini destekler.

`--reload` seçeneği çok daha fazla kaynak tüketir, daha kararsızdır vb.

**Geliştirme** sırasında çok yardımcı olur, ancak **production** ortamında kullanmamalısınız.

///

## Deployment Kavramları { #deployment-concepts }

Bu örnekler server programını (ör. Uvicorn) çalıştırır; **tek bir process** başlatır, tüm IP'lerde (`0.0.0.0`) ve önceden belirlenmiş bir port'ta (ör. `80`) dinler.

Temel fikir budur. Ancak muhtemelen şunlar gibi bazı ek konularla da ilgilenmek isteyeceksiniz:

* Güvenlik - HTTPS
* Açılışta çalıştırma
* Yeniden başlatmalar
* Replikasyon (çalışan process sayısı)
* Bellek
* Başlatmadan önceki adımlar

Sonraki bölümlerde bu kavramların her birini nasıl düşünmeniz gerektiğini ve bunlarla başa çıkmak için kullanabileceğiniz somut örnekleri/stratejileri anlatacağım. 🚀
