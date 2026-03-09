# Password ile OAuth2 (ve hashing), JWT token'ları ile Bearer { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

Artık tüm security flow elimizde olduğuna göre, uygulamayı gerçekten güvenli hâle getirelim: <abbr title="JSON Web Tokens">JWT</abbr> token'ları ve güvenli password hashing kullanacağız.

Bu kodu uygulamanızda gerçekten kullanabilirsiniz; password hash'lerini veritabanınıza kaydedebilirsiniz, vb.

Bir önceki bölümde bıraktığımız yerden başlayıp üzerine ekleyerek ilerleyeceğiz.

## JWT Hakkında { #about-jwt }

JWT, "JSON Web Tokens" anlamına gelir.

Bir JSON nesnesini, boşluk içermeyen uzun ve yoğun bir string'e kodlamak için kullanılan bir standarttır. Şuna benzer:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Şifrelenmiş değildir; yani herkes içeriğindeki bilgiyi geri çıkarabilir.

Ancak imzalanmıştır. Bu yüzden, sizin ürettiğiniz bir token'ı aldığınızda, gerçekten onu sizin ürettiğinizi doğrulayabilirsiniz.

Bu şekilde, örneğin 1 haftalık süre sonu (expiration) olan bir token oluşturabilirsiniz. Sonra kullanıcı ertesi gün token ile geri geldiğinde, kullanıcının hâlâ sisteminizde oturum açmış olduğunu bilirsiniz.

Bir hafta sonra token'ın süresi dolar; kullanıcı yetkilendirilmez ve yeni bir token almak için tekrar giriş yapmak zorunda kalır. Ayrıca kullanıcı (veya üçüncü bir taraf) token'ı değiştirip süre sonunu farklı göstermek isterse bunu tespit edebilirsiniz; çünkü imzalar eşleşmez.

JWT token'larıyla oynayıp nasıl çalıştıklarını görmek isterseniz <a href="https://jwt.io/" class="external-link" target="_blank">https://jwt.io</a> adresine bakın.

## `PyJWT` Kurulumu { #install-pyjwt }

Python'da JWT token'larını üretmek ve doğrulamak için `PyJWT` kurmamız gerekiyor.

