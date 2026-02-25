# Eski 403 Kimlik Doğrulama Hata Durum Kodlarını Kullanma { #use-old-403-authentication-error-status-codes }

FastAPI `0.122.0` sürümünden önce, entegre security yardımcı araçları başarısız bir kimlik doğrulama (authentication) sonrasında client'a bir hata döndüğünde HTTP durum kodu olarak `403 Forbidden` kullanıyordu.

FastAPI `0.122.0` sürümünden itibaren ise daha uygun olan HTTP durum kodu `401 Unauthorized` kullanılmakta ve HTTP spesifikasyonlarına uygun olarak response içinde anlamlı bir `WWW-Authenticate` header'ı döndürülmektedir: <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>, <a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>.

Ancak herhangi bir nedenle client'larınız eski davranışa bağlıysa, security class'larınızda `make_not_authenticated_error` metodunu override ederek eski davranışa geri dönebilirsiniz.

Örneğin, varsayılan `401 Unauthorized` hatası yerine `403 Forbidden` hatası döndüren bir `HTTPBearer` alt sınıfı oluşturabilirsiniz:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | İpucu

Fonksiyonun exception instance'ını döndürdüğüne dikkat edin; exception'ı raise etmiyor. Raise işlemi internal kodun geri kalan kısmında yapılıyor.

///
