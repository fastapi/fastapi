# Testing Events: lifespan और startup - shutdown { #testing-events-lifespan-and-startup-shutdown }

जब आपको अपने tests में `lifespan` चलाने की ज़रूरत हो, तो आप `with` statement के साथ `TestClient` का उपयोग कर सकते हैं:

{* ../../docs_src/app_testing/tutorial004_py310.py hl[9:15,18,27:28,30:32,41:43] *}


आप इसके बारे में अधिक विवरण ["आधिकारिक Starlette documentation site में tests में lifespan चलाना।"](https://www.starlette.dev/lifespan/#running-lifespan-in-tests) में पढ़ सकते हैं।

deprecated `startup` और `shutdown` event के लिए, आप `TestClient` का उपयोग इस प्रकार कर सकते हैं:

{* ../../docs_src/app_testing/tutorial003_py310.py hl[9:12,20:24] *}
