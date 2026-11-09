# Response Status Code { #response-status-code }

যেভাবে একটি response model specify করা যায়, ঠিক সেভাবেই যেকোনো *path operation*-এ `status_code` parameter দিয়ে response-এর HTTP status code declare করতে পারেন:

* `@app.get()`
* `@app.post()`
* `@app.put()`
* `@app.delete()`
* ইত্যাদি।

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

/// note | Note

খেয়াল করুন, `status_code` হলো "decorator" method-এর (`get`, `post`, ইত্যাদি) একটি parameter। সব parameters আর body-র মতো আপনার *path operation function*-এর নয়।

///

`status_code` parameter HTTP status code-এর একটি সংখ্যা নেয়।

/// note | Note

`status_code` বিকল্প হিসেবে একটি `IntEnum`-ও নিতে পারে, যেমন Python-এর [`http.HTTPStatus`](https://docs.python.org/3/library/http.html#http.HTTPStatus)।

///

এটা:

* response-এ ওই status code return করবে।
* OpenAPI schema-তে (আর তাই user interfaces-এও) সেভাবেই document করবে:

<img src="/img/tutorial/response-status-code/image01.png">

/// note | Note

কিছু response codes (পরের section দেখুন) বোঝায় যে response-এ কোনো body নেই।

FastAPI এটা জানে, আর এমন OpenAPI docs বানাবে যেখানে লেখা থাকবে যে কোনো response body নেই।

///

## HTTP status codes সম্পর্কে { #about-http-status-codes }

/// note | Note

HTTP status codes কী, সেটা আগে থেকেই জানলে পরের section-এ চলে যান।

///

HTTP-তে response-এর অংশ হিসেবে 3 অঙ্কের একটি numeric status code পাঠানো হয়।

চেনার সুবিধার জন্য এই status codes-এর একটি করে নাম আছে, কিন্তু আসল জিনিস হলো সংখ্যাটা।

সংক্ষেপে:

* `100 - 199` হলো "Information"-এর জন্য। এগুলো সরাসরি খুব কমই ব্যবহার করবেন। এই status codes-এর responses-এ body থাকতে পারে না।
* **`200 - 299`** হলো "Successful" responses-এর জন্য। এগুলোই আপনি সবচেয়ে বেশি ব্যবহার করবেন।
    * `200` হলো default status code, মানে সবকিছু "OK" ছিল।
    * আরেকটি উদাহরণ `201`, "Created"। database-এ নতুন record বানানোর পর সাধারণত এটা ব্যবহার হয়।
    * একটি বিশেষ case হলো `204`, "No Content"। client-কে return করার মতো কোনো content না থাকলে এই response ব্যবহার হয়, তাই এই response-এ body থাকা চলবে না।
* **`300 - 399`** হলো "Redirection"-এর জন্য। এই status codes-এর responses-এ body থাকতেও পারে, না-ও থাকতে পারে, শুধু `304`, "Not Modified" ছাড়া, যেটাতে body থাকা চলবে না।
* **`400 - 499`** হলো "Client error" responses-এর জন্য। সম্ভবত এগুলোই আপনি দ্বিতীয় সবচেয়ে বেশি ব্যবহার করবেন।
    * একটি উদাহরণ `404`, "Not Found" response-এর জন্য।
    * client-এর সাধারণ errors-এর জন্য শুধু `400` ব্যবহার করতে পারেন।
* `500 - 599` হলো server errors-এর জন্য। এগুলো সরাসরি প্রায় কখনোই ব্যবহার করবেন না। আপনার application code বা server-এর কোনো অংশে কিছু ভুল হলে, এটা নিজে থেকেই এগুলোর কোনো একটি status code return করবে।

/// tip | Tip

প্রতিটি status code সম্পর্কে আরও জানতে আর কোন code কীসের জন্য, সেটা দেখতে [HTTP status codes নিয়ে <abbr title="Mozilla Developer Network">MDN</abbr> documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) দেখুন।

///

## নামগুলো মনে রাখার shortcut { #shortcut-to-remember-the-names }

আগের উদাহরণটা আবার দেখা যাক:

{* ../../docs_src/response_status_code/tutorial001_py310.py hl[6] *}

`201` হলো "Created"-এর status code।

কিন্তু এই codes-এর প্রতিটার মানে মুখস্থ করার দরকার নেই।

`fastapi.status` থেকে সুবিধাজনক variables ব্যবহার করতে পারেন।

{* ../../docs_src/response_status_code/tutorial002_py310.py hl[1,6] *}

এগুলো শুধু সুবিধার জন্য, এগুলোতে একই সংখ্যা থাকে, কিন্তু এভাবে editor-এর autocomplete দিয়ে খুঁজে নিতে পারবেন:

<img src="/img/tutorial/response-status-code/image02.png">

/// note | Technical Details

`from starlette import status`-ও ব্যবহার করতে পারেন।

**FastAPI** একই `starlette.status`-কে `fastapi.status` হিসেবে দেয়, শুধু আপনার, মানে developer-এর সুবিধার জন্য। কিন্তু এটা সরাসরি Starlette থেকে আসে।

///

## Default বদলানো { #changing-the-default }

পরে [Advanced User Guide](../advanced/response-change-status-code.md)-এ দেখবেন, এখানে declare করা default ছাড়া অন্য status code কীভাবে return করতে হয়।
