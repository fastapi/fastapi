# Benchmarks { #benchmarks }

নিরপেক্ষ TechEmpower benchmarks দেখায়, Uvicorn-এ চলা **FastAPI** applications [সবচেয়ে দ্রুত Python framework-গুলোর একটি](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7), শুধু Starlette আর Uvicorn-এর পরেই (যেগুলো FastAPI নিজেই ভেতরে ব্যবহার করে)।

কিন্তু benchmarks আর comparisons দেখার সময় নিচের বিষয়গুলো মাথায় রাখা উচিত।

## Benchmarks আর speed { #benchmarks-and-speed }

benchmarks দেখলে প্রায়ই দেখবেন বিভিন্ন ধরনের কয়েকটা tools-কে সমান ধরে তুলনা করা হচ্ছে।

বিশেষ করে Uvicorn, Starlette আর FastAPI-কে একসাথে তুলনা করা হচ্ছে (আরও অনেক tools-এর মধ্যে)।

tool যত সহজ সমস্যা সমাধান করে, তত ভালো performance পায়। আর বেশিরভাগ benchmarks tool-এর দেওয়া বাড়তি features test করে না।

hierarchy-টা এরকম:

* **Uvicorn**: একটি ASGI server
    * **Starlette**: (Uvicorn ব্যবহার করে) একটি web microframework
        * **FastAPI**: (Starlette ব্যবহার করে) APIs বানানোর জন্য কয়েকটা বাড়তি features-সহ একটি API microframework, data validation, ইত্যাদি সহ।

* **Uvicorn**:
    * সবচেয়ে ভালো performance পাবে, কারণ server ছাড়া এতে খুব বেশি বাড়তি code নেই।
    * সরাসরি Uvicorn-এ application লিখবেন না। তার মানে আপনার code-এ কমবেশি অন্তত Starlette (বা **FastAPI**)-এর দেওয়া সব code রাখতে হবে। আর সেটা করলে, আপনার final application-এর overhead একটি framework ব্যবহার করে app code আর bugs কমানোর মতোই হবে।
    * Uvicorn-কে তুলনা করলে Daphne, Hypercorn, uWSGI, ইত্যাদির সাথে তুলনা করুন। Application servers।
* **Starlette**:
    * Uvicorn-এর পরেই সবচেয়ে ভালো performance পাবে। আসলে Starlette চলার জন্য Uvicorn ব্যবহার করে। তাই সম্ভবত বেশি code চালাতে হয় বলে এটা শুধু Uvicorn-এর চেয়ে "ধীর" হতে পারে।
    * কিন্তু এটা আপনাকে সহজ web applications বানানোর tools দেয়, paths-ভিত্তিক routing, ইত্যাদি সহ।
    * Starlette-কে তুলনা করলে Sanic, Flask, Django, ইত্যাদির সাথে তুলনা করুন। Web frameworks (বা microframeworks)।
* **FastAPI**:
    * যেভাবে Starlette Uvicorn ব্যবহার করে আর এর চেয়ে দ্রুত হতে পারে না, সেভাবেই **FastAPI** Starlette ব্যবহার করে, তাই এর চেয়ে দ্রুত হতে পারে না।
    * FastAPI, Starlette-এর উপরে আরও features দেয়। এমন features যেগুলো APIs বানানোর সময় প্রায় সবসময়ই লাগে, যেমন data validation আর serialization। আর এটা ব্যবহার করলে automatic documentation বিনামূল্যে পান (automatic documentation চলমান applications-এ কোনো overhead-ও যোগ করে না, এটা startup-এ generate হয়)।
    * FastAPI ব্যবহার না করে সরাসরি Starlette (বা অন্য কোনো tool, যেমন Sanic, Flask, Responder, ইত্যাদি) ব্যবহার করলে, সব data validation আর serialization নিজেকেই implement করতে হতো। তাই আপনার final application-এর overhead FastAPI দিয়ে বানানোর মতোই থাকত। আর অনেক ক্ষেত্রে applications-এ লেখা code-এর সবচেয়ে বড় অংশই এই data validation আর serialization।
    * তাই FastAPI ব্যবহার করে আপনি development time, bugs, lines of code বাঁচাচ্ছেন, আর সম্ভবত এটা ব্যবহার না করলে যে performance পেতেন সেটাই (বা আরও ভালো) পাবেন (কারণ তখন সব আপনার code-এ implement করতে হতো)।
    * FastAPI-কে তুলনা করলে এমন একটি web application framework (বা tools-এর সেট)-এর সাথে তুলনা করুন যেটা data validation, serialization আর documentation দেয়, যেমন Flask-apispec, NestJS, Molten, ইত্যাদি। integrated automatic data validation, serialization আর documentation-সহ Frameworks।
