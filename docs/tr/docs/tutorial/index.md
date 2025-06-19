# Rehber - Kullanıcı Kılavuzu

Bu rehber, **FastAPI** birçok özelliğini adım adım nasıl kullanacağınızı gösteriyor.

Her bölüm kademeli olarak bir öncekinin üzerine inşa edilir, ancak ayrı konulara göre yapılandırılmıştır, böylece belirli API ihtiyaçlarınızı çözmek için doğrudan belirli bir bölüme gidebilirsiniz.

Ayrıca gelecekte referans olarak kullanılmak üzere tasarlanmıştır.

Böylece geri gelebilir ve tam olarak neye ihtiyacınız olduğunu görebilirsiniz.

## Kodu çalıştır

Tüm kod blokları kopyalanabilir ve doğrudan kullanılabilir (bunlar aslında test edilmiş Python dosyalarıdır).

Örneklerden herhangi birini çalıştırmak için kodu `main.py` dosyasına kopyalayın ve `fastapi dev` ile başlatın:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:single">main.py</u>
<font color="#3465A4">INFO    </font> Using path <font color="#3465A4">main.py</font>
<font color="#3465A4">INFO    </font> Resolved absolute path <font color="#75507B">/home/user/code/awesomeapp/</font><font color="#AD7FA8">main.py</font>
<font color="#3465A4">INFO    </font> Searching for package file structure from directories with <font color="#3465A4">__init__.py</font> files
<font color="#3465A4">INFO    </font> Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

 ╭─ <font color="#8AE234"><b>Python module file</b></font> ─╮
 │                      │
 │  🐍 main.py          │
 │                      │
 ╰──────────────────────╯

<font color="#3465A4">INFO    </font> Importing module <font color="#4E9A06">main</font>
<font color="#3465A4">INFO    </font> Found importable FastAPI app

 ╭─ <font color="#8AE234"><b>Importable FastAPI app</b></font> ─╮
 │                          │
 │  <span style="background-color:#272822"><font color="#FF4689">from</font></span><span style="background-color:#272822"><font color="#F8F8F2"> main </font></span><span style="background-color:#272822"><font color="#FF4689">import</font></span><span style="background-color:#272822"><font color="#F8F8F2"> app</font></span><span style="background-color:#272822">  </span>  │
 │                          │
 ╰──────────────────────────╯

<font color="#3465A4">INFO    </font> Using import string <font color="#8AE234"><b>main:app</b></font>

 <span style="background-color:#C4A000"><font color="#2E3436">╭────────── FastAPI CLI - Development mode ───────────╮</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Serving at: http://127.0.0.1:8000                  │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  API docs: http://127.0.0.1:8000/docs               │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  Running in development mode, for production use:   │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│  </font></span><span style="background-color:#C4A000"><font color="#555753"><b>fastapi run</b></font></span><span style="background-color:#C4A000"><font color="#2E3436">                                        │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">│                                                     │</font></span>
 <span style="background-color:#C4A000"><font color="#2E3436">╰─────────────────────────────────────────────────────╯</font></span>

<font color="#4E9A06">INFO</font>:     Will watch for changes in these directories: [&apos;/home/user/code/awesomeapp&apos;]
<font color="#4E9A06">INFO</font>:     Uvicorn running on <b>http://127.0.0.1:8000</b> (Press CTRL+C to quit)
<font color="#4E9A06">INFO</font>:     Started reloader process [<font color="#34E2E2"><b>2265862</b></font>] using <font color="#34E2E2"><b>WatchFiles</b></font>
<font color="#4E9A06">INFO</font>:     Started server process [<font color="#06989A">2265873</font>]
<font color="#4E9A06">INFO</font>:     Waiting for application startup.
<font color="#4E9A06">INFO</font>:     Application startup complete.
</pre>
```

</div>

Kodu yazmanız veya kopyalamanız, düzenlemeniz ve yerel olarak çalıştırmanız **ŞİDDETLE** tavsiye edilir.

Editörünüzde kullanmak, FastAPI'ın faydalarını size gerçekten gösteren şeydir, ne kadar az kod yazmanız gerektiğini, tüm tip kontrollerini, otomatik tamamlamayı vb. görürsünüz.

---

## FastAPI'ı Yükleme

FastAPI'ı yüklemenin ilk adımı:

Kurulum yapmadan önce [sanal ortam](../virtual-environments.md){.internal-link target=_blank} oluşturun, etkinleştirin ve sonra **FastAPI yükleyin** :

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

!!! Not
`pip install "fastapi[standard]"` ile kurulum yaptığınızda, bazı varsayılan isteğe bağlı standart bağımlılıklarla birlikte gelir.

Bu isteğe bağlı bağımlılıklara sahip olmak istemiyorsanız, bunun yerine `pip install fastapi` ile yükleyebilirsiniz.

## Gelişmiş Kullanıcı Kılavuzu

Ayrıca, bu **Rehber - Kullanıcı Kılavuzu'ndan** sonra okuyabileceğiniz bir **Gelişmiş Kullanıcı Kılavuzu** da bulunmaktadır.

**Gelişmiş Kullanıcı Kılavuzu**, bunun üzerine inşa edilmiştir, aynı kavramları kullanır ve size bazı ekstra özellikler öğretir.

Ancak önce **Rehber - Kullanıcı Kılavuzu'nu** (şu anda okumakta olduğunuz) okumalısınız.

Bu doküman sadece **Rehber - Kullanıcı Kılavuzu** ile eksiksiz bir uygulama oluşturabileceğiniz ve daha sonra uygulamanızı **Gelişmiş Kullanıcı Kılavuzu'ndaki** bazı ek fikirleri kullanarak ve ihtiyaçlarınıza bağlı olarak farklı şekillerde genişletebileceğiniz şekilde tasarlanmıştır.
