# Eğitim - Kullanıcı Rehberi { #tutorial-user-guide }

Bu eğitim, **FastAPI**'yi özelliklerinin çoğuyla birlikte adım adım nasıl kullanacağınızı gösterir.

Her bölüm bir öncekilerin üzerine kademeli olarak eklenir, ancak konular birbirinden ayrılacak şekilde yapılandırılmıştır; böylece API ihtiyaçlarınıza göre doğrudan belirli bir konuya gidip aradığınızı bulabilirsiniz.

Ayrıca, ileride tekrar dönüp tam olarak ihtiyaç duyduğunuz şeyi görebileceğiniz bir referans olarak da tasarlanmıştır.

## Kodu Çalıştırın { #run-the-code }

Tüm code block'lar kopyalanıp doğrudan kullanılabilir (zaten test edilmiş Python dosyalarıdır).

Örneklerden herhangi birini çalıştırmak için, kodu `main.py` adlı bir dosyaya kopyalayın ve `uv run` ile `fastapi dev`'i başlatın:

<div class="termy">

```console
$ <font color="#4E9A06">uv run fastapi</font> dev

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

Kodu yazmanız ya da kopyalayıp düzenlemeniz ve yerelinizde çalıştırmanız **şiddetle önerilir**.

Editörünüzde kullanmak FastAPI'nin avantajlarını gerçekten gösterir: ne kadar az kod yazmanız gerektiğini, type check'leri, autocompletion'ı vb. görürsünüz.

---

## FastAPI'yi Kurun { #install-fastapi }

İlk adım projenizi hazırlamak ve FastAPI'yi eklemektir.

[`uv`](https://docs.astral.sh/uv/getting-started/installation/)'yi kurun, ardından bir proje oluşturup FastAPI'yi ekleyin:

<div class="termy">

```console
$ uv init awesome-project --bare
$ cd awesome-project
$ uv add "fastapi[standard]"

---> 100%
```

</div>

`uv add`, projenin sanal ortamını `.venv` içinde oluşturur, FastAPI'yi `pyproject.toml` dosyasına ekler ve aynı paket sürümlerinin daha sonra kurulabilmesi için `uv.lock` oluşturur.

/// details | Bu komutlar ne yapar

* `uv init`: yeni bir Python projesi oluşturur.
* `awesome-project`: projeyi bu adla yeni bir dizinde oluşturur.
* `--bare`: örnek bir `main.py`, `README.md` veya başka dosyalar oluşturmadan yalnızca en minimal `pyproject.toml` dosyasını oluşturur. Bu eğitimin sonraki adımlarında uygulama dosyalarını kendiniz oluşturacaksınız.

Ardından `cd awesome-project`, FastAPI eklenmeden önce yeni proje dizinine girer.

`uv`, sisteminizde zaten kurulu olan uyumlu bir Python sürümünü kullanır veya gerekirse bir tane indirir.

`uv add` çalıştırdığınızda, FastAPI'nin ve FastAPI'nin bağlı olduğu tüm paketlerin uyumlu sürümlerini seçer. Kesin sürümleri `uv.lock` içine kaydeder; bu da aynı paket sürümlerini daha sonra başka bir bilgisayarda veya uygulamayı deploy ederken kurmayı mümkün kılar.

Bu dosyayı oluşturmak veya güncellemek, proje bağımlılıklarını [**lock'lamak**](https://docs.astral.sh/uv/concepts/projects/sync/) olarak adlandırılır. `uv`, bir paket eklediğinizde bunu otomatik olarak yapar.

///

/// details | FastAPI kurulum seçenekleri

`uv add "fastapi[standard]"` ile kurduğunuzda, bazı varsayılan opsiyonel standart bağımlılıklarla birlikte gelir. Bunlara `fastapi-cloud-cli` da dahildir; bu sayede [FastAPI Cloud](https://fastapicloud.com)'a deploy edebilirsiniz.

Bu opsiyonel bağımlılıkları istemiyorsanız bunun yerine `uv add fastapi` kurabilirsiniz.

Standart bağımlılıkları kurmak istiyor ama `fastapi-cloud-cli` olmasın diyorsanız, `uv add "fastapi[standard-no-fastapi-cloud-cli]"` ile kurabilirsiniz.

///

/// details | Bunun yerine `pip` kullanmak

Bir sanal ortamı ve paketleri manuel yönetmeyi tercih ediyorsanız, bir sanal ortam oluşturup etkinleştirin ve ardından FastAPI'yi `pip install "fastapi[standard]"` ile kurun.

Ayrıntılı adımlar için [Sanal Ortamlar rehberini](https://tiangolo.com/guides/virtual-environments/) okuyun.

///

## AI Agent Skill'leri { #ai-agent-skills }

FastAPI, AI kodlama agent'ları için resmi bir skill içerir. Paketle birlikte gelir; bu nedenle yönergeleri projenizde kurulu FastAPI sürümüyle uyumlu kalır ve FastAPI'yi güncellediğinizde güncellenir.

Projenize FastAPI'yi kurduktan sonra, skill'i <a href="https://library-skills.io">Library Skills</a> ile kurabilirsiniz:

```bash
uvx library-skills
```

/// note | Not

`uvx`, `uv tool run` için bir alias'tır. Library Skills projenizde kurulu paketleri tararken, Library Skills'i geçici ve izole bir ortamda çalıştırır.

///

Skill; Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, Pi, OpenCode ve diğer çoğu kodlama agent'ı ile uyumludur. Claude Code için, skill'in nereye kurulacağı sorulduğunda `.claude/skills` seçeneğini seçin.

## İleri Düzey Kullanıcı Rehberi { #advanced-user-guide }

Bu **Eğitim - Kullanıcı Rehberi**'ni bitirdikten sonra daha sonra okuyabileceğiniz bir **İleri Düzey Kullanıcı Rehberi** de var.

**İleri Düzey Kullanıcı Rehberi** bunun üzerine inşa eder, aynı kavramları kullanır ve size bazı ek özellikler öğretir.

Ancak önce **Eğitim - Kullanıcı Rehberi**'ni (şu anda okuduğunuz bölümü) okumalısınız.

Yalnızca **Eğitim - Kullanıcı Rehberi** ile eksiksiz bir uygulama oluşturabilmeniz hedeflenmiştir; ardından ihtiyaçlarınıza göre, **İleri Düzey Kullanıcı Rehberi**'ndeki ek fikirlerden bazılarını kullanarak farklı şekillerde genişletebilirsiniz.
