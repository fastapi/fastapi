# Dağıtım { #deployment }

**FastAPI** uygulamasını deploy etmek nispeten kolaydır.

## Dağıtım Ne Anlama Gelir? { #what-does-deployment-mean }

Bir uygulamayı **deploy** etmek, onu **kullanıcılara erişilebilir hale getirmek** için gerekli adımları gerçekleştirmek anlamına gelir.

Bir **web API** için bu süreç normalde uygulamayı **uzak bir makineye** yerleştirmeyi, iyi performans, kararlılık vb. özellikler sağlayan bir **sunucu programı** ile **kullanıcılarınızın** uygulamaya etkili ve kesintisiz bir şekilde, sorun yaşamadan **erişebilmesini** kapsar.

Bu, kodu sürekli olarak değiştirdiğiniz, bozup düzelttiğiniz, geliştirme sunucusunu durdurup yeniden başlattığınız vb. **geliştirme** aşamalarının tam tersidir.

## Dağıtım Stratejileri { #deployment-strategies }

Kullanım durumunuza ve kullandığınız araçlara bağlı olarak bunu yapmanın birkaç yolu vardır.

Bir dizi araç kombinasyonunu kullanarak kendiniz **bir sunucu deploy edebilirsiniz**, yayınlama sürecinin bir kısmını sizin için gerçekleştiren bir **bulut hizmeti** veya diğer olası seçenekleri kullanabilirsiniz.

Örneğin, FastAPI'nin arkasındaki ekip olarak, FastAPI uygulamalarını buluta mümkün olduğunca akıcı şekilde deploy etmeyi sağlamak için, FastAPI ile çalışmanın aynı geliştirici deneyimini sunarak <a href="https://fastapicloud.com" class="external-link" target="_blank">**FastAPI Cloud**</a>'u oluşturduk.

**FastAPI** uygulamasını yayınlarken aklınızda bulundurmanız gereken ana kavramlardan bazılarını size göstereceğim (ancak bunların çoğu diğer web uygulamaları için de geçerlidir).

Sonraki bölümlerde akılda tutulması gereken diğer ayrıntıları ve bunu yapmaya yönelik bazı teknikleri göreceksiniz. ✨
