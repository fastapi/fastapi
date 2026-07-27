# उन्नत Python Types { #advanced-python-types }

Python types के साथ काम करते समय यहाँ कुछ अतिरिक्त विचार हैं जो उपयोगी हो सकते हैं।

## `Union` या `Optional` का उपयोग { #using-union-or-optional }

अगर आपका code किसी कारण से `|` का उपयोग नहीं कर सकता, उदाहरण के लिए अगर यह type annotation में नहीं बल्कि `response_model=` जैसी किसी चीज़ में है, तो vertical bar (`|`) का उपयोग करने के बजाय आप `typing` से `Union` का उपयोग कर सकते हैं।

उदाहरण के लिए, आप declare कर सकते हैं कि कोई चीज़ `str` या `None` हो सकती है:

```python
from typing import Union


def say_hi(name: Union[str, None]):
        print(f"Hi {name}!")
```

`typing` में `Optional` के साथ यह declare करने का एक shortcut भी है कि कोई चीज़ `None` हो सकती है।

मेरे बहुत **subjective** दृष्टिकोण से एक tip यहाँ है:

* 🚨 `Optional[SomeType]` का उपयोग करने से बचें
* इसके बजाय ✨ **`Union[SomeType, None]` का उपयोग करें** ✨।

दोनों equivalent हैं और अंदर से वे समान हैं, लेकिन मैं `Optional` के बजाय `Union` की सलाह दूँगा क्योंकि "**optional**" शब्द से ऐसा लग सकता है कि value optional है, जबकि इसका वास्तविक अर्थ है "यह `None` हो सकता है", भले ही यह optional न हो और अभी भी required हो।

मुझे लगता है कि `Union[SomeType, None]` अपने अर्थ के बारे में अधिक explicit है।

यह बस शब्दों और नामों की बात है। लेकिन ये शब्द इस बात को प्रभावित कर सकते हैं कि आप और आपके teammates code के बारे में कैसे सोचते हैं।

एक उदाहरण के रूप में, इस function को लेते हैं:

```python
from typing import Optional


def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

parameter `name` को `Optional[str]` के रूप में define किया गया है, लेकिन यह **optional नहीं है**, आप function को parameter के बिना call नहीं कर सकते:

```Python
say_hi()  # अरे नहीं, यह error throw करता है! 😱
```

`name` parameter **अभी भी required** है (*optional* नहीं) क्योंकि इसमें default value नहीं है। फिर भी, `name` value के रूप में `None` स्वीकार करता है:

```Python
say_hi(name=None)  # यह काम करता है, None valid है 🎉
```

अच्छी खबर यह है कि अधिकतर मामलों में, आप types के unions को define करने के लिए बस `|` का उपयोग कर पाएँगे:

```python
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

इसलिए, सामान्यतः आपको `Optional` और `Union` जैसे नामों के बारे में चिंता करने की ज़रूरत नहीं होती। 😎
