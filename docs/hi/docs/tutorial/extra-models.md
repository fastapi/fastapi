# Extra Models { #extra-models }

पिछले उदाहरण को आगे बढ़ाते हुए, एक से अधिक संबंधित model होना आम बात होगी।

यह खासकर user models के मामले में होता है, क्योंकि:

* **input model** में password हो सकने की क्षमता चाहिए।
* **output model** में password नहीं होना चाहिए।
* **database model** में शायद hashed password होना चाहिए।

/// danger | खतरा

user के plaintext passwords कभी store न करें। हमेशा एक "secure hash" store करें जिसे आप बाद में verify कर सकें।

अगर आप नहीं जानते, तो आप [security chapters](security/simple-oauth2.md#password-hashing) में सीखेंगे कि "password hash" क्या होता है।

///

## कई models { #multiple-models }

यह एक सामान्य idea है कि models अपने password fields और जहाँ वे इस्तेमाल होते हैं, वहाँ कैसे दिख सकते हैं:

{* ../../docs_src/extra_models/tutorial001_py310.py hl[7,9,14,20,22,27:28,31:33,38:39] *}

### `**user_in.model_dump()` के बारे में { #about-user-in-model-dump }

#### Pydantic का `.model_dump()` { #pydantics-model-dump }

`user_in`, class `UserIn` का एक Pydantic model है।

Pydantic models में एक `.model_dump()` method होता है जो model के data के साथ एक `dict` return करता है।

तो, अगर हम इस तरह एक Pydantic object `user_in` बनाते हैं:

```Python
user_in = UserIn(username="john", password="secret", email="john.doe@example.com")
```

और फिर हम call करते हैं:

```Python
user_dict = user_in.model_dump()
```

तो अब हमारे पास variable `user_dict` में data के साथ एक `dict` है (यह Pydantic model object के बजाय एक `dict` है)।

और अगर हम call करते हैं:

```Python
print(user_dict)
```

तो हमें यह Python `dict` मिलेगा:

```Python
{
    'username': 'john',
    'password': 'secret',
    'email': 'john.doe@example.com',
    'full_name': None,
}
```

#### एक `dict` को unpack करना { #unpacking-a-dict }

अगर हम `user_dict` जैसा एक `dict` लेते हैं और उसे किसी function (या class) को `**user_dict` के साथ pass करते हैं, तो Python उसे "unpack" करेगा। यह `user_dict` की keys और values को सीधे key-value arguments के रूप में pass करेगा।

तो, ऊपर वाले `user_dict` को जारी रखते हुए, यह लिखना:

```Python
UserInDB(**user_dict)
```

कुछ इस equivalent result देगा:

```Python
UserInDB(
    username="john",
    password="secret",
    email="john.doe@example.com",
    full_name=None,
)
```

या अधिक सही रूप में, `user_dict` को सीधे इस्तेमाल करते हुए, उसमें भविष्य में जो भी contents हों:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
)
```

#### दूसरे model के contents से एक Pydantic model { #a-pydantic-model-from-the-contents-of-another }

जैसा कि ऊपर के उदाहरण में हमें `user_in.model_dump()` से `user_dict` मिला, यह code:

```Python
user_dict = user_in.model_dump()
UserInDB(**user_dict)
```

इसके equivalent होगा:

```Python
UserInDB(**user_in.model_dump())
```

...क्योंकि `user_in.model_dump()` एक `dict` है, और फिर हम उसे `**` prefix के साथ `UserInDB` को pass करके Python से उसे "unpack" करवाते हैं।

तो, हमें एक Pydantic model के data से दूसरा Pydantic model मिलता है।

#### एक `dict` को unpack करना और extra keywords { #unpacking-a-dict-and-extra-keywords }

और फिर extra keyword argument `hashed_password=hashed_password` जोड़ना, जैसे:

```Python
UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
```

...अंत में ऐसा बन जाता है:

```Python
UserInDB(
    username = user_dict["username"],
    password = user_dict["password"],
    email = user_dict["email"],
    full_name = user_dict["full_name"],
    hashed_password = hashed_password,
)
```

/// warning | चेतावनी

supporting additional functions `fake_password_hasher` और `fake_save_user` सिर्फ data के एक possible flow को demo करने के लिए हैं, लेकिन वे निश्चित रूप से कोई real security नहीं दे रहे हैं।

///

## Duplication कम करें { #reduce-duplication }

Code duplication कम करना **FastAPI** के core ideas में से एक है।

क्योंकि code duplication बढ़ने से bugs, security issues, code desynchronization issues (जब आप एक जगह update करते हैं लेकिन बाकी जगह नहीं), आदि की संभावना बढ़ जाती है।

और ये models बहुत सारा data share कर रहे हैं और attribute names और types को duplicate कर रहे हैं।

हम इससे बेहतर कर सकते हैं।

हम एक `UserBase` model declare कर सकते हैं जो हमारे दूसरे models के लिए base की तरह काम करता है। और फिर हम उस model की subclasses बना सकते हैं जो उसके attributes (type declarations, validation, आदि) inherit करती हैं।

सारा data conversion, validation, documentation, आदि सामान्य रूप से काम करता रहेगा।

इस तरह, हम केवल models के बीच के अंतर declare कर सकते हैं (plaintext `password` के साथ, `hashed_password` के साथ और password के बिना):

{* ../../docs_src/extra_models/tutorial002_py310.py hl[7,13:14,17:18,21:22] *}

## `Union` या `anyOf` { #union-or-anyof }

आप response को दो या अधिक types के `Union` के रूप में declare कर सकते हैं, जिसका मतलब है कि response उनमें से कोई भी हो सकता है।

इसे OpenAPI में `anyOf` के साथ define किया जाएगा।

ऐसा करने के लिए, standard Python type hint [`typing.Union`](https://docs.python.org/3/library/typing.html#typing.Union) का इस्तेमाल करें:

/// note | नोट

[`Union`](https://docs.pydantic.dev/latest/concepts/types/#unions) define करते समय, सबसे specific type को पहले include करें, उसके बाद कम specific type को। नीचे दिए गए उदाहरण में, अधिक specific `PlaneItem`, `Union[PlaneItem, CarItem]` में `CarItem` से पहले आता है।

///

{* ../../docs_src/extra_models/tutorial003_py310.py hl[1,14:15,18:20,33] *}

### Python 3.10 में `Union` { #union-in-python-3-10 }

इस उदाहरण में हम argument `response_model` की value के रूप में `Union[PlaneItem, CarItem]` pass करते हैं।

क्योंकि हम इसे **type annotation** में रखने के बजाय **argument को value** के रूप में pass कर रहे हैं, इसलिए हमें Python 3.10 में भी `Union` इस्तेमाल करना होगा।

अगर यह type annotation में होता तो हम vertical bar इस्तेमाल कर सकते थे, जैसे:

```Python
some_variable: PlaneItem | CarItem
```

लेकिन अगर हम इसे assignment `response_model=PlaneItem | CarItem` में डालते, तो हमें error मिलता, क्योंकि Python इसे type annotation के रूप में interpret करने के बजाय `PlaneItem` और `CarItem` के बीच एक **invalid operation** perform करने की कोशिश करता।

## Models की list { #list-of-models }

इसी तरह, आप objects की lists के responses declare कर सकते हैं।

इसके लिए, standard Python `list` इस्तेमाल करें:

{* ../../docs_src/extra_models/tutorial004_py310.py hl[18] *}

## Arbitrary `dict` के साथ response { #response-with-arbitrary-dict }

आप plain arbitrary `dict` का इस्तेमाल करके भी response declare कर सकते हैं, जिसमें Pydantic model का इस्तेमाल किए बिना केवल keys और values का type declare किया जाता है।

यह तब उपयोगी है जब आपको valid field/attribute names (जो Pydantic model के लिए चाहिए होंगे) पहले से नहीं पता हों।

इस मामले में, आप `dict` इस्तेमाल कर सकते हैं:

{* ../../docs_src/extra_models/tutorial005_py310.py hl[6] *}

## Recap { #recap }

हर case के लिए कई Pydantic models इस्तेमाल करें और freely inherit करें।

अगर किसी entity में अलग-अलग "states" हो सकने चाहिए, तो आपको प्रति entity एक ही data model रखने की जरूरत नहीं है। **user** "entity" एक उदाहरण है, जिसमें states में `password`, `password_hash`, या कोई password नहीं होना शामिल है।
