# Background Tasks { #background-tasks }

آپ background tasks define کر سکتے ہیں جو response واپس بھیجنے کے *بعد* چلائے جائیں۔

یہ ان operations کے لیے مفید ہے جو request کے بعد ہونے چاہئیں، لیکن client کو response وصول کرنے سے پہلے ان کے مکمل ہونے کا انتظار کرنے کی ضرورت نہیں ہے۔

اس میں مثال کے طور پر شامل ہیں:

* کوئی عمل انجام دینے کے بعد بھیجی جانے والی email notifications:
    * چونکہ email server سے connect ہونا اور email بھیجنا "سست" ہوتا ہے (کئی سیکنڈز)، آپ فوری طور پر response واپس بھیج سکتے ہیں اور email notification background میں بھیج سکتے ہیں۔
* Data کی processing:
    * مثال کے طور پر، فرض کریں آپ کو ایک فائل ملتی ہے جسے سست process سے گزرنا ہے، آپ "Accepted" (HTTP 202) کا response واپس بھیج سکتے ہیں اور فائل کو background میں process کر سکتے ہیں۔

## `BackgroundTasks` استعمال کرنا { #using-backgroundtasks }

سب سے پہلے، `BackgroundTasks` import کریں اور اپنے *path operation function* میں `BackgroundTasks` کی type declaration کے ساتھ ایک parameter define کریں:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[1,13] *}

**FastAPI** آپ کے لیے `BackgroundTasks` قسم کا object بنائے گا اور اسے اس parameter کے طور پر منتقل کرے گا۔

## ایک task function بنائیں { #create-a-task-function }

background task کے طور پر چلایا جانے والا function بنائیں۔

یہ ایک عام function ہے جو parameters وصول کر سکتا ہے۔

یہ `async def` یا عام `def` function ہو سکتا ہے، **FastAPI** اسے درست طریقے سے handle کرنا جانتا ہے۔

اس صورت میں، task function ایک فائل میں لکھے گا (email بھیجنے کی نقل)۔

اور چونکہ write operation `async` اور `await` استعمال نہیں کرتا، ہم function کو عام `def` سے define کرتے ہیں:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[6:9] *}

## Background task شامل کریں { #add-the-background-task }

اپنے *path operation function* کے اندر، اپنا task function `.add_task()` method کے ذریعے *background tasks* object کو دیں:

{* ../../docs_src/background_tasks/tutorial001_py310.py hl[14] *}

`.add_task()` arguments کے طور پر وصول کرتا ہے:

* background میں چلایا جانے والا task function (`write_notification`)۔
* task function کو ترتیب سے منتقل کیے جانے والے arguments کی کوئی بھی sequence (`email`)۔
* task function کو منتقل کیے جانے والے کوئی بھی keyword arguments (`message="some notification"`)۔

## Dependency Injection { #dependency-injection }

`BackgroundTasks` کا استعمال dependency injection system کے ساتھ بھی کام کرتا ہے، آپ متعدد سطحوں پر `BackgroundTasks` قسم کا parameter declare کر سکتے ہیں: *path operation function* میں، dependency (dependable) میں، sub-dependency میں، وغیرہ۔

**FastAPI** جانتا ہے کہ ہر صورت میں کیا کرنا ہے اور ایک ہی object کو دوبارہ استعمال کرنا ہے، تاکہ تمام background tasks آپس میں مل جائیں اور بعد میں background میں چلائے جائیں:

{* ../../docs_src/background_tasks/tutorial002_an_py310.py hl[13,15,22,25] *}

اس مثال میں، پیغامات `log.txt` فائل میں response بھیجنے کے *بعد* لکھے جائیں گے۔

اگر request میں کوئی query تھی، تو اسے background task میں log میں لکھا جائے گا۔

اور پھر *path operation function* میں بنایا گیا ایک اور background task `email` path parameter استعمال کرتے ہوئے ایک پیغام لکھے گا۔

## تکنیکی تفصیلات { #technical-details }

`BackgroundTasks` class براہ راست [`starlette.background`](https://www.starlette.dev/background/) سے آتی ہے۔

اسے FastAPI میں براہ راست import/شامل کیا گیا ہے تاکہ آپ اسے `fastapi` سے import کر سکیں اور غلطی سے `starlette.background` سے متبادل `BackgroundTask` (آخر میں `s` کے بغیر) import کرنے سے بچ سکیں۔

صرف `BackgroundTasks` (نہ کہ `BackgroundTask`) استعمال کر کے، اسے *path operation function* parameter کے طور پر استعمال کرنا ممکن ہو جاتا ہے اور **FastAPI** باقی کام خود سنبھال لیتا ہے، بالکل اسی طرح جیسے `Request` object کو براہ راست استعمال کرتے وقت۔

FastAPI میں اکیلے `BackgroundTask` استعمال کرنا بھی ممکن ہے، لیکن آپ کو اپنے code میں object بنانا ہوگا اور اسے شامل کرتے ہوئے Starlette `Response` واپس کرنا ہوگا۔

آپ [Starlette کی Background Tasks کی سرکاری دستاویزات](https://www.starlette.dev/background/) میں مزید تفصیلات دیکھ سکتے ہیں۔

## احتیاط { #caveat }

اگر آپ کو بھاری background computation کرنے کی ضرورت ہے اور آپ کو لازمی طور پر اسی process سے چلانے کی ضرورت نہیں ہے (مثلاً، آپ کو memory، variables وغیرہ share کرنے کی ضرورت نہیں)، تو آپ کو [Celery](https://docs.celeryq.dev) جیسے بڑے tools استعمال کرنے سے فائدہ ہو سکتا ہے۔

ان میں عام طور پر زیادہ پیچیدہ configurations، message/job queue manager، جیسے RabbitMQ یا Redis کی ضرورت ہوتی ہے، لیکن یہ آپ کو background tasks کو متعدد processes میں، اور خاص طور پر، متعدد servers میں چلانے کی اجازت دیتے ہیں۔

لیکن اگر آپ کو اسی **FastAPI** app سے variables اور objects تک رسائی حاصل کرنے کی ضرورت ہے، یا آپ کو چھوٹے background tasks (جیسے email notification بھیجنا) انجام دینے کی ضرورت ہے، تو آپ آسانی سے `BackgroundTasks` استعمال کر سکتے ہیں۔

## خلاصہ { #recap }

Background tasks شامل کرنے کے لیے *path operation functions* اور dependencies میں parameters کے ساتھ `BackgroundTasks` import اور استعمال کریں۔
