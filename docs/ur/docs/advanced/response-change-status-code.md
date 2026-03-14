# Response - Status Code تبدیل کریں { #response-change-status-code }

آپ نے شاید پہلے پڑھا ہوگا کہ آپ پہلے سے طے شدہ [Response Status Code](../tutorial/response-status-code.md) مقرر کر سکتے ہیں۔

لیکن بعض صورتوں میں آپ کو پہلے سے طے شدہ status code سے مختلف status code واپس کرنے کی ضرورت ہوتی ہے۔

## استعمال کی صورت { #use-case }

مثال کے طور پر، تصور کریں کہ آپ پہلے سے طے شدہ طور پر HTTP status code "OK" `200` واپس کرنا چاہتے ہیں۔

لیکن اگر ڈیٹا موجود نہیں تھا، تو آپ اسے بنانا چاہتے ہیں، اور HTTP status code "CREATED" `201` واپس کرنا چاہتے ہیں۔

لیکن آپ پھر بھی `response_model` کے ساتھ واپس کیے گئے ڈیٹا کو فلٹر اور تبدیل کرنے کے قابل رہنا چاہتے ہیں۔

ان صورتوں میں، آپ `Response` parameter استعمال کر سکتے ہیں۔

## `Response` parameter استعمال کریں { #use-a-response-parameter }

آپ اپنے *path operation function* میں `Response` قسم کا parameter اعلان کر سکتے ہیں (جیسا کہ آپ cookies اور headers کے لیے کر سکتے ہیں)۔

اور پھر آپ اس *عارضی* response آبجیکٹ میں `status_code` مقرر کر سکتے ہیں۔

{* ../../docs_src/response_change_status_code/tutorial001_py310.py hl[1,9,12] *}

اور پھر آپ جیسے عام طور پر کرتے ہیں، کوئی بھی آبجیکٹ واپس کر سکتے ہیں (ایک `dict`، database model وغیرہ)۔

اور اگر آپ نے `response_model` کا اعلان کیا ہے، تو اسے پھر بھی آپ کے واپس کردہ آبجیکٹ کو فلٹر اور تبدیل کرنے کے لیے استعمال کیا جائے گا۔

**FastAPI** اس *عارضی* response کو status code (نیز cookies اور headers) نکالنے کے لیے استعمال کرے گا، اور انہیں حتمی response میں ڈالے گا جس میں آپ کی واپس کردہ قدر ہوگی، کسی بھی `response_model` سے فلٹر شدہ۔

آپ dependencies میں بھی `Response` parameter کا اعلان کر سکتے ہیں، اور ان میں status code مقرر کر سکتے ہیں۔ لیکن ذہن میں رکھیں کہ آخری مقرر کیا گیا غالب آئے گا۔
