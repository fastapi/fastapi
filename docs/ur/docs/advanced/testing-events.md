# Events کی جانچ: lifespan اور startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

جب آپ کو اپنے ٹیسٹوں میں `lifespan` چلانے کی ضرورت ہو، تو آپ `TestClient` کو `with` statement کے ساتھ استعمال کر سکتے ہیں:

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}


آپ مزید تفصیلات ["Running lifespan in tests in the official Starlette documentation site."](https://www.starlette.dev/lifespan/#running-lifespan-in-tests) میں پڑھ سکتے ہیں۔

فرسودہ `startup` اور `shutdown` events کے لیے، آپ `TestClient` کو اس طرح استعمال کر سکتے ہیں:

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
