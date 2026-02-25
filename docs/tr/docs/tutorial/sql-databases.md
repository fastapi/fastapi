# SQL (İlişkisel) Veritabanları { #sql-relational-databases }

**FastAPI**, SQL (ilişkisel) bir veritabanı kullanmanızı zorunlu kılmaz. Ancak isterseniz **istediğiniz herhangi bir veritabanını** kullanabilirsiniz.

Burada <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a> kullanarak bir örnek göreceğiz.

**SQLModel**, <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> ve Pydantic’in üzerine inşa edilmiştir. **FastAPI**’nin yazarı tarafından, **SQL veritabanları** kullanması gereken FastAPI uygulamalarıyla mükemmel uyum sağlaması için geliştirilmiştir.

/// tip | İpucu

İstediğiniz başka bir SQL veya NoSQL veritabanı kütüphanesini kullanabilirsiniz (bazı durumlarda <abbr title="Object Relational Mapper - Obje-İlişkisel Eşleyici: bazı sınıfların SQL tablolarını ve örneklerin bu tablolardaki satırları temsil ettiği bir kütüphane için süslü bir terim">"ORMs"</abbr> olarak adlandırılır). FastAPI sizi hiçbir şeye zorlamaz. 😎

///

SQLModel, SQLAlchemy tabanlı olduğu için SQLAlchemy’nin **desteklediği herhangi bir veritabanını** kolayca kullanabilirsiniz (bu da SQLModel tarafından da desteklendikleri anlamına gelir), örneğin:

* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, vb.

Bu örnekte **SQLite** kullanacağız; çünkü tek bir dosya kullanır ve Python’da yerleşik desteği vardır. Yani bu örneği kopyalayıp olduğu gibi çalıştırabilirsiniz.

Daha sonra, production uygulamanız için **PostgreSQL** gibi bir veritabanı sunucusu kullanmak isteyebilirsiniz.

/// tip | İpucu

Frontend ve daha fazla araçla birlikte **FastAPI** + **PostgreSQL** içeren resmi bir proje oluşturucu (project generator) var: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

Bu çok basit ve kısa bir eğitimdir. Veritabanları genelinde, SQL hakkında veya daha ileri özellikler hakkında öğrenmek isterseniz <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel dokümantasyonuna</a> gidin.

## `SQLModel` Kurulumu { #install-sqlmodel }

