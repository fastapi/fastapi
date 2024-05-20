# Deployment (Yayınlama)

**FastAPI** uygulamasını deploy etmek oldukça kolaydır.

## Deployment Ne Anlama Gelir?

Bir uygulamayı **deploy** etmek (yayınlamak), uygulamayı **kullanıcılara erişilebilir hale getirmek** için gerekli adımları gerçekleştirmek anlamına gelir.

Bir **Web API** için, bu süreç normalde uygulamayı **uzak bir makineye** yerleştirmeyi, iyi performans, kararlılık vb. özellikler sağlayan bir **sunucu programı** ile **kullanıcılarınızın** uygulamaya etkili ve kesintisiz bir şekilde **erişebilmesini** kapsar.

Bu, kodu sürekli olarak değiştirdiğiniz, hata alıp hata giderdiğiniz, geliştirme sunucusunu durdurup yeniden başlattığınız vb. **geliştirme** aşamalarının tam tersidir.

## Deployment Stratejileri

Kullanım durumunuza ve kullandığınız araçlara bağlı olarak bir kaç farklı yol izleyebilirsiniz.

Bir dizi araç kombinasyonunu kullanarak kendiniz **bir sunucu yayınlayabilirsiniz**, yayınlama sürecinin bir kısmını sizin için gerçekleştiren bir **bulut hizmeti** veya diğer olası seçenekleri kullanabilirsiniz.

I will show you some of the main concepts you should probably keep in mind when deploying a **FastAPI** application (although most of it applies to any other type of web application).

**FastAPI** uygulamasını yayınlarken aklınızda bulundurmanız gereken ana kavramlardan bazılarını size göstereceğim (ancak çoğu diğer web uygulamalarına da kullanılabilir).

Sonraki bölümlerde akılda tutulması gereken diğer ayrıntıları ve tekniklerinden bazılarını göreceksiniz. ✨
