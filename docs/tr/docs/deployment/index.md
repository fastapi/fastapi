# Deployment { #deployment }

**FastAPI** uygulamasını deploy etmek nispeten kolaydır.

## Deployment Ne Anlama Gelir { #what-does-deployment-mean }

Bir uygulamayı **deploy** etmek, uygulamayı **kullanıcıların erişimine sunmak** için gerekli adımları gerçekleştirmek anlamına gelir.

Bir **web API** için bu, normalde uygulamayı **uzak bir makineye** koymayı; iyi performans, kararlılık vb. sağlayan bir **sunucu programı** ile **kullanıcılarınızın** uygulamaya verimli bir şekilde ve kesinti ya da sorun yaşamadan **erişebilmesini** sağlamayı içerir.

Bu, kodu sürekli değiştirdiğiniz, bozup düzelttiğiniz, geliştirme sunucusunu durdurup yeniden başlattığınız vb. **geliştirme** aşamalarının tersidir.

## Deployment Stratejileri { #deployment-strategies }

Kullanım senaryonuza ve kullandığınız araçlara bağlı olarak bunu yapmanın birkaç yolu vardır.

Bir dizi aracın kombinasyonunu kullanarak kendiniz **bir sunucu deploy edebilirsiniz**, işin bir kısmını sizin için yapan bir **bulut hizmeti** kullanabilirsiniz veya başka olası seçenekler de vardır.

Örneğin, FastAPI'nin arkasındaki ekip olarak, FastAPI ile çalışmanın aynı geliştirici deneyimiyle, FastAPI uygulamalarını buluta deploy etmeyi mümkün olduğunca kolaylaştırmak için <a href="https://fastapicloud.com" class="external-link" target="_blank">**FastAPI Cloud**</a>'u geliştirdik.

**FastAPI** uygulamasını deploy ederken muhtemelen aklınızda tutmanız gereken ana kavramlardan bazılarını size göstereceğim (bunların çoğu diğer herhangi bir web uygulaması türü için de geçerlidir).

Sonraki bölümlerde, akılda tutulması gereken daha fazla ayrıntı ve bunu yapmak için bazı teknikler göreceksiniz. ✨
