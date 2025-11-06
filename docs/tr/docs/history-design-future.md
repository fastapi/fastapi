# Geçmişi, Tasarımı ve Geleceği

Bir süre önce, <a href="https://github.com/fastapi/fastapi/issues/3#issuecomment-454956920" class="external-link" target="_blank">bir **FastAPI** kullanıcısı sordu</a>:

> Bu projenin geçmişi nedir? Birkaç hafta içinde hiçbir yerden harika bir şeye dönüşmüş gibi görünüyor [...]

İşte o geçmişin bir kısmı.

## Alternatifler

Bir süredir karmaşık gereksinimlere sahip API'lar oluşturuyor (Makine Öğrenimi, dağıtık sistemler, asenkron işler, NoSQL veritabanları vb.) ve farklı geliştirici ekiplerini yönetiyorum.

Bu süreçte birçok alternatifi araştırmak, test etmek ve kullanmak zorunda kaldım.

**FastAPI**'ın geçmişi, büyük ölçüde önceden geliştirilen araçların geçmişini kapsıyor.

[Alternatifler](alternatives.md){.internal-link target=_blank} bölümünde belirtildiği gibi:

<blockquote markdown="1">

Başkalarının daha önceki çalışmaları olmasaydı, **FastAPI** var olmazdı.

Geçmişte oluşturulan pek çok araç **FastAPI**'a ilham kaynağı olmuştur.

Yıllardır yeni bir framework oluşturmaktan kaçınıyordum. Başlangıçta **FastAPI**'ın çözdüğü sorunları çözebilmek için pek çok farklı framework, <abbr title="Eklenti: Plug-In">eklenti</abbr> ve araç kullanmayı denedim.

Ancak bir noktada, geçmişteki diğer araçlardan en iyi fikirleri alarak bütün bu çözümleri kapsayan, ayrıca bütün bunları Python'ın daha önce mevcut olmayan özelliklerini (Python 3.6+ ile gelen <abbr title="Tip belirteçleri: Type Hints">tip belirteçleri</abbr>) kullanarak yapan bir şey üretmekten başka bir seçenek kalmamıştı.

</blockquote>

## Araştırma

Önceki alternatifleri kullanarak hepsinden bir şeyler öğrenip, fikirler alıp, bunları kendim ve çalıştığım geliştirici ekipler için en iyi şekilde birleştirebilme şansım oldu.

Mesela, ideal olarak standart Python tip belirteçlerine dayanması gerektiği açıktı.

Ayrıca, en iyi yaklaşım zaten mevcut olan standartları kullanmaktı.

Sonuç olarak, **FastAPI**'ı kodlamaya başlamadan önce, birkaç ay boyunca OpenAPI, JSON Schema, OAuth2 ve benzerlerinin tanımlamalarını inceledim. İlişkilerini, örtüştükleri noktaları ve farklılıklarını anlamaya çalıştım.

## Tasarım

Sonrasında, (**FastAPI** kullanan bir geliştirici olarak) sahip olmak istediğim "API"ı tasarlamak için biraz zaman harcadım.

Çeşitli fikirleri en popüler Python editörlerinde test ettim: PyCharm, VS Code, Jedi tabanlı editörler.

Bu test, en son <a href="https://www.jetbrains.com/research/python-developers-survey-2018/#development-tools" class="external-link" target="_blank">Python Developer Survey</a>'ine göre, kullanıcıların yaklaşık %80'inin kullandığı editörleri kapsıyor.

Bu da demek oluyor ki **FastAPI**, Python geliştiricilerinin %80'inin kullandığı editörlerle test edildi. Ve diğer editörlerin çoğu benzer şekilde çalıştığından, avantajları neredeyse tüm editörlerde çalışacaktır.

Bu şekilde, kod tekrarını mümkün olduğunca azaltmak, her yerde <abbr title="Otomatik Tamamlama: auto-complete, autocompletion, IntelliSense">otomatik tamamlama</abbr>, tip ve hata kontrollerine sahip olmak için en iyi yolları bulabildim.

Hepsi, tüm geliştiriciler için en iyi geliştirme deneyimini sağlayacak şekilde.

## Gereksinimler

Çeşitli alternatifleri test ettikten sonra, avantajlarından dolayı <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">**Pydantic**</a>'i kullanmaya karar verdim.

Sonra, JSON Schema ile tamamen uyumlu olmasını sağlamak, kısıtlama bildirimlerini tanımlamanın farklı yollarını desteklemek ve birkaç editördeki testlere dayanarak editör desteğini (tip kontrolleri, otomatik tamamlama) geliştirmek için katkıda bulundum.

Geliştirme sırasında, diğer ana gereksinim olan <a href="https://www.starlette.dev/" class="external-link" target="_blank">**Starlette**</a>'e de katkıda bulundum.

## Geliştirme

**FastAPI**'ı oluşturmaya başladığımda, parçaların çoğu zaten yerindeydi, tasarım tanımlanmıştı, gereksinimler ve araçlar hazırdı, standartlar ve tanımlamalar hakkındaki bilgi net ve tazeydi.

## Gelecek

Şimdiye kadar, **FastAPI**'ın fikirleriyle birçok kişiye faydalı olduğu apaçık ortada.

Birçok kullanım durumuna daha iyi uyduğu için, önceki alternatiflerin yerine seçiliyor.

Ben ve ekibim dahil, birçok geliştirici ve ekip projelerinde **FastAPI**'ya bağlı.

Tabi, geliştirilecek birçok özellik ve iyileştirme mevcut.

**FastAPI**'ın önünde harika bir gelecek var.

[Yardımlarınız](help-fastapi.md){.internal-link target=_blank} çok değerlidir.
