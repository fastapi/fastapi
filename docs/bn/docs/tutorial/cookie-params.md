# Cookie Parameters { #cookie-parameters }

`Query` আর `Path` parameters যেভাবে define করেন, Cookie parameters-ও সেভাবেই define করতে পারেন।

## `Cookie` import করুন { #import-cookie }

প্রথমে `Cookie` import করুন:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[3] *}

## `Cookie` parameters declare করুন { #declare-cookie-parameters }

তারপর `Path` আর `Query`-এর মতো একই গঠনে cookie parameters declare করুন।

default value আর সব বাড়তি validation বা annotation parameters define করতে পারেন:

{* ../../docs_src/cookie_params/tutorial001_an_py310.py hl[9] *}

/// note | Technical Details

`Cookie` হলো `Path` আর `Query`-এর একটি "বোন" class। এটাও একই common `Param` class থেকে inherit করে।

কিন্তু মনে রাখবেন, `fastapi` থেকে `Query`, `Path`, `Cookie` আর অন্যগুলো import করলে, সেগুলো আসলে functions, যেগুলো special classes return করে।

///

/// note | Note

cookies declare করতে `Cookie` ব্যবহার করতে হবে, না হলে parameters query parameters হিসেবে ধরা হবে।

///

/// note | Note

মনে রাখবেন, যেহেতু **browsers cookies handle করে** বিশেষভাবে আর আড়ালে, তাই এরা **JavaScript**-কে সহজে এগুলো ছুঁতে **দেয় না**।

`/docs`-এ **API docs UI**-তে গেলে আপনার *path operations*-এর cookies-এর **documentation** দেখতে পাবেন।

কিন্তু **data পূরণ করে** "Execute" click করলেও, যেহেতু docs UI **JavaScript** দিয়ে কাজ করে, তাই cookies পাঠানো হবে না, আর এমন একটি **error** message দেখবেন যেন আপনি কোনো values লেখেনইনি।

///

## Recap { #recap }

`Query` আর `Path`-এর মতো একই common pattern মেনে `Cookie` দিয়ে cookies declare করুন।
