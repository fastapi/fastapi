# Mevcut Kullanıcıyı Alma { #get-current-user }

Önceki bölümde güvenlik sistemi (dependency injection sistemine dayanır) *path operation function*'a `str` olarak bir `token` veriyordu:

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

Ancak bu hâlâ pek kullanışlı değil.

Bize mevcut kullanıcıyı verecek şekilde düzenleyelim.

## Bir kullanıcı modeli oluşturun { #create-a-user-model }

Önce bir Pydantic kullanıcı modeli oluşturalım.

Body'leri bildirmek için Pydantic'i nasıl kullanıyorsak, aynı şekilde onu başka her yerde de kullanabiliriz:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## `get_current_user` dependency'si oluşturun { #create-a-get-current-user-dependency }

Bir `get_current_user` dependency'si oluşturalım.

Dependency'lerin alt dependency'leri olabileceğini hatırlıyor musunuz?

`get_current_user`, daha önce oluşturduğumuz `oauth2_scheme` ile aynı dependency'yi kullanacak.

Daha önce *path operation* içinde doğrudan yaptığımız gibi, yeni dependency'miz `get_current_user`, alt dependency olan `oauth2_scheme` üzerinden `str` olarak bir `token` alacak:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## Kullanıcıyı alın { #get-the-user }

`get_current_user`, oluşturduğumuz (sahte) bir yardımcı (utility) fonksiyonu kullanacak; bu fonksiyon `str` olarak bir token alır ve Pydantic `User` modelimizi döndürür:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## Mevcut kullanıcıyı enjekte edin { #inject-the-current-user }

Artık *path operation* içinde `get_current_user` ile aynı `Depends` yaklaşımını kullanabiliriz:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

`current_user` tipini Pydantic `User` modeli olarak belirttiğimize dikkat edin.

Bu sayede fonksiyonun içinde otomatik tamamlama ve tip kontrollerinin tamamından faydalanırız.

/// tip | İpucu

Request body'lerinin de Pydantic modelleri ile bildirildiğini hatırlıyor olabilirsiniz.

Burada `Depends` kullandığınız için **FastAPI** karışıklık yaşamaz.

///

/// check | Ek bilgi

Bu dependency sisteminin tasarımı, hepsi `User` modeli döndüren farklı dependency'lere (farklı "dependable"lara) sahip olmamıza izin verir.

Bu tipte veri döndürebilen yalnızca tek bir dependency ile sınırlı değiliz.

///

## Diğer modeller { #other-models }

Artık *path operation function* içinde mevcut kullanıcıyı doğrudan alabilir ve güvenlik mekanizmalarını `Depends` kullanarak **Dependency Injection** seviyesinde yönetebilirsiniz.

Ayrıca güvenlik gereksinimleri için herhangi bir model veya veri kullanabilirsiniz (bu örnekte bir Pydantic `User` modeli).

Ancak belirli bir data model, class ya da type kullanmak zorunda değilsiniz.

Modelinizde bir `id` ve `email` olsun, ama `username` olmasın mı istiyorsunuz? Elbette. Aynı araçları kullanabilirsiniz.

Sadece bir `str` mı istiyorsunuz? Ya da sadece bir `dict`? Veya doğrudan bir veritabanı class model instance'ı? Hepsi aynı şekilde çalışır.

Uygulamanıza giriş yapan kullanıcılar yok da robotlar, botlar veya yalnızca bir access token'a sahip başka sistemler mi var? Yine, her şey aynı şekilde çalışır.

Uygulamanız için neye ihtiyacınız varsa o türden bir model, class ve veritabanı kullanın. **FastAPI**, dependency injection sistemiyle bunları destekler.

## Kod boyutu { #code-size }

Bu örnek biraz uzun görünebilir. Güvenlik, data model'ler, utility fonksiyonlar ve *path operation*'ları aynı dosyada bir araya getirdiğimizi unutmayın.

Ama kritik nokta şu:

Güvenlik ve dependency injection tarafını bir kez yazarsınız.

İstediğiniz kadar karmaşık hâle getirebilirsiniz. Yine de hepsi tek bir yerde ve sadece bir kez yazılmış olur. Üstelik tüm esneklikle.

Sonrasında aynı güvenlik sistemini kullanan binlerce endpoint (*path operation*) olabilir.

Ve bunların hepsi (ya da istediğiniz bir kısmı) bu dependency'leri veya oluşturacağınız başka dependency'leri yeniden kullanmaktan faydalanabilir.

Hatta bu binlerce *path operation* 3 satır kadar kısa olabilir:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## Özet { #recap }

Artık *path operation function* içinde mevcut kullanıcıyı doğrudan alabilirsiniz.

Yolun yarısına geldik.

Kullanıcının/istemcinin gerçekten `username` ve `password` göndermesini sağlayacak bir *path operation* eklememiz gerekiyor.

Sırada bu var.
