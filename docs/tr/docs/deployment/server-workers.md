# Server Workers - Worker'larla Uvicorn { #server-workers-uvicorn-with-workers }

Önceki bölümlerde bahsettiğimiz deployment kavramlarına tekrar bakalım:

* Güvenlik - HTTPS
* Başlangıçta çalıştırma
* Yeniden başlatmalar
* **Replikasyon (çalışan process sayısı)**
* Bellek
* Başlatmadan önceki adımlar

Bu noktaya kadar, dokümantasyondaki tüm tutorial'larla muhtemelen bir **server programı** çalıştırıyordunuz; örneğin Uvicorn'u çalıştıran `fastapi` komutunu kullanarak ve **tek bir process** ile.

Uygulamaları deploy ederken, **çok çekirdekten (multiple cores)** faydalanmak ve daha fazla request'i karşılayabilmek için büyük olasılıkla **process replikasyonu** (birden fazla process) isteyeceksiniz.

[Daha önceki Deployment Concepts](concepts.md){.internal-link target=_blank} bölümünde gördüğünüz gibi, kullanabileceğiniz birden fazla strateji var.

Burada, `fastapi` komutunu kullanarak ya da `uvicorn` komutunu doğrudan çalıştırarak **worker process**'lerle **Uvicorn**'u nasıl kullanacağınızı göstereceğim.

/// info | Bilgi

Container kullanıyorsanız (örneğin Docker veya Kubernetes ile), bununla ilgili daha fazlasını bir sonraki bölümde anlatacağım: [Container'larda FastAPI - Docker](docker.md){.internal-link target=_blank}.

Özellikle **Kubernetes** üzerinde çalıştırırken, büyük olasılıkla worker kullanmak **istemeyeceksiniz**; bunun yerine **container başına tek bir Uvicorn process** çalıştırmak daha uygundur. Ancak bunu da o bölümde detaylandıracağım.

///

## Birden Fazla Worker { #multiple-workers }

Komut satırında `--workers` seçeneğiyle birden fazla worker başlatabilirsiniz:

//// tab | `fastapi`

`fastapi` komutunu kullanıyorsanız:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting production server 🚀

             Searching for package file structure from directories with
             <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with the
             following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000/docs</u></font>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://0.0.0.0:8000</u></font> <b>(</b>Press CTRL+C to
             quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started parent process <b>[</b><font color="#34E2E2"><b>27365</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27368</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27369</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27370</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>27367</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

////

//// tab | `uvicorn`

`uvicorn` komutunu doğrudan kullanmayı tercih ederseniz:

<div class="termy">

```console
$ uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
<font color="#A6E22E">INFO</font>:     Uvicorn running on <b>http://0.0.0.0:8080</b> (Press CTRL+C to quit)
<font color="#A6E22E">INFO</font>:     Started parent process [<font color="#A1EFE4"><b>27365</b></font>]
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27368</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27369</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27370</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
<font color="#A6E22E">INFO</font>:     Started server process [<font color="#A1EFE4">27367</font>]
<font color="#A6E22E">INFO</font>:     Waiting for application startup.
<font color="#A6E22E">INFO</font>:     Application startup complete.
```

</div>

////

Buradaki tek yeni seçenek `--workers`; bu seçenek Uvicorn'a 4 adet worker process başlatmasını söyler.

Ayrıca her process'in **PID**'inin gösterildiğini de görebilirsiniz: parent process için `27365` (bu **process manager**), her worker process için de bir PID: `27368`, `27369`, `27370` ve `27367`.

## Deployment Kavramları { #deployment-concepts }

Burada, uygulamanın çalışmasını **paralelleştirmek**, CPU'daki **çok çekirdekten** yararlanmak ve **daha fazla request** karşılayabilmek için birden fazla **worker**'ı nasıl kullanacağınızı gördünüz.

Yukarıdaki deployment kavramları listesinden, worker kullanımı ağırlıklı olarak **replikasyon** kısmına yardımcı olur, ayrıca **yeniden başlatmalar** konusunda da az da olsa katkı sağlar. Ancak diğerlerini yine sizin yönetmeniz gerekir:

* **Güvenlik - HTTPS**
* **Başlangıçta çalıştırma**
* ***Yeniden başlatmalar***
* Replikasyon (çalışan process sayısı)
* **Bellek**
* **Başlatmadan önceki adımlar**

## Container'lar ve Docker { #containers-and-docker }

Bir sonraki bölümde, [Container'larda FastAPI - Docker](docker.md){.internal-link target=_blank} üzerinden diğer **deployment kavramlarını** ele almak için kullanabileceğiniz bazı stratejileri anlatacağım.

Tek bir Uvicorn process çalıştıracak şekilde **sıfırdan kendi image'ınızı oluşturmayı** göstereceğim. Bu oldukça basit bir süreçtir ve **Kubernetes** gibi dağıtık bir container yönetim sistemi kullanırken büyük olasılıkla yapmak isteyeceğiniz şey de budur.

## Özet { #recap }

**Çok çekirdekli CPU**'lardan faydalanmak ve **birden fazla process'i paralel** çalıştırmak için `fastapi` veya `uvicorn` komutlarıyla `--workers` CLI seçeneğini kullanarak birden fazla worker process çalıştırabilirsiniz.

Diğer deployment kavramlarını da kendiniz ele alarak **kendi deployment sisteminizi** kuruyorsanız, bu araçları ve fikirleri kullanabilirsiniz.

Container'larla (örn. Docker ve Kubernetes) **FastAPI**'yi öğrenmek için bir sonraki bölüme göz atın. Bu araçların, diğer **deployment kavramlarını** çözmek için de basit yöntemleri olduğunu göreceksiniz. ✨
