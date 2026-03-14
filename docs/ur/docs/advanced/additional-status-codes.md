# اضافی Status Codes { #additional-status-codes }

پہلے سے طے شدہ طور پر، **FastAPI** responses کو `JSONResponse` استعمال کر کے واپس کرے گا، آپ کے *path operation* سے واپس آنے والے مواد کو اس `JSONResponse` میں ڈال کر۔

یہ پہلے سے طے شدہ status code یا وہ استعمال کرے گا جو آپ نے اپنے *path operation* میں مقرر کیا ہے۔

## اضافی status codes { #additional-status-codes_1 }

اگر آپ بنیادی status code کے علاوہ اضافی status codes واپس کرنا چاہتے ہیں، تو آپ براہ راست `Response` واپس کر کے ایسا کر سکتے ہیں، جیسے `JSONResponse`، اور اضافی status code براہ راست مقرر کر سکتے ہیں۔

مثال کے طور پر، فرض کریں کہ آپ ایک *path operation* چاہتے ہیں جو آئٹمز کو اپ ڈیٹ کرنے کی اجازت دے، اور کامیاب ہونے پر HTTP status code 200 "OK" واپس کرے۔

لیکن آپ یہ بھی چاہتے ہیں کہ یہ نئے آئٹمز قبول کرے۔ اور جب آئٹمز پہلے سے موجود نہیں تھے، تو یہ انہیں بنائے اور HTTP status code 201 "Created" واپس کرے۔

اس کے لیے، `JSONResponse` import کریں، اور اپنا مواد وہاں براہ راست واپس کریں، جو `status_code` آپ چاہتے ہیں وہ مقرر کرتے ہوئے:

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning | انتباہ

جب آپ براہ راست `Response` واپس کرتے ہیں، جیسا کہ اوپر کی مثال میں، تو یہ براہ راست واپس کیا جائے گا۔

اسے model وغیرہ کے ساتھ serialize نہیں کیا جائے گا۔

یقینی بنائیں کہ اس میں وہ ڈیٹا ہے جو آپ چاہتے ہیں، اور قدریں درست JSON ہیں (اگر آپ `JSONResponse` استعمال کر رہے ہیں)۔

///

/// note | تکنیکی تفصیلات

آپ `from starlette.responses import JSONResponse` بھی استعمال کر سکتے ہیں۔

**FastAPI** وہی `starlette.responses` فراہم کرتا ہے جو `fastapi.responses` کے طور پر، بس آپ یعنی developer کی سہولت کے لیے۔ لیکن زیادہ تر دستیاب responses براہ راست Starlette سے آتے ہیں۔ `status` کے ساتھ بھی یہی ہے۔

///

## OpenAPI اور API docs { #openapi-and-api-docs }

اگر آپ اضافی status codes اور responses براہ راست واپس کرتے ہیں، تو وہ OpenAPI schema (API docs) میں شامل نہیں ہوں گے، کیونکہ FastAPI کے پاس پہلے سے یہ جاننے کا کوئی طریقہ نہیں ہے کہ آپ کیا واپس کرنے والے ہیں۔

لیکن آپ اپنے کوڈ میں اسے دستاویزی شکل دے سکتے ہیں، استعمال کرتے ہوئے: [OpenAPI میں اضافی Responses](additional-responses.md)۔
