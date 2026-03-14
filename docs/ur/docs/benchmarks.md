# Benchmarks { #benchmarks }

آزاد TechEmpower benchmarks ظاہر کرتے ہیں کہ Uvicorn کے تحت چلنے والی **FastAPI** applications [دستیاب تیز ترین Python frameworks میں سے ایک](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7) ہیں، صرف Starlette اور Uvicorn سے پیچھے (جو FastAPI اندرونی طور پر استعمال کرتا ہے)۔

لیکن benchmarks اور موازنے دیکھتے وقت آپ کو درج ذیل باتیں ذہن میں رکھنی چاہئیں۔

## Benchmarks اور رفتار { #benchmarks-and-speed }

جب آپ benchmarks دیکھتے ہیں، تو عام طور پر مختلف اقسام کے کئی tools کو مساوی کے طور پر موازنہ کیا جاتا ہے۔

خاص طور پر، Uvicorn، Starlette اور FastAPI کو ایک ساتھ (بہت سے دوسرے tools کے درمیان) موازنے میں دیکھنا۔

tool جتنا آسان مسئلہ حل کرتا ہے، اتنی بہتر performance دیتا ہے۔ اور زیادہ تر benchmarks tool کی فراہم کردہ اضافی features کو ٹیسٹ نہیں کرتے۔

درجہ بندی اس طرح ہے:

* **Uvicorn**: ایک ASGI server
    * **Starlette**: (Uvicorn استعمال کرتا ہے) ایک web microframework
        * **FastAPI**: (Starlette استعمال کرتا ہے) ایک API microframework جس میں APIs بنانے کے لیے کئی اضافی features ہیں، data validation وغیرہ کے ساتھ۔

* **Uvicorn**:
    * سب سے بہترین performance ہوگی، کیونکہ server کے علاوہ اس میں زیادہ اضافی code نہیں ہے۔
    * آپ براہ راست Uvicorn میں application نہیں لکھیں گے۔ اس کا مطلب ہوگا کہ آپ کے code میں کم از کم وہ سارا code شامل ہو جو Starlette (یا **FastAPI**) فراہم کرتا ہے۔ اور اگر آپ ایسا کریں، تو آپ کی حتمی application میں بھی وہی overhead ہوگا جیسا framework استعمال کرنے اور app code اور bugs کو کم سے کم رکھنے میں ہوتا۔
    * اگر آپ Uvicorn کا موازنہ کر رہے ہیں، تو اسے Daphne، Hypercorn، uWSGI وغیرہ سے موازنہ کریں۔ Application servers۔
* **Starlette**:
    * Uvicorn کے بعد اگلی بہترین performance ہوگی۔ درحقیقت، Starlette چلنے کے لیے Uvicorn استعمال کرتا ہے۔ تو یہ شاید صرف مزید code execute کرنے کی وجہ سے Uvicorn سے "سست" ہو سکتا ہے۔
    * لیکن یہ آپ کو سادہ web applications بنانے کے tools فراہم کرتا ہے، paths پر مبنی routing وغیرہ کے ساتھ۔
    * اگر آپ Starlette کا موازنہ کر رہے ہیں، تو اسے Sanic، Flask، Django وغیرہ سے موازنہ کریں۔ Web frameworks (یا microframeworks)۔
* **FastAPI**:
    * جس طرح Starlette، Uvicorn استعمال کرتا ہے اور اس سے تیز نہیں ہو سکتا، **FastAPI** Starlette استعمال کرتا ہے، تو یہ اس سے تیز نہیں ہو سکتا۔
    * FastAPI، Starlette کے اوپر مزید features فراہم کرتا ہے۔ وہ features جن کی آپ کو APIs بناتے وقت تقریباً ہمیشہ ضرورت ہوتی ہے، جیسے data validation اور serialization۔ اور اسے استعمال کرنے سے آپ کو خودکار documentation مفت میں ملتی ہے (خودکار documentation چلتی applications میں overhead بھی نہیں ڈالتی، یہ startup پر generate ہوتی ہے)۔
    * اگر آپ نے FastAPI استعمال نہ کیا ہوتا اور براہ راست Starlette (یا کوئی اور tool جیسے Sanic، Flask، Responder وغیرہ) استعمال کیا ہوتا تو آپ کو ساری data validation اور serialization خود implement کرنی ہوتی۔ تو آپ کی حتمی application میں پھر بھی وہی overhead ہوتا جیسا FastAPI استعمال کرنے میں ہوتا۔ اور بہت سے معاملات میں، یہ data validation اور serialization applications میں لکھے جانے والے code کا سب سے بڑا حصہ ہوتی ہے۔
    * تو FastAPI استعمال کرکے آپ development time، bugs، code کی لائنیں بچا رہے ہیں، اور شاید آپ کو وہی performance (یا بہتر) ملے گی جو آپ کو اسے استعمال نہ کرنے پر ملتی (کیونکہ آپ کو یہ سب اپنے code میں implement کرنا ہوتا)۔
    * اگر آپ FastAPI کا موازنہ کر رہے ہیں، تو اسے کسی web application framework (یا tools کے مجموعے) سے موازنہ کریں جو data validation، serialization اور documentation فراہم کرتا ہو، جیسے Flask-apispec، NestJS، Molten وغیرہ۔ وہ frameworks جن میں مربوط خودکار data validation، serialization اور documentation شامل ہو۔
