# Global Dependencies { #global-dependencies }

Bazı uygulama türlerinde, tüm uygulama için dependency eklemek isteyebilirsiniz.

[`dependencies`'i *path operation decorator*'larına ekleyebildiğiniz](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} gibi, `FastAPI` uygulamasına da ekleyebilirsiniz.

Bu durumda, uygulamadaki tüm *path operation*'lara uygulanırlar:

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}


Ve [*path operation decorator*'larına `dependencies` ekleme](dependencies-in-path-operation-decorators.md){.internal-link target=_blank} bölümündeki tüm fikirler hâlâ geçerlidir; ancak bu sefer, uygulamadaki tüm *path operation*'lar için geçerli olur.

## *Path operations* grupları için Dependencies { #dependencies-for-groups-of-path-operations }

İleride, daha büyük uygulamaları nasıl yapılandıracağınızı ([Bigger Applications - Multiple Files](../../tutorial/bigger-applications.md){.internal-link target=_blank}) okurken, muhtemelen birden fazla dosyayla birlikte, bir *path operations* grubu için tek bir `dependencies` parametresini nasıl tanımlayacağınızı öğreneceksiniz.
