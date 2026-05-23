# Override Kullanarak Dependency'leri Test Etme { #testing-dependencies-with-overrides }

## Test Sırasında Dependency Override Etme { #overriding-dependencies-during-testing }

Test yazarken bazı durumlarda bir dependency'yi override etmek isteyebilirsiniz.

Orijinal dependency'nin (ve varsa tüm alt dependency'lerinin) çalışmasını istemezsiniz.

Bunun yerine, yalnızca testler sırasında (hatta belki sadece belirli bazı testlerde) kullanılacak farklı bir dependency sağlarsınız; böylece orijinal dependency'nin ürettiği değerin kullanıldığı yerde, test için üretilen değeri kullanabilirsiniz.

### Kullanım Senaryoları: Harici Servis { #use-cases-external-service }

Örneğin, çağırmanız gereken harici bir authentication provider'ınız olabilir.

Ona bir token gönderirsiniz ve o da authenticated bir user döndürür.

Bu provider request başına ücret alıyor olabilir ve onu çağırmak, testlerde sabit bir mock user kullanmaya kıyasla daha fazla zaman alabilir.

Muhtemelen harici provider'ı bir kez test etmek istersiniz; ancak çalışan her testte onu çağırmanız şart değildir.

Bu durumda, o provider'ı çağıran dependency'yi override edebilir ve yalnızca testleriniz için mock user döndüren özel bir dependency kullanabilirsiniz.

### `app.dependency_overrides` Attribute'ünü Kullanın { #use-the-app-dependency-overrides-attribute }

Bu tür durumlar için **FastAPI** uygulamanızda `app.dependency_overrides` adında bir attribute bulunur; bu basit bir `dict`'tir.

Test için bir dependency'yi override etmek istediğinizde, key olarak orijinal dependency'yi (bir function), value olarak da override edecek dependency'nizi (başka bir function) verirsiniz.

Böylece **FastAPI**, orijinal dependency yerine bu override'ı çağırır.

{* ../../docs_src/dependency_testing/tutorial001_an_py310.py hl[26:27,30] *}

/// tip | İpucu

**FastAPI** uygulamanızın herhangi bir yerinde kullanılan bir dependency için override tanımlayabilirsiniz.

Orijinal dependency bir *path operation function* içinde, bir *path operation decorator* içinde (return value kullanmadığınız durumlarda), bir `.include_router()` çağrısında, vb. kullanılıyor olabilir.

FastAPI yine de onu override edebilir.

///

Sonrasında override'larınızı (yani kaldırıp sıfırlamayı) `app.dependency_overrides` değerini boş bir `dict` yaparak gerçekleştirebilirsiniz:

```Python
app.dependency_overrides = {}
```


/// tip | İpucu

Bir dependency'yi yalnızca bazı testler sırasında override etmek istiyorsanız, override'ı testin başında (test function'ının içinde) ayarlayıp testin sonunda (yine test function'ının sonunda) sıfırlayabilirsiniz.

///