Bir [virtual environment](../../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan emin olun, aktif edin ve ardından `pyjwt` kurun:

<div class="termy">

```console
$ pip install pyjwt

---> 100%
```

</div>

/// info | Bilgi

RSA veya ECDSA gibi dijital imza algoritmaları kullanmayı planlıyorsanız, `pyjwt[crypto]` bağımlılığı olan `cryptography` kütüphanesini kurmalısınız.

Daha fazla bilgi için <a href="https://pyjwt.readthedocs.io/en/latest/installation.html" class="external-link" target="_blank">PyJWT Installation docs</a> sayfasını okuyabilirsiniz.

///

## Password hashing { #password-hashing }

"Hashing", bazı içerikleri (bu örnekte bir password) anlamsız görünen bir bayt dizisine (pratikte bir string) dönüştürmek demektir.

Aynı içeriği (aynı password'ü) her seferinde verirseniz, her seferinde aynı anlamsız çıktıyı elde edersiniz.

Ancak bu anlamsız çıktıdan geri password'e dönüştürme yapılamaz.

### Neden password hashing kullanılır { #why-use-password-hashing }

Veritabanınız çalınırsa, hırsız kullanıcılarınızın düz metin (plaintext) password'lerini değil, sadece hash'leri elde eder.

Dolayısıyla, o password'ü başka bir sistemde denemek kolay olmaz (pek çok kullanıcı her yerde aynı password'ü kullandığı için bu tehlikeli olurdu).

## `pwdlib` Kurulumu { #install-pwdlib }

pwdlib, password hash'leriyle çalışmak için çok iyi bir Python paketidir.

Birçok güvenli hashing algoritmasını ve bunlarla çalışmak için yardımcı araçları destekler.

Önerilen algoritma "Argon2"dir.

Bir [virtual environment](../../virtual-environments.md){.internal-link target=_blank} oluşturduğunuzdan emin olun, aktif edin ve sonra Argon2 ile birlikte pwdlib'i kurun:

<div class="termy">

```console
$ pip install "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | İpucu

`pwdlib` ile, **Django** tarafından oluşturulmuş password'leri, bir **Flask** security eklentisinin ürettiklerini veya başka birçok kaynaktan gelen password'leri okuyabilecek şekilde bile yapılandırabilirsiniz.

Böylece örneğin bir Django uygulamasındaki verileri aynı veritabanında bir FastAPI uygulamasıyla paylaşabilirsiniz. Ya da aynı veritabanını kullanarak bir Django uygulamasını kademeli şekilde taşıyabilirsiniz.

Ayrıca kullanıcılarınız, aynı anda hem Django uygulamanızdan hem de **FastAPI** uygulamanızdan login olabilir.

///

## Password'leri hash'leme ve doğrulama { #hash-and-verify-the-passwords }

Gerekli araçları `pwdlib` içinden import edelim.

Önerilen ayarlarla bir PasswordHash instance'ı oluşturalım; bunu password'leri hash'lemek ve doğrulamak için kullanacağız.

/// tip | İpucu

pwdlib, bcrypt hashing algoritmasını da destekler; ancak legacy algoritmaları içermez. Eski hash'lerle çalışmak için passlib kütüphanesini kullanmanız önerilir.

Örneğin, başka bir sistemin (Django gibi) ürettiği password'leri okuyup doğrulayabilir, ancak yeni password'leri Argon2 veya Bcrypt gibi farklı bir algoritmayla hash'leyebilirsiniz.

Ve aynı anda hepsiyle uyumlu kalabilirsiniz.

///

Kullanıcıdan gelen password'ü hash'lemek için bir yardımcı (utility) fonksiyon oluşturalım.

Sonra, alınan password'ün kayıttaki hash ile eşleşip eşleşmediğini doğrulayan başka bir yardımcı fonksiyon yazalım.

Bir tane de kullanıcıyı authenticate edip geri döndüren bir yardımcı fonksiyon ekleyelim.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

`authenticate_user`, veritabanında var olmayan bir username ile çağrıldığında, yine de sahte (dummy) bir hash'e karşı `verify_password` çalıştırıyoruz.

Bu, username geçerli olsun ya da olmasın endpoint'in yaklaşık aynı sürede yanıt vermesini sağlar; böylece mevcut username'leri saymaya yarayabilecek zamanlama saldırılarını (timing attacks) engeller.

/// note | Not

Yeni (sahte) veritabanı `fake_users_db`'ye bakarsanız, hash'lenmiş password'ün artık nasıl göründüğünü görebilirsiniz: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## JWT token'larını yönetme { #handle-jwt-tokens }

Kurulu modülleri import edelim.

JWT token'larını imzalamak için kullanılacak rastgele bir secret key oluşturalım.

Güvenli, rastgele bir secret key üretmek için şu komutu kullanın:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Çıktıyı `SECRET_KEY` değişkenine kopyalayın (örnektekini kullanmayın).

JWT token'ını imzalamak için kullanılan algoritmayı tutacak `ALGORITHM` adlı bir değişken oluşturup değerini `"HS256"` yapın.

Token'ın süre sonu (expiration) için bir değişken oluşturun.

Response için token endpoint'inde kullanılacak bir Pydantic Model tanımlayın.

Yeni bir access token üretmek için bir yardımcı fonksiyon oluşturun.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Dependency'leri güncelleme { #update-the-dependencies }

`get_current_user` fonksiyonunu, öncekiyle aynı token'ı alacak şekilde güncelleyelim; ancak bu sefer JWT token'larını kullanacağız.

Gelen token'ı decode edin, doğrulayın ve mevcut kullanıcıyı döndürün.

Token geçersizse, hemen bir HTTP hatası döndürün.

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## `/token` *path operation*'ını güncelleme { #update-the-token-path-operation }

Token'ın süre sonu için bir `timedelta` oluşturun.

Gerçek bir JWT access token üretip döndürün.

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### JWT "subject" `sub` Hakkında Teknik Detaylar { #technical-details-about-the-jwt-subject-sub }

JWT spesifikasyonu, token'ın konusu (subject) için `sub` adlı bir anahtar olduğunu söyler.

Bunu kullanmak zorunlu değildir; ancak kullanıcı kimliğini koymak için uygun yer burasıdır, bu yüzden burada onu kullanıyoruz.

JWT, sadece bir kullanıcıyı tanımlamak ve API'nizde doğrudan işlem yapmasına izin vermek dışında başka amaçlarla da kullanılabilir.

Örneğin bir "araba"yı veya bir "blog post"u tanımlayabilirsiniz.

Sonra o varlık için izinler ekleyebilirsiniz; örneğin (araba için) "drive" ya da (blog için) "edit".

Ardından bu JWT token'ını bir kullanıcıya (veya bot'a) verebilirsiniz; onlar da, hesapları olmasına bile gerek kalmadan, sadece API'nizin bunun için ürettiği JWT token'ıyla bu aksiyonları gerçekleştirebilir (arabayı sürmek veya blog post'u düzenlemek gibi).

Bu fikirlerle JWT, çok daha gelişmiş senaryolarda kullanılabilir.

Bu durumlarda, birden fazla varlığın aynı ID'ye sahip olması mümkündür; örneğin `foo` (kullanıcı `foo`, araba `foo`, blog post `foo`).

Dolayısıyla ID çakışmalarını önlemek için, kullanıcı için JWT token oluştururken `sub` anahtarının değerine bir önek ekleyebilirsiniz; örneğin `username:`. Bu örnekte `sub` değeri şöyle olabilirdi: `username:johndoe`.

Unutmamanız gereken önemli nokta şudur: `sub` anahtarı, tüm uygulama genelinde benzersiz bir tanımlayıcı olmalı ve string olmalıdır.

## Kontrol Edelim { #check-it }

Server'ı çalıştırın ve docs'a gidin: <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Şuna benzer bir arayüz göreceksiniz:

<img src="/img/tutorial/security/image07.png">

Uygulamayı, öncekiyle aynı şekilde authorize edin.

Şu kimlik bilgilerini kullanarak:

Username: `johndoe`
Password: `secret`

/// check | Ek bilgi

Kodun hiçbir yerinde düz metin password "`secret`" yok; sadece hash'lenmiş hâli var.

///

<img src="/img/tutorial/security/image08.png">

`/users/me/` endpoint'ini çağırın; response şöyle olacaktır:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Developer tools'u açarsanız, gönderilen verinin sadece token'ı içerdiğini görebilirsiniz. Password sadece kullanıcıyı authenticate edip access token almak için yapılan ilk request'te gönderilir, sonrasında gönderilmez:

<img src="/img/tutorial/security/image10.png">

/// note | Not

`Authorization` header'ına dikkat edin; değeri `Bearer ` ile başlıyor.

///

## `scopes` ile İleri Seviye Kullanım { #advanced-usage-with-scopes }

OAuth2'nin "scopes" kavramı vardır.

Bunları kullanarak bir JWT token'a belirli bir izin seti ekleyebilirsiniz.

Sonra bu token'ı bir kullanıcıya doğrudan veya bir üçüncü tarafa verip, API'nizle belirli kısıtlarla etkileşime girmesini sağlayabilirsiniz.

Nasıl kullanıldıklarını ve **FastAPI** ile nasıl entegre olduklarını, ileride **Advanced User Guide** içinde öğreneceksiniz.

## Özet { #recap }

Şimdiye kadar gördüklerinizle, OAuth2 ve JWT gibi standartları kullanarak güvenli bir **FastAPI** uygulaması kurabilirsiniz.

Neredeyse her framework'te security'yi ele almak oldukça hızlı bir şekilde karmaşık bir konu hâline gelir.

Bunu çok basitleştiren birçok paket, veri modeli, veritabanı ve mevcut özelliklerle ilgili pek çok ödün vermek zorunda kalır. Hatta bazıları işi aşırı basitleştirirken arka planda güvenlik açıkları da barındırır.

---

**FastAPI**, hiçbir veritabanı, veri modeli veya araç konusunda ödün vermez.

Projenize en uygun olanları seçebilmeniz için size tam esneklik sağlar.

Ayrıca `pwdlib` ve `PyJWT` gibi iyi bakımı yapılan ve yaygın kullanılan paketleri doğrudan kullanabilirsiniz; çünkü **FastAPI**, haricî paketleri entegre etmek için karmaşık mekanizmalara ihtiyaç duymaz.

Buna rağmen, esneklikten, sağlamlıktan veya güvenlikten ödün vermeden süreci mümkün olduğunca basitleştiren araçları sağlar.

Ve OAuth2 gibi güvenli, standart protokolleri nispeten basit bir şekilde kullanabilir ve uygulayabilirsiniz.

Aynı standartları izleyerek, daha ince taneli (fine-grained) bir izin sistemi için OAuth2 "scopes" kullanımını **Advanced User Guide** içinde daha detaylı öğrenebilirsiniz. Scopes'lu OAuth2; Facebook, Google, GitHub, Microsoft, X (Twitter) vb. pek çok büyük kimlik doğrulama sağlayıcısının, üçüncü taraf uygulamaların kullanıcıları adına API'leriyle etkileşebilmesine izin vermek için kullandığı mekanizmadır.
