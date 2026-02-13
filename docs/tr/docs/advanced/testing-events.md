# Event'leri Test Etme: lifespan ve startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

Test'lerinizde `lifespan`'ın çalışması gerektiğinde, `TestClient`'ı bir `with` ifadesiyle kullanabilirsiniz:

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}


Bu konuda daha fazla ayrıntıyı resmi Starlette dokümantasyon sitesindeki ["Testlerde lifespan'ı çalıştırma"](https://www.starlette.dev/lifespan/#running-lifespan-in-tests) bölümünde okuyabilirsiniz.

Kullanımdan kaldırılmış `startup` ve `shutdown` event'leri için ise `TestClient`'ı aşağıdaki gibi kullanabilirsiniz:

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
