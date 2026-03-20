# SDK Üretme { #generating-sdks }

**FastAPI**, **OpenAPI** spesifikasyonunu temel aldığı için API'leri birçok aracın anlayabildiği standart bir formatta tanımlanabilir.

Bu sayede güncel **dokümantasyon**, birden fazla dilde istemci kütüphaneleri (<abbr title="Software Development Kits - Yazılım Geliştirme Kitleri">**SDKs**</abbr>) ve kodunuzla senkron kalan **test** veya **otomasyon iş akışları** üretmek kolaylaşır.

Bu rehberde, FastAPI backend'iniz için bir **TypeScript SDK** üretmeyi öğreneceksiniz.

## Açık Kaynak SDK Üreteçleri { #open-source-sdk-generators }

Esnek bir seçenek olan [OpenAPI Generator](https://openapi-generator.tech/), **birçok programlama dilini** destekler ve OpenAPI spesifikasyonunuzdan SDK üretebilir.

**TypeScript client**'lar için [Hey API](https://heyapi.dev/), TypeScript ekosistemi için özel olarak tasarlanmış, optimize bir deneyim sunan bir çözümdür.

Daha fazla SDK üretecini [OpenAPI.Tools](https://openapi.tools/#sdk) üzerinde keşfedebilirsiniz.

/// tip | İpucu

FastAPI otomatik olarak **OpenAPI 3.1** spesifikasyonları üretir; bu yüzden kullanacağınız aracın bu sürümü desteklemesi gerekir.

///

## FastAPI Sponsorlarından SDK Üreteçleri { #sdk-generators-from-fastapi-sponsors }

Bu bölüm, FastAPI'yi sponsorlayan şirketlerin sunduğu **yatırım destekli** ve **şirket destekli** çözümleri öne çıkarır. Bu ürünler, yüksek kaliteli üretilen SDK'ların üzerine **ek özellikler** ve **entegrasyonlar** sağlar.

✨ [**FastAPI'ye sponsor olarak**](../help-fastapi.md#sponsor-the-author) ✨ bu şirketler, framework'ün ve **ekosisteminin** sağlıklı ve **sürdürülebilir** kalmasına yardımcı olur.

Sponsor olmaları aynı zamanda FastAPI **topluluğuna** (size) güçlü bir bağlılığı da gösterir; yalnızca **iyi bir hizmet** sunmayı değil, aynı zamanda **güçlü ve gelişen bir framework** olan FastAPI'yi desteklemeyi de önemsediklerini gösterir. 🙇

Örneğin şunları deneyebilirsiniz:

* [Speakeasy](https://speakeasy.com/editor?utm_source=fastapi+repo&utm_medium=github+sponsorship)
* [Stainless](https://www.stainless.com/?utm_source=fastapi&utm_medium=referral)
* [liblab](https://developers.liblab.com/tutorials/sdk-for-fastapi?utm_source=fastapi)

Bu çözümlerin bazıları açık kaynak olabilir veya ücretsiz katman sunabilir; yani finansal bir taahhüt olmadan deneyebilirsiniz. Başka ticari SDK üreteçleri de vardır ve internette bulunabilir. 🤓

## TypeScript SDK Oluşturma { #create-a-typescript-sdk }

Basit bir FastAPI uygulamasıyla başlayalım:

{* ../../docs_src/generate_clients/tutorial001_py310.py hl[7:9,12:13,16:17,21] *}

*Path operation*'ların, request payload ve response payload için kullandıkları modelleri `Item` ve `ResponseMessage` modelleriyle tanımladıklarına dikkat edin.

### API Dokümanları { #api-docs }

`/docs` adresine giderseniz, request'lerde gönderilecek ve response'larda alınacak veriler için **schema**'ları içerdiğini görürsünüz:

<img src="/img/tutorial/generate-clients/image01.png">

Bu schema'ları görebilirsiniz, çünkü uygulamada modellerle birlikte tanımlandılar.

Bu bilgi uygulamanın **OpenAPI schema**'sında bulunur ve sonrasında API dokümanlarında gösterilir.

OpenAPI'ye dahil edilen, modellerden gelen bu bilginin aynısı **client code üretmek** için kullanılabilir.

### Hey API { #hey-api }

Modelleri olan bir FastAPI uygulamamız olduğunda, Hey API ile bir TypeScript client üretebiliriz. Bunu yapmanın en hızlı yolu npx kullanmaktır.

```sh
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o src/client
```

Bu komut `./src/client` içine bir TypeScript SDK üretecektir.

Web sitelerinde [`@hey-api/openapi-ts` kurulumunu](https://heyapi.dev/openapi-ts/get-started) öğrenebilir ve [üretilen çıktıyı](https://heyapi.dev/openapi-ts/output) inceleyebilirsiniz.

### SDK'yı Kullanma { #using-the-sdk }

Artık client code'u import edip kullanabilirsiniz. Şuna benzer görünebilir; method'lar için otomatik tamamlama aldığınıza dikkat edin:

<img src="/img/tutorial/generate-clients/image02.png">

Ayrıca gönderilecek payload için de otomatik tamamlama alırsınız:

<img src="/img/tutorial/generate-clients/image03.png">

/// tip | İpucu

`name` ve `price` için otomatik tamamlamaya dikkat edin; bunlar FastAPI uygulamasında, `Item` modelinde tanımlanmıştı.

///

Gönderdiğiniz veriler için satır içi hatalar (inline errors) da alırsınız:

<img src="/img/tutorial/generate-clients/image04.png">

Response objesi de otomatik tamamlama sunacaktır:

<img src="/img/tutorial/generate-clients/image05.png">

## Tag'lerle FastAPI Uygulaması { #fastapi-app-with-tags }

Birçok durumda FastAPI uygulamanız daha büyük olacaktır ve farklı *path operation* gruplarını ayırmak için muhtemelen tag'leri kullanacaksınız.

Örneğin **items** için bir bölüm, **users** için başka bir bölüm olabilir ve bunları tag'lerle ayırabilirsiniz:

{* ../../docs_src/generate_clients/tutorial002_py310.py hl[21,26,34] *}

### Tag'lerle TypeScript Client Üretme { #generate-a-typescript-client-with-tags }

Tag'leri kullanan bir FastAPI uygulaması için client ürettiğinizde, genelde client code da tag'lere göre ayrılır.

Bu sayede client code tarafında her şey doğru şekilde sıralanır ve gruplandırılır:

<img src="/img/tutorial/generate-clients/image06.png">

Bu örnekte şunlar var:

* `ItemsService`
* `UsersService`

### Client Method İsimleri { #client-method-names }

Şu an üretilen `createItemItemsPost` gibi method isimleri çok temiz görünmüyor:

```TypeScript
ItemsService.createItemItemsPost({name: "Plumbus", price: 5})
```

...çünkü client üreteci, her *path operation* için OpenAPI'nin dahili **operation ID** değerini kullanır.

OpenAPI, her operation ID'nin tüm *path operation*'lar arasında benzersiz olmasını ister. Bu yüzden FastAPI; operation ID'yi benzersiz tutabilmek için **function adı**, **path** ve **HTTP method/operation** bilgilerini birleştirerek üretir.

Ancak bunu bir sonraki adımda nasıl iyileştirebileceğinizi göstereceğim. 🤓

## Özel Operation ID'ler ve Daha İyi Method İsimleri { #custom-operation-ids-and-better-method-names }

Bu operation ID'lerin **üretilme** şeklini **değiştirerek**, client'larda daha basit **method isimleri** elde edebilirsiniz.

Bu durumda, her operation ID'nin **benzersiz** olduğundan başka bir şekilde emin olmanız gerekir.

Örneğin, her *path operation*'ın bir tag'i olmasını sağlayabilir ve operation ID'yi **tag** ve *path operation* **adı**na (function adı) göre üretebilirsiniz.

### Benzersiz ID Üreten Özel Fonksiyon { #custom-generate-unique-id-function }

FastAPI, her *path operation* için bir **unique ID** kullanır. Bu ID, **operation ID** için ve ayrıca request/response'lar için gerekebilecek özel model isimleri için de kullanılır.

Bu fonksiyonu özelleştirebilirsiniz. Bir `APIRoute` alır ve string döndürür.

Örneğin burada ilk tag'i (muhtemelen tek tag'iniz olur) ve *path operation* adını (function adı) kullanıyor.

Sonrasında bu özel fonksiyonu `generate_unique_id_function` parametresiyle **FastAPI**'ye geçebilirsiniz:

{* ../../docs_src/generate_clients/tutorial003_py310.py hl[6:7,10] *}

### Özel Operation ID'lerle TypeScript Client Üretme { #generate-a-typescript-client-with-custom-operation-ids }

Artık client'ı tekrar üretirseniz, geliştirilmiş method isimlerini göreceksiniz:

<img src="/img/tutorial/generate-clients/image07.png">

Gördüğünüz gibi method isimleri artık önce tag'i, sonra function adını içeriyor; URL path'i ve HTTP operation bilgisini artık taşımıyor.

### Client Üretecine Vermeden Önce OpenAPI Spesifikasyonunu Ön İşlemek { #preprocess-the-openapi-specification-for-the-client-generator }

Üretilen kodda hâlâ bazı **tekrarlanan bilgiler** var.

Bu method'un **items** ile ilişkili olduğunu zaten biliyoruz; çünkü bu kelime `ItemsService` içinde var (tag'den geliyor). Ama method adında da tag adı önek olarak duruyor. 😕

OpenAPI genelinde muhtemelen bunu korumak isteriz; çünkü operation ID'lerin **benzersiz** olmasını sağlar.

Ancak üretilen client için, client'ları üretmeden hemen önce OpenAPI operation ID'lerini **değiştirip**, method isimlerini daha hoş ve **temiz** hale getirebiliriz.

OpenAPI JSON'u `openapi.json` diye bir dosyaya indirip, şu tarz bir script ile **öndeki tag'i kaldırabiliriz**:

{* ../../docs_src/generate_clients/tutorial004_py310.py *}

//// tab | Node.js

```Javascript
{!> ../../docs_src/generate_clients/tutorial004.js!}
```

////

Bununla operation ID'ler `items-get_items` gibi değerlerden sadece `get_items` olacak şekilde yeniden adlandırılır; böylece client üreteci daha basit method isimleri üretebilir.

### Ön İşlenmiş OpenAPI ile TypeScript Client Üretme { #generate-a-typescript-client-with-the-preprocessed-openapi }

Sonuç artık bir `openapi.json` dosyasında olduğuna göre, input konumunu güncellemeniz gerekir:

```sh
npx @hey-api/openapi-ts -i ./openapi.json -o src/client
```

Yeni client'ı ürettikten sonra, tüm **otomatik tamamlama**, **satır içi hatalar**, vb. ile birlikte **temiz method isimleri** elde edersiniz:

<img src="/img/tutorial/generate-clients/image08.png">

## Faydalar { #benefits }

Otomatik üretilen client'ları kullanınca şu alanlarda **otomatik tamamlama** elde edersiniz:

* Method'lar.
* Body'deki request payload'ları, query parametreleri, vb.
* Response payload'ları.

Ayrıca her şey için **satır içi hatalar** (inline errors) da olur.

Backend kodunu her güncellediğinizde ve frontend'i **yeniden ürettiğinizde**, yeni *path operation*'lar method olarak eklenir, eskileri kaldırılır ve diğer değişiklikler de üretilen koda yansır. 🤓

Bu, bir şey değiştiğinde client code'a otomatik olarak **yansıyacağı** anlamına gelir. Ayrıca client'ı **build** ettiğinizde, kullanılan verilerde bir **uyuşmazlık** (mismatch) varsa hata alırsınız.

Böylece üretimde son kullanıcılara hata yansımasını beklemek ve sonra sorunun nerede olduğunu debug etmeye çalışmak yerine, geliştirme sürecinin çok erken aşamalarında **birçok hatayı tespit edersiniz**. ✨
