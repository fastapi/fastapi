# Swagger UI کی ترتیب { #configure-swagger-ui }

آپ کچھ اضافی [Swagger UI parameters](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) ترتیب دے سکتے ہیں۔

انہیں ترتیب دینے کے لیے، `FastAPI()` app object بناتے وقت یا `get_swagger_ui_html()` function میں `swagger_ui_parameters` argument پاس کریں۔

`swagger_ui_parameters` ایک dictionary قبول کرتا ہے جس میں ترتیبات براہ راست Swagger UI کو بھیجی جاتی ہیں۔

FastAPI ترتیبات کو **JSON** میں تبدیل کرتا ہے تاکہ وہ JavaScript کے ساتھ ہم آہنگ ہوں، کیونکہ Swagger UI کو اسی کی ضرورت ہوتی ہے۔

## Syntax Highlighting غیر فعال کریں { #disable-syntax-highlighting }

مثال کے طور پر، آپ Swagger UI میں syntax highlighting غیر فعال کر سکتے ہیں۔

Settings تبدیل کیے بغیر، syntax highlighting بطور default فعال ہوتی ہے:

<img src="/img/tutorial/extending-openapi/image02.png">

لیکن آپ `syntaxHighlight` کو `False` سیٹ کر کے اسے غیر فعال کر سکتے ہیں:

{* ../../docs_src/configure_swagger_ui/tutorial001_py310.py hl[3] *}

...اور پھر Swagger UI مزید syntax highlighting نہیں دکھائے گا:

<img src="/img/tutorial/extending-openapi/image03.png">

## Theme تبدیل کریں { #change-the-theme }

اسی طرح آپ `"syntaxHighlight.theme"` key کے ساتھ syntax highlighting theme سیٹ کر سکتے ہیں (نوٹ کریں کہ اس میں درمیان میں ایک dot ہے):

{* ../../docs_src/configure_swagger_ui/tutorial002_py310.py hl[3] *}

یہ ترتیب syntax highlighting کی رنگ theme تبدیل کرے گی:

<img src="/img/tutorial/extending-openapi/image04.png">

## Default Swagger UI Parameters تبدیل کریں { #change-default-swagger-ui-parameters }

FastAPI میں زیادہ تر استعمال کے معاملات کے لیے کچھ default ترتیبی parameters شامل ہیں۔

اس میں یہ default ترتیبات شامل ہیں:

{* ../../fastapi/openapi/docs.py ln[9:24] hl[18:24] *}

آپ `swagger_ui_parameters` argument میں مختلف قدر سیٹ کر کے ان میں سے کسی کو بھی override کر سکتے ہیں۔

مثال کے طور پر، `deepLinking` کو غیر فعال کرنے کے لیے آپ یہ settings `swagger_ui_parameters` میں پاس کر سکتے ہیں:

{* ../../docs_src/configure_swagger_ui/tutorial003_py310.py hl[3] *}

## دیگر Swagger UI Parameters { #other-swagger-ui-parameters }

تمام ممکنہ ترتیبات دیکھنے کے لیے جو آپ استعمال کر سکتے ہیں، سرکاری [Swagger UI parameters کی دستاویزات](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) پڑھیں۔

## صرف JavaScript والی settings { #javascript-only-settings }

Swagger UI دیگر ترتیبات کی بھی اجازت دیتا ہے جو **صرف JavaScript** objects ہیں (مثال کے طور پر، JavaScript functions)۔

FastAPI میں یہ صرف JavaScript والی `presets` settings بھی شامل ہیں:

```JavaScript
presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIBundle.SwaggerUIStandalonePreset
]
```

یہ **JavaScript** objects ہیں، strings نہیں، اس لیے آپ انہیں Python کوڈ سے براہ راست پاس نہیں کر سکتے۔

اگر آپ کو اس طرح کی صرف JavaScript والی ترتیبات استعمال کرنے کی ضرورت ہے، تو آپ اوپر بیان کردہ طریقوں میں سے کوئی ایک استعمال کر سکتے ہیں۔ تمام Swagger UI *path operation* کو override کریں اور جو بھی JavaScript آپ کو چاہیے دستی طور پر لکھیں۔
