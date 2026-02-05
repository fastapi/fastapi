# FastAPI Sürümleri Hakkında { #about-fastapi-versions }

**FastAPI** hâlihazırda birçok uygulama ve sistemde production ortamında kullanılmaktadır. Ayrıca test kapsamı %100 seviyesinde tutulmaktadır. Ancak geliştirme süreci hâlâ hızlı şekilde ilerlemektedir.

Yeni özellikler sık sık eklenir, bug'lar düzenli olarak düzeltilir ve kod sürekli iyileştirilmektedir.

Bu yüzden mevcut sürümler hâlâ `0.x.x` şeklindedir; bu da her sürümde breaking change olma ihtimalini yansıtır. Bu yaklaşım <a href="https://semver.org/" class="external-link" target="_blank">Semantic Versioning</a> kurallarını takip eder.

Şu anda **FastAPI** ile production uygulamaları geliştirebilirsiniz (muhtemelen bir süredir yapıyorsunuz da); sadece kodunuzun geri kalanıyla doğru çalışan bir sürüm kullandığınızdan emin olmanız gerekir.

## `fastapi` sürümünü sabitleyin { #pin-your-fastapi-version }

İlk yapmanız gereken, kullandığınız **FastAPI** sürümünü uygulamanızla doğru çalıştığını bildiğiniz belirli bir güncel sürüme "sabitlemek" (pinlemek) olmalı.

Örneğin, uygulamanızda `0.112.0` sürümünü kullandığınızı varsayalım.

`requirements.txt` dosyası kullanıyorsanız sürümü şöyle belirtebilirsiniz:

```txt
fastapi[standard]==0.112.0
```

Bu, tam olarak `0.112.0` sürümünü kullanacağınız anlamına gelir.

Ya da şu şekilde de sabitleyebilirsiniz:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

Bu da `0.112.0` ve üzeri, ama `0.113.0` altındaki sürümleri kullanacağınız anlamına gelir; örneğin `0.112.2` gibi bir sürüm de kabul edilir.

Kurulumları yönetmek için `uv`, Poetry, Pipenv gibi başka bir araç (veya benzerleri) kullanıyorsanız, bunların hepsinde paketler için belirli sürümler tanımlamanın bir yolu vardır.

## Mevcut sürümler { #available-versions }

Mevcut sürümleri (ör. en güncel son sürümün hangisi olduğunu kontrol etmek için) [Release Notes](../release-notes.md){.internal-link target=_blank} sayfasında görebilirsiniz.

## Sürümler Hakkında { #about-versions }

Semantic Versioning kurallarına göre, `1.0.0` altındaki herhangi bir sürüm breaking change içerebilir.

FastAPI ayrıca "PATCH" sürüm değişikliklerinin bug fix'ler ve breaking olmayan değişiklikler için kullanılması kuralını da takip eder.

/// tip | İpucu

"PATCH" son sayıdır. Örneğin `0.2.3` içinde PATCH sürümü `3`'tür.

///

Dolayısıyla şu şekilde bir sürüme sabitleyebilmelisiniz:

```txt
fastapi>=0.45.0,<0.46.0
```

Breaking change'ler ve yeni özellikler "MINOR" sürümlerde eklenir.

/// tip | İpucu

"MINOR" ortadaki sayıdır. Örneğin `0.2.3` içinde MINOR sürümü `2`'dir.

///

## FastAPI Sürümlerini Yükseltme { #upgrading-the-fastapi-versions }

Uygulamanız için test'ler eklemelisiniz.

**FastAPI** ile bu çok kolaydır (Starlette sayesinde). Dokümantasyona bakın: [Testing](../tutorial/testing.md){.internal-link target=_blank}

Test'leriniz olduktan sonra **FastAPI** sürümünü daha yeni bir sürüme yükseltebilir ve test'lerinizi çalıştırarak tüm kodunuzun doğru çalıştığından emin olabilirsiniz.

Her şey çalışıyorsa (ya da gerekli değişiklikleri yaptıktan sonra) ve tüm test'leriniz geçiyorsa, `fastapi` sürümünü o yeni sürüme sabitleyebilirsiniz.

## Starlette Hakkında { #about-starlette }

`starlette` sürümünü sabitlememelisiniz.

**FastAPI**'nin farklı sürümleri, Starlette'in belirli (daha yeni) bir sürümünü kullanır.

Bu yüzden **FastAPI**'nin doğru Starlette sürümünü kullanmasına izin verebilirsiniz.

## Pydantic Hakkında { #about-pydantic }

Pydantic, **FastAPI** için olan test'leri kendi test'lerinin içine dahil eder; bu yüzden Pydantic'in yeni sürümleri (`1.0.0` üzeri) her zaman FastAPI ile uyumludur.

Pydantic'i sizin için çalışan `1.0.0` üzerindeki herhangi bir sürüme sabitleyebilirsiniz.

Örneğin:

```txt
pydantic>=2.7.0,<3.0.0
```
