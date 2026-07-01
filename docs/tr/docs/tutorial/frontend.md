# Frontend { #frontend }

Statik frontend uygulamalarını `app.frontend()` (veya `router.frontend()`) ile sunabilirsiniz.

Bu, Vite ile React, TanStack Router, Astro, Vue, Svelte, Angular, Solid ve benzeri statik dosyalar üreten frontend araçları için kullanışlıdır.

Bu araçlarda genellikle frontend'i build eden bir adım olur, örneğin şöyle bir komutla:

```bash
npm run build
```

Bu komut, frontend dosyalarınızla birlikte `./dist/` gibi bir dizin oluşturur.

Bu dizini, frontend framework'lerinin ihtiyaç duyduğu kurallara uygun şekilde sunmak için `app.frontend()` kullanabilirsiniz.

**FastAPI** önce *path operation*'ları kontrol eder. Frontend dosyaları yalnızca hiçbir normal route eşleşmezse kontrol edilir, bu yüzden API'niz bundan etkilenmez.

## Frontend Sunma { #serve-a-frontend }

Frontend'inizi build ettikten sonra, örneğin `npm run build` ile, oluşturulan dosyaları bir dizine koyun; örneğin `dist`.

Proje yapınız şöyle görünebilir:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

Ardından bunu `app.frontend()` ile sunun:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

Böylece `/assets/app.js` için gelen bir request, `dist/assets/app.js` dosyasını sunabilir.

Aynı zamanda bir **FastAPI** *path operation*'ınız varsa, öncelik *path operation*'dadır.

## Client-Side Routing { #client-side-routing }

**Single-page app**'ler (SPA'ler) dahil birçok frontend uygulaması client-side routing kullanır. `/dashboard/settings` gibi bir path gerçek bir dosya olmayabilir; bunu frontend framework'ü ele alır.

Bu yüzden, o URL'ye doğrudan erişildiğinde (uygulama içinde gezinmek yerine), backend frontend uygulamasını `index.html` üzerinden sunmalıdır. Böylece frontend framework'ü client-side routing'i işleyebilir.

Bunun için `fallback="index.html"` kullanın:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** bu fallback'i yalnızca tarayıcı gezinmesi gibi görünen `GET` ve `HEAD` request'leri için kullanır. JavaScript, CSS ve görseller gibi eksik dosyalar yine `404` döndürür.

`POST` veya `PUT` gibi diğer metotlarla, yalnızca frontend fallback'i ile eşleşen path'lere yapılan request'ler de `404` döndürür. Normal **FastAPI** *path operation*'ları frontend route'larından yine daha yüksek önceliğe sahiptir.

/// tip | İpucu

Varsayılan olarak `fallback`, `fallback="auto"` değerine sahiptir. Çoğu durumda `fallback` belirtmeniz gerekmez. Detaylar için aşağıyı okuyun.

///

Client-side routing kullanan birçok frontend uygulamasında istediğiniz davranış budur; örneğin TanStack Router ile React, Vue, Angular, SvelteKit veya Solid.

## Özel 404 Sayfası { #custom-404-page }

Bulunamayan frontend path'leri için statik bir `404.html` sayfası da sunabilirsiniz:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

Bu response, `404` status code'unu korur.

Bu durumda **FastAPI**, bulunamayan frontend path'leri için `index.html` sunmaz. Bunun yerine `404.html` dosyasını döndürür.

/// tip | İpucu

Varsayılan olarak `fallback`, `fallback="auto"` değerine sahiptir. Bu durumda bir `404.html` dosyası bulunursa, otomatik olarak fallback olarak kullanılır.

Bu yüzden normalde `fallback` argümanını atlayabilirsiniz.

///

Bu, Astro gibi her sayfa için statik HTML dosyaları üreten frontend araçlarıyla kullanışlıdır.

## Otomatik Fallback { #fallback-auto }

Varsayılan olarak `app.frontend()`, `fallback="auto"` kullanır.

Frontend dizininde bir `404.html` dosyası varsa, bulunamayan frontend path'leri bu dosyayı `404` status code'u ile sunar.

Aksi halde bir `index.html` dosyası varsa, bulunamayan tarayıcı gezinme path'leri `index.html` sunar. Client-side routing kullanan birçok frontend uygulamasının beklediği davranış budur.

Bu yüzden çoğu durumda `fallback` argümanını belirtmeden `app.frontend("/", directory="dist")` kullanabilirsiniz.

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Fallback'i Devre Dışı Bırakma { #disable-fallback }

Bulunamayan frontend path'leri için fallback dosyası sunmak istemiyorsanız `fallback=None` kullanın:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

Bundan sonra bulunamayan frontend path'leri normal `404` döndürür.

## Dizini Kontrol Etme { #check-directory }

Varsayılan olarak `app.frontend()`, uygulama oluşturulduğunda dizinin var olduğunu kontrol eder.

Bu, yapılandırma hatalarını erken yakalamaya yardımcı olur. Örneğin frontend build çıktısı dizini yoksa, **FastAPI** başlangıçta hata verir.

Frontend dosyalarınız daha sonra oluşturuluyorsa, örneğin app nesnesi oluşturulduktan sonra ayrı bir build adımıyla, `check_dir=False` ayarlayın:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

`check_dir=False` ile **FastAPI**, app oluşturulduğunda dizini kontrol etmez. Yapılandırılan dizin bir request işlendiği sırada hâlâ yoksa, **FastAPI** o zaman hata verir.

## `APIRouter` ile Kullanma { #use-it-with-apirouter }

Frontend dosyalarını bir `APIRouter`'a da ekleyebilir ve bunu bir prefix ile dahil edebilirsiniz:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

Bu örnekte frontend path'leri `/app` altında sunulur.

Uygulamadaki herhangi bir normal *path operation*, diğer router'larda olanlar dahil, yine öncelikli olur.

## Yalnızca Statik Build Çıktısı { #static-build-output-only }

`app.frontend()`, frontend build'iniz tarafından önceden oluşturulmuş dosyaları sunar.

Server-side rendering çalıştırmaz. Her request için server'da dinamik rendering gerektiren framework'ler için değil, statik dosyalar üreten frontend framework'leri içindir.
