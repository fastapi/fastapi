# موجودہ صارف حاصل کریں { #get-current-user }

پچھلے باب میں security system (جو dependency injection system پر مبنی ہے) *path operation function* کو `token` بطور `str` دے رہا تھا:

{* ../../docs_src/security/tutorial001_an_py310.py hl[12] *}

لیکن یہ ابھی تک اتنا کارآمد نہیں ہے۔

آئیے اسے ہمیں موجودہ صارف دینے کے قابل بنائیں۔

## ایک user model بنائیں { #create-a-user-model }

پہلے، آئیے ایک Pydantic user model بناتے ہیں۔

جس طرح ہم Pydantic کو bodies declare کرنے کے لیے استعمال کرتے ہیں، ہم اسے کہیں بھی استعمال کر سکتے ہیں:

{* ../../docs_src/security/tutorial002_an_py310.py hl[5,12:6] *}

## ایک `get_current_user` dependency بنائیں { #create-a-get-current-user-dependency }

آئیے ایک dependency `get_current_user` بناتے ہیں۔

یاد ہے کہ dependencies میں sub-dependencies ہو سکتی ہیں؟

`get_current_user` کے پاس وہی `oauth2_scheme` بطور dependency ہوگا جو ہم نے پہلے بنایا تھا۔

جس طرح ہم پہلے *path operation* میں براہ راست کر رہے تھے، ہماری نئی dependency `get_current_user` sub-dependency `oauth2_scheme` سے `token` بطور `str` وصول کرے گی:

{* ../../docs_src/security/tutorial002_an_py310.py hl[25] *}

## صارف حاصل کریں { #get-the-user }

`get_current_user` ایک (جعلی) utility function استعمال کرے گا جو ہم نے بنایا ہے، جو token کو `str` کے طور پر لیتا ہے اور ہمارا Pydantic `User` model واپس کرتا ہے:

{* ../../docs_src/security/tutorial002_an_py310.py hl[19:22,26:27] *}

## موجودہ صارف inject کریں { #inject-the-current-user }

تو اب ہم *path operation* میں `Depends` کے ساتھ اپنا `get_current_user` استعمال کر سکتے ہیں:

{* ../../docs_src/security/tutorial002_an_py310.py hl[31] *}

دھیان دیں کہ ہم نے `current_user` کی type Pydantic model `User` بیان کی ہے۔

یہ ہماری function کے اندر تمام completion اور type checks میں مدد کرے گا۔

/// tip | مشورہ

آپ کو یاد ہوگا کہ request bodies بھی Pydantic models کے ساتھ declare کی جاتی ہیں۔

یہاں **FastAPI** الجھے گا نہیں کیونکہ آپ `Depends` استعمال کر رہے ہیں۔

///

/// check

جس طرح یہ dependency system ڈیزائن کیا گیا ہے وہ ہمیں مختلف dependencies (مختلف "dependables") رکھنے کی اجازت دیتا ہے جو سب ایک `User` model واپس کرتی ہیں۔

ہم صرف ایک dependency تک محدود نہیں ہیں جو اس قسم کا data واپس کر سکے۔

///

## دوسرے models { #other-models }

اب آپ موجودہ صارف کو براہ راست *path operation functions* میں حاصل کر سکتے ہیں اور security کے طریقہ کار کو **Dependency Injection** کی سطح پر، `Depends` استعمال کرتے ہوئے سنبھال سکتے ہیں۔

اور آپ security کی ضروریات کے لیے کوئی بھی model یا data استعمال کر سکتے ہیں (اس معاملے میں، ایک Pydantic model `User`)۔

لیکن آپ کسی مخصوص data model، class یا type استعمال کرنے تک محدود نہیں ہیں۔

کیا آپ اپنے model میں `id` اور `email` رکھنا چاہتے ہیں اور کوئی `username` نہیں چاہتے؟ ضرور۔ آپ یہی tools استعمال کر سکتے ہیں۔

کیا آپ صرف ایک `str` چاہتے ہیں؟ یا صرف ایک `dict`؟ یا براہ راست ایک database class model instance؟ یہ سب اسی طرح کام کرتا ہے۔

آپ کے پاس حقیقت میں ایسے صارف نہیں ہیں جو آپ کی application میں login کرتے ہوں بلکہ robots، bots، یا دوسرے systems ہیں، جن کے پاس صرف ایک access token ہے؟ پھر بھی، یہ سب اسی طرح کام کرتا ہے۔

بس اپنی application کے لیے جو بھی model، class، یا database آپ کو درکار ہو استعمال کریں۔ **FastAPI** dependency injection system کے ساتھ آپ کا ساتھ دیتا ہے۔

## Code کا سائز { #code-size }

یہ مثال طویل لگ سکتی ہے۔ یاد رکھیں کہ ہم security، data models، utility functions اور *path operations* کو ایک ہی فائل میں ملا رہے ہیں۔

لیکن یہاں اہم نکتہ یہ ہے۔

Security اور dependency injection کا کام ایک بار لکھا جاتا ہے۔

اور آپ اسے جتنا پیچیدہ چاہیں بنا سکتے ہیں۔ اور پھر بھی، یہ صرف ایک بار، ایک ہی جگہ لکھا جاتا ہے۔ تمام لچک کے ساتھ۔

لیکن آپ کے پاس ہزاروں endpoints (*path operations*) ہو سکتے ہیں جو اسی security system کو استعمال کریں۔

اور ان سب (یا ان کا جو بھی حصہ آپ چاہیں) ان dependencies یا آپ کی بنائی ہوئی کسی بھی اور dependency کو دوبارہ استعمال کرنے کا فائدہ اٹھا سکتے ہیں۔

اور یہ سب ہزاروں *path operations* صرف 3 لائنوں جتنی چھوٹی ہو سکتی ہیں:

{* ../../docs_src/security/tutorial002_an_py310.py hl[30:32] *}

## خلاصہ { #recap }

اب آپ موجودہ صارف کو براہ راست اپنی *path operation function* میں حاصل کر سکتے ہیں۔

ہم پہلے سے آدھے راستے پر ہیں۔

ہمیں بس ایک *path operation* شامل کرنے کی ضرورت ہے تاکہ صارف/client حقیقت میں `username` اور `password` بھیج سکے۔

یہ اگلے باب میں آتا ہے۔