Önce [virtual environment](../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan emin olun, aktive edin ve ardından `sqlmodel`’i yükleyin:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Tek Model ile Uygulamayı Oluşturma { #create-the-app-with-a-single-model }

Önce, tek bir **SQLModel** modeliyle uygulamanın en basit ilk sürümünü oluşturacağız.

Aşağıda, **birden fazla model** kullanarak güvenliği ve esnekliği artırıp geliştireceğiz. 🤓

### Modelleri Oluşturma { #create-models }

`SQLModel`’i import edin ve bir veritabanı modeli oluşturun:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

`Hero` sınıfı, bir Pydantic modeline çok benzer (hatta altta aslında *bir Pydantic modelidir*).

Birkaç fark var:

* `table=True`, SQLModel’e bunun bir *table model* olduğunu söyler; SQL veritabanında bir **table**’ı temsil etmelidir, sadece bir *data model* değildir (diğer normal Pydantic sınıflarında olduğu gibi).

* `Field(primary_key=True)`, SQLModel’e `id`’nin SQL veritabanındaki **primary key** olduğunu söyler (SQL primary key’leri hakkında daha fazlasını SQLModel dokümantasyonunda öğrenebilirsiniz).

    **Not:** primary key alanı için `int | None` kullanıyoruz; böylece Python kodunda *`id` olmadan bir nesne oluşturabiliriz* (`id=None`) ve veritabanının *kaydederken bunu üreteceğini* varsayarız. SQLModel, veritabanının `id` sağlayacağını anlar ve *veritabanı şemasında sütunu null olamayan bir `INTEGER`* olarak tanımlar. Detaylar için <a href="https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#primary-key-id" class="external-link" target="_blank">primary key’ler hakkında SQLModel dokümantasyonuna</a> bakın.

* `Field(index=True)`, SQLModel’e bu sütun için bir **SQL index** oluşturmasını söyler; bu da bu sütuna göre filtrelenmiş verileri okurken veritabanında daha hızlı arama yapılmasını sağlar.

    SQLModel, `str` olarak tanımlanan bir şeyin SQL tarafında `TEXT` (veya veritabanına bağlı olarak `VARCHAR`) tipinde bir sütun olacağını bilir.

### Engine Oluşturma { #create-an-engine }

Bir SQLModel `engine`’i (altta aslında bir SQLAlchemy `engine`’idir) veritabanına olan **bağlantıları tutan** yapıdır.

Tüm kodunuzun aynı veritabanına bağlanması için **tek bir `engine` nesnesi** kullanırsınız.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

`check_same_thread=False` kullanmak, FastAPI’nin aynı SQLite veritabanını farklı thread’lerde kullanmasına izin verir. Bu gereklidir; çünkü **tek bir request** **birden fazla thread** kullanabilir (örneğin dependency’lerde).

Merak etmeyin; kodun yapısı gereği, ileride **her request için tek bir SQLModel *session*** kullandığımızdan emin olacağız. Zaten `check_same_thread` de temelde bunu mümkün kılmaya çalışır.

### Table’ları Oluşturma { #create-the-tables }

Sonra `SQLModel.metadata.create_all(engine)` kullanan bir fonksiyon ekleyerek tüm *table model*’ler için **table’ları oluştururuz**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Session Dependency’si Oluşturma { #create-a-session-dependency }

Bir **`Session`**, **nesneleri memory’de** tutar ve verideki gerekli değişiklikleri takip eder; ardından veritabanıyla iletişim kurmak için **`engine` kullanır**.

`yield` ile, her request için yeni bir `Session` sağlayacak bir FastAPI **dependency** oluşturacağız. Bu da her request’te tek session kullanmamızı garanti eder. 🤓

Ardından bu dependency’yi kullanacak kodun geri kalanını sadeleştirmek için `Annotated` ile `SessionDep` dependency’sini oluştururuz.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Startup’ta Veritabanı Table’larını Oluşturma { #create-database-tables-on-startup }

Uygulama başlarken veritabanı table’larını oluşturacağız.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Burada bir uygulama startup event’inde table’ları oluşturuyoruz.

Production’da büyük ihtimalle uygulamayı başlatmadan önce çalışan bir migration script’i kullanırsınız. 🤓

/// tip | İpucu

SQLModel, Alembic’i saran migration araçlarına sahip olacak; ancak şimdilik <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="_blank">Alembic</a>’i doğrudan kullanabilirsiniz.

///

### Hero Oluşturma { #create-a-hero }

Her SQLModel modeli aynı zamanda bir Pydantic modeli olduğu için, Pydantic modelleriyle kullanabildiğiniz **type annotation**’larda aynı şekilde kullanabilirsiniz.

Örneğin `Hero` tipinde bir parametre tanımlarsanız, bu parametre **JSON body**’den okunur.

Aynı şekilde, bunu fonksiyonun **return type**’ı olarak da tanımlayabilirsiniz; böylece verinin şekli otomatik API docs arayüzünde görünür.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Burada `SessionDep` dependency’sini (bir `Session`) kullanarak yeni `Hero`’yu `Session` instance’ına ekliyoruz, değişiklikleri veritabanına commit ediyoruz, `hero` içindeki veriyi refresh ediyoruz ve sonra geri döndürüyoruz.

### Hero’ları Okuma { #read-heroes }

`select()` kullanarak veritabanından `Hero`’ları **okuyabiliriz**. Sonuçları sayfalama (pagination) yapmak için `limit` ve `offset` ekleyebiliriz.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Tek Bir Hero Okuma { #read-one-hero }

Tek bir `Hero` **okuyabiliriz**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Hero Silme { #delete-a-hero }

Bir `Hero`’yu **silebiliriz**.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Uygulamayı Çalıştırma { #run-the-app }

Uygulamayı çalıştırabilirsiniz:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Sonra `/docs` arayüzüne gidin; **FastAPI**’nin API’yi **dokümante etmek** için bu **modelleri** kullandığını göreceksiniz. Ayrıca veriyi **serialize** ve **validate** etmek için de onları kullanacaktır.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Birden Fazla Model ile Uygulamayı Güncelleme { #update-the-app-with-multiple-models }

Şimdi bu uygulamayı biraz **refactor** edelim ve **güvenliği** ile **esnekliği** artıralım.

Önceki uygulamaya bakarsanız, UI’da şu ana kadar client’ın oluşturulacak `Hero`’nun `id` değerini belirlemesine izin verdiğini görebilirsiniz. 😱

Buna izin vermemeliyiz; DB’de zaten atanmış bir `id`’yi ezebilirler. `id` belirlemek **client** tarafından değil, **backend** veya **veritabanı** tarafından yapılmalıdır.

Ayrıca hero için bir `secret_name` oluşturuyoruz ama şimdiye kadar her yerde geri döndürüyoruz; bu pek de **secret** sayılmaz... 😅

Bunları birkaç **ek model** ekleyerek düzelteceğiz. SQLModel’in parlayacağı yer de burası. ✨

### Birden Fazla Model Oluşturma { #create-multiple-models }

**SQLModel**’de, `table=True` olan herhangi bir model sınıfı bir **table model**’dir.

`table=True` olmayan her model sınıfı ise bir **data model**’dir; bunlar aslında sadece Pydantic modelleridir (bazı küçük ek özelliklerle). 🤓

SQLModel ile **inheritance** kullanarak her durumda tüm alanları tekrar tekrar yazmaktan **kaçınabiliriz**.

#### `HeroBase` - temel sınıf { #herobase-the-base-class }

Önce tüm modeller tarafından **paylaşılan alanları** içeren bir `HeroBase` modeliyle başlayalım:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - *table model* { #hero-the-table-model }

Sonra gerçek *table model* olan `Hero`’yu, diğer modellerde her zaman bulunmayan **ek alanlarla** oluşturalım:

* `id`
* `secret_name`

`Hero`, `HeroBase`’ten miras aldığı için `HeroBase`’te tanımlanan alanlara da sahiptir. Dolayısıyla `Hero` için tüm alanlar:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - public *data model* { #heropublic-the-public-data-model }

Sonraki adımda `HeroPublic` modelini oluştururuz; bu model API client’larına **geri döndürülecek** modeldir.

`HeroBase` ile aynı alanlara sahiptir; dolayısıyla `secret_name` içermez.

Sonunda kahramanlarımızın kimliği korunmuş oldu! 🥷

Ayrıca `id: int` alanını yeniden tanımlar. Bunu yaparak API client’larıyla bir **contract** (sözleşme) oluşturmuş oluruz; böylece `id` alanının her zaman var olacağını ve `int` olacağını (asla `None` olmayacağını) bilirler.

/// tip | İpucu

Return model’in bir değerin her zaman mevcut olduğunu ve her zaman `int` olduğunu (`None` değil) garanti etmesi API client’ları için çok faydalıdır; bu kesinlik sayesinde daha basit kod yazabilirler.

Ayrıca **otomatik üretilen client**’ların arayüzleri de daha basit olur; böylece API’nizle çalışan geliştiriciler için süreç çok daha rahat olur. 😎

///

`HeroPublic` içindeki tüm alanlar `HeroBase` ile aynıdır; tek fark `id`’nin `int` olarak tanımlanmasıdır (`None` değil):

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - hero oluşturmak için *data model* { #herocreate-the-data-model-to-create-a-hero }

Şimdi `HeroCreate` modelini oluştururuz; bu model client’tan gelen veriyi **validate** etmek için kullanılır.

`HeroBase` ile aynı alanlara sahiptir ve ek olarak `secret_name` içerir.

Artık client’lar **yeni bir hero oluştururken** `secret_name` gönderecek; bu değer veritabanında saklanacak, ancak API response’larında client’a geri döndürülmeyecek.

/// tip | İpucu

**Password**’ları bu şekilde ele alırsınız: alırsınız ama API’de geri döndürmezsiniz.

Ayrıca password değerlerini saklamadan önce **hash** etmelisiniz; **asla plain text olarak saklamayın**.

///

`HeroCreate` alanları:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - hero güncellemek için *data model* { #heroupdate-the-data-model-to-update-a-hero }

Uygulamanın önceki sürümünde bir hero’yu **güncellemenin** bir yolu yoktu; ancak artık **birden fazla model** ile bunu yapabiliriz. 🎉

`HeroUpdate` *data model* biraz özeldir: yeni bir hero oluşturmak için gereken alanların **tamamına** sahiptir, ancak tüm alanlar **opsiyoneldir** (hepsinin bir default değeri vardır). Bu sayede hero güncellerken sadece güncellemek istediğiniz alanları gönderebilirsiniz.

Tüm **alanlar aslında değiştiği** için (tip artık `None` içeriyor ve default değerleri `None` oluyor), onları **yeniden tanımlamamız** gerekir.

Aslında `HeroBase`’ten miras almamız gerekmiyor; çünkü tüm alanları yeniden tanımlıyoruz. Tutarlılık için miras almayı bırakıyorum ama bu gerekli değil. Daha çok kişisel tercih meselesi. 🤷

`HeroUpdate` alanları:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### `HeroCreate` ile Oluşturma ve `HeroPublic` Döndürme { #create-with-herocreate-and-return-a-heropublic }

Artık **birden fazla model** olduğuna göre, onları kullanan uygulama kısımlarını güncelleyebiliriz.

Request’te bir `HeroCreate` *data model* alırız ve bundan bir `Hero` *table model* oluştururuz.

Bu yeni *table model* `Hero`, client’ın gönderdiği alanlara sahip olur ve ayrıca veritabanının ürettiği bir `id` alır.

Sonra fonksiyondan bu *table model* `Hero`’yu olduğu gibi döndürürüz. Ancak `response_model`’i `HeroPublic` *data model* olarak belirlediğimiz için **FastAPI**, veriyi validate ve serialize etmek için `HeroPublic` kullanır.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip | İpucu

Burada **return type annotation** `-> HeroPublic` yerine `response_model=HeroPublic` kullanıyoruz; çünkü gerçekte döndürdüğümüz değer *bir* `HeroPublic` değil.

Eğer `-> HeroPublic` yazsaydık, editörünüz ve linter’ınız (haklı olarak) `HeroPublic` yerine `Hero` döndürdüğünüz için şikayet edecekti.

Bunu `response_model` içinde belirterek **FastAPI**’ye işini yapmasını söylüyoruz; type annotation’lara ve editörünüzün/diğer araçların sağladığı desteğe karışmamış oluyoruz.

///

### `HeroPublic` ile Hero’ları Okuma { #read-heroes-with-heropublic }

Daha öncekiyle aynı şekilde `Hero`’ları **okuyabiliriz**; yine `response_model=list[HeroPublic]` kullanarak verinin doğru biçimde validate ve serialize edilmesini garanti ederiz.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65] *}

### `HeroPublic` ile Tek Bir Hero Okuma { #read-one-hero-with-heropublic }

Tek bir hero’yu **okuyabiliriz**:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### `HeroUpdate` ile Hero Güncelleme { #update-a-hero-with-heroupdate }

Bir hero’yu **güncelleyebiliriz**. Bunun için HTTP `PATCH` operasyonu kullanırız.

Kodda, client’ın gönderdiği tüm verilerle bir `dict` alırız; **yalnızca client’ın gönderdiği veriler**, yani sadece default değer oldukları için orada bulunan değerler hariç. Bunu yapmak için `exclude_unset=True` kullanırız. Asıl numara bu. 🪄

Sonra `hero_db.sqlmodel_update(hero_data)` ile `hero_db`’yi `hero_data` içindeki verilerle güncelleriz.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Hero’yu Tekrar Silme { #delete-a-hero-again }

Bir hero’yu **silmek** büyük ölçüde aynı kalıyor.

Bu örnekte her şeyi refactor etme isteğimizi bastıracağız. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Uygulamayı Tekrar Çalıştırma { #run-the-app-again }

Uygulamayı tekrar çalıştırabilirsiniz:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

`/docs` API UI’a giderseniz artık güncellendiğini göreceksiniz; hero oluştururken client’tan `id` beklemeyecek, vb.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Özet { #recap }

Bir SQL veritabanıyla etkileşim kurmak için <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">**SQLModel**</a> kullanabilir ve *data model* ile *table model* yaklaşımıyla kodu sadeleştirebilirsiniz.

**SQLModel** dokümantasyonunda çok daha fazlasını öğrenebilirsiniz; **FastAPI** ile SQLModel kullanımı için daha uzun bir mini <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="_blank">tutorial</a> da bulunuyor. 🚀
