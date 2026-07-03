# अतिरिक्त Data Types { #extra-data-types }

अब तक, आप सामान्य data types का उपयोग करते रहे हैं, जैसे:

* `int`
* `float`
* `str`
* `bool`

लेकिन आप अधिक जटिल data types भी उपयोग कर सकते हैं।

और आपको अब तक देखी गई वही features मिलती रहेंगी:

* शानदार editor support.
* आने वाली requests से data conversion.
* response data के लिए data conversion.
* Data validation.
* Automatic annotation और documentation.

## अन्य data types { #other-data-types }

यहाँ कुछ अतिरिक्त data types हैं जिनका आप उपयोग कर सकते हैं:

* `UUID`:
    * एक standard "Universally Unique Identifier", जो कई databases और systems में ID के रूप में आम है।
    * requests और responses में इसे `str` के रूप में दर्शाया जाएगा।
* `datetime.datetime`:
    * एक Python `datetime.datetime`.
    * requests और responses में इसे ISO 8601 format में `str` के रूप में दर्शाया जाएगा, जैसे: `2008-09-15T15:53:00+05:00`.
* `datetime.date`:
    * Python `datetime.date`.
    * requests और responses में इसे ISO 8601 format में `str` के रूप में दर्शाया जाएगा, जैसे: `2008-09-15`.
* `datetime.time`:
    * एक Python `datetime.time`.
    * requests और responses में इसे ISO 8601 format में `str` के रूप में दर्शाया जाएगा, जैसे: `14:23:55.003`.
* `datetime.timedelta`:
    * एक Python `datetime.timedelta`.
    * requests और responses में इसे कुल seconds के `float` के रूप में दर्शाया जाएगा।
    * Pydantic इसे "ISO 8601 time diff encoding" के रूप में दर्शाने की अनुमति भी देता है, [अधिक जानकारी के लिए docs देखें](https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers).
* `frozenset`:
    * requests और responses में, इसे `set` जैसा ही माना जाता है:
        * requests में, एक list पढ़ी जाएगी, duplicates हटाए जाएँगे और उसे `set` में convert किया जाएगा।
        * responses में, `set` को `list` में convert किया जाएगा।
        * generate किया गया schema बताएगा कि `set` values unique हैं (JSON Schema के `uniqueItems` का उपयोग करते हुए)।
* `bytes`:
    * Standard Python `bytes`.
    * requests और responses में इसे `str` की तरह माना जाएगा।
    * generate किया गया schema बताएगा कि यह `binary` "format" वाला `str` है।
* `Decimal`:
    * Standard Python `Decimal`.
    * requests और responses में, इसे `float` जैसा ही handle किया जाएगा।
* आप सभी valid Pydantic data types यहाँ देख सकते हैं: [Pydantic data types](https://docs.pydantic.dev/latest/usage/types/types/).

## उदाहरण { #example }

यहाँ ऊपर दिए गए कुछ types का उपयोग करते हुए parameters वाला एक उदाहरण *path operation* है।

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[1,3,12:16] *}

ध्यान दें कि function के अंदर parameters के अपने natural data type होते हैं, और उदाहरण के लिए, आप सामान्य date manipulations कर सकते हैं, जैसे:

{* ../../docs_src/extra_data_types/tutorial001_an_py310.py hl[18:19] *}
