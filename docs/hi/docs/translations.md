# Translations (अनुवाद) { #translations }

Translation pull requests LLMs द्वारा बनाए जाते हैं, जो FastAPI team द्वारा प्रत्येक समर्थित भाषा के लिए native speakers की community के साथ मिलकर डिज़ाइन किए गए prompts द्वारा निर्देशित होते हैं।

## प्रत्येक भाषा के लिए LLM Prompt { #llm-prompt-per-language }

प्रत्येक भाषा की एक directory होती है: [https://github.com/fastapi/fastapi/tree/master/docs](https://github.com/fastapi/fastapi/tree/master/docs), इसमें आप उस भाषा के लिए विशिष्ट prompt वाली एक file `llm-prompt.md` देख सकते हैं।

उदाहरण के लिए, स्पैनिश (Spanish) के लिए, prompt यहाँ है: [`docs/es/llm-prompt.md`](https://github.com/fastapi/fastapi/blob/master/docs/es/llm-prompt.md)।

यदि आप अपनी भाषा में गलतियाँ देखते हैं, तो आप अपनी भाषा के लिए उस file में prompt के लिए सुझाव दे सकते हैं, और उन विशिष्ट pages का अनुरोध कर सकते हैं जिन्हें आप परिवर्तनों के बाद फिर से generate करना चाहते हैं।

भाषा-विशिष्ट LLM prompt के सुझावों वाले PRs के लिए कम से कम एक native speaker के approval की आवश्यकता होती है। यहाँ आपकी मदद की बहुत सराहना की जाती है!

## एक नई भाषा का अनुरोध करें { #request-a-new-language }

मान लीजिए कि आप किसी ऐसी भाषा के अनुवाद का अनुरोध करना चाहते हैं जिसका अभी तक अनुवाद नहीं हुआ है, कुछ pages भी नहीं। उदाहरण के लिए, लैटिन (Latin)।

* पहला कदम आपके लिए 2 अन्य लोगों को खोजना होगा जो आपके साथ उस भाषा के लिए translation PRs की समीक्षा (review) करने के इच्छुक हों।
* एक बार जब कम से कम 3 लोग उस भाषा को maintain करने में मदद करने के लिए प्रतिबद्ध होने को तैयार हों, तो आप अगले कदम जारी रख सकते हैं।
* Template का पालन करते हुए एक नया discussion बनाएँ।
* अन्य 2 लोगों को tag करें जो उस भाषा में मदद करेंगे, और उनसे comments में पुष्टि करने के लिए कहें कि वे मदद करेंगे।

एक बार जब discussion में कई लोग शामिल हो जाते हैं, तो FastAPI team इसका मूल्यांकन कर सकती है और इसे एक official translation बना सकती है।

फिर docs को LLMs का उपयोग करके स्वचालित रूप से अनुवादित किया जाएगा, और native speakers की team अनुवाद की समीक्षा कर सकती है, और LLM prompts को बेहतर बनाने में मदद कर सकती है।

एक बार जब कोई नया अनुवाद उपलब्ध हो जाता है, उदाहरण के लिए यदि docs अपडेट किए जाते हैं या कोई नया section आता है, तो समीक्षा करने के लिए नए अनुवाद के लिंक के साथ उसी discussion में एक comment होगा।
