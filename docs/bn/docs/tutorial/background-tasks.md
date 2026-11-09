# Background Tasks { #background-tasks }

response return করার *পরে* চালানোর জন্য background tasks define করতে পারেন।

এটা সেই operations-এর জন্য কাজে লাগে যেগুলো request-এর পরে হওয়া দরকার, কিন্তু response পাওয়ার আগে operation শেষ হওয়া পর্যন্ত client-কে আসলে অপেক্ষা করতে হয় না।

যেমন:

* কোনো কাজ করার পর পাঠানো email notifications:
    * যেহেতু email server-এ connect করে email পাঠাতে সাধারণত "সময় লাগে" (কয়েক সেকেন্ড), তাই সাথে সাথেই response return করে background-এ email notification পাঠাতে পারেন।
* Data processing:
    * যেমন, ধরুন আপনি একটি file পেলেন যেটাকে একটি ধীর process-এর মধ্য দিয়ে যেতে হবে, তাহলে "Accepted" (HTTP 202) response return করে file-টা background-এ process করতে পারেন।

## `BackgroundTasks` ব্যবহার করা { #using-backgroundtasks }

প্রথমে `BackgroundTasks` import করুন, আর আপনার *path operation function*-এ `BackgroundTasks` type declaration-সহ একটি parameter define করুন:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** আপনার জন্য `BackgroundTasks` type-এর object বানিয়ে ওই parameter হিসেবে দিয়ে দেবে।

## একটি task function বানান { #create-a-task-function }

background task হিসেবে চালানোর জন্য একটি function বানান।

এটা শুধু একটি standard function, যেটা parameters নিতে পারে।

এটা `async def` বা সাধারণ `def` function হতে পারে, **FastAPI** জানবে কীভাবে ঠিকমতো handle করতে হয়।

এখানে task function একটি file-এ লিখবে (email পাঠানোর মতো করে দেখানোর জন্য)।

আর যেহেতু write operation `async` আর `await` ব্যবহার করে না, তাই function-টা সাধারণ `def` দিয়ে define করা হয়েছে:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## Background task যোগ করুন { #add-the-background-task }

আপনার *path operation function*-এর ভেতরে, `.add_task()` method দিয়ে আপনার task function *background tasks* object-এ দিয়ে দিন:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` arguments হিসেবে নেয়:

* background-এ চালানোর জন্য একটি task function (`write_notification`)।
* task function-এ ক্রম অনুযায়ী যে arguments পাঠাতে হবে, সেগুলো (`email`)।
* task function-এ যে keyword arguments পাঠাতে হবে, সেগুলো (`message="some notification"`)।

## Dependency Injection { #dependency-injection }

`BackgroundTasks` dependency injection system-এর সাথেও কাজ করে, বিভিন্ন level-এ `BackgroundTasks` type-এর parameter declare করতে পারেন: একটি *path operation function*-এ, একটি dependency (dependable)-তে, একটি sub-dependency-তে, ইত্যাদি।

**FastAPI** জানে প্রতিটি ক্ষেত্রে কী করতে হবে আর কীভাবে একই object আবার ব্যবহার করতে হবে, যাতে সব background tasks একসাথে মিলিয়ে পরে background-এ চালানো যায়:


{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}


এই উদাহরণে messages-গুলো response পাঠানোর *পরে* `log.txt` file-এ লেখা হবে।

request-এ কোনো query থাকলে, সেটা একটি background task-এ log-এ লেখা হবে।

তারপর *path operation function*-এ তৈরি হওয়া আরেকটি background task `email` path parameter ব্যবহার করে একটি message লিখবে।

## Technical Details { #technical-details }

`BackgroundTasks` class সরাসরি [`starlette.background`](https://starlette.dev/background/) থেকে আসে।

এটা সরাসরি FastAPI-তে import/include করা, যাতে এটা `fastapi` থেকে import করতে পারেন, আর ভুল করে `starlette.background` থেকে বিকল্প `BackgroundTask` (শেষে `s` ছাড়া) import না হয়ে যায়।

শুধু `BackgroundTasks` ব্যবহার করলে (`BackgroundTask` নয়), এটা একটি *path operation function* parameter হিসেবে ব্যবহার করা যায়, আর বাকিটা **FastAPI** নিজেই handle করে, ঠিক যেমন সরাসরি `Request` object ব্যবহার করার সময় হয়।

FastAPI-তে শুধু `BackgroundTask`-ও ব্যবহার করা যায়, কিন্তু তখন object-টা আপনার code-এ বানিয়ে, সেটা সহ একটি Starlette `Response` return করতে হবে।

আরও বিস্তারিত দেখতে পারেন [Background Tasks নিয়ে Starlette-এর official docs](https://starlette.dev/background/)-এ।

## সতর্কতা { #caveat }

আপনার যদি ভারী background computation করতে হয়, আর সেটা একই process-এ চালানো জরুরি না হয় (যেমন memory, variables, ইত্যাদি share করার দরকার নেই), তাহলে [Celery](https://docs.celeryq.dev)-এর মতো অন্য বড় tools ব্যবহার করে লাভ হতে পারে।

এগুলোর জন্য সাধারণত আরও জটিল configuration লাগে, RabbitMQ বা Redis-এর মতো একটি message/job queue manager লাগে, কিন্তু এগুলো দিয়ে একাধিক processes-এ, বিশেষ করে একাধিক servers-এ background tasks চালানো যায়।

কিন্তু একই **FastAPI** app-এর variables আর objects access করার দরকার হলে, বা ছোট background tasks (যেমন একটি email notification পাঠানো) করতে হলে, সোজা `BackgroundTasks` ব্যবহার করলেই হবে।

## Recap { #recap }

background tasks যোগ করতে *path operation functions* আর dependencies-এ parameters দিয়ে `BackgroundTasks` import করে ব্যবহার করুন।
