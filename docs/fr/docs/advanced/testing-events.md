# Tester les événements : lifespan et startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

Lorsque vous avez besoin d'exécuter `lifespan` dans vos tests, vous pouvez utiliser `TestClient` avec une instruction `with` :

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}

Vous pouvez lire plus de détails dans [« Exécuter lifespan dans les tests sur le site de documentation officiel de Starlette. »](https://www.starlette.dev/lifespan/#running-lifespan-in-tests)

Pour les événements dépréciés `startup` et `shutdown`, vous pouvez utiliser le `TestClient` comme suit :

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
