# Frontend { #frontend }

आप `app.frontend()` (या `router.frontend()`) के साथ static frontend apps serve कर सकते हैं।

यह उन frontend tools के लिए उपयोगी है जो static files generate करते हैं, जैसे React with Vite, TanStack Router, Astro, Vue, Svelte, Angular, Solid, और अन्य।

इन tools के साथ, आपके पास आमतौर पर एक step होता है जो frontend को build करता है, जैसे इस command के साथ:

```bash
npm run build
```

यह आपके frontend files के साथ `./dist/` जैसी एक directory generate करेगा।

आप उस directory को इन frontend frameworks के लिए required conventions के अनुसार serve करने के लिए `app.frontend()` का उपयोग कर सकते हैं।

**FastAPI** पहले *path operations* की जाँच करता है। frontend files की जाँच केवल तब की जाती है जब कोई सामान्य route match नहीं हुआ हो, इसलिए आपकी API प्रभावित नहीं होगी।

## Frontend Serve करें { #serve-a-frontend }

अपना frontend build करने के बाद, उदाहरण के लिए `npm run build` के साथ, generate की गई files को किसी directory में रखें, उदाहरण के लिए, `dist`।

आपकी project संरचना ऐसी दिख सकती है:

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

फिर इसे `app.frontend()` के साथ serve करें:

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

इसके साथ, `/assets/app.js` के लिए एक request `dist/assets/app.js` serve कर सकती है।

अगर आपके पास एक **FastAPI** *path operation* भी है, तो *path operation* को प्राथमिकता मिलती है।

## Client-Side Routing { #client-side-routing }

कई frontend apps, जिनमें **single-page apps** (SPAs) शामिल हैं, client-side routing का उपयोग करते हैं। `/dashboard/settings` जैसा path असली file नहीं हो सकता है, लेकिन framework इसे handle करने का ध्यान रखेगा।

इसलिए, अगर उस URL को सीधे access किया जा रहा है (app के अंदर navigate करने के बजाय), तो backend को frontend app को `index.html` से serve करना चाहिए, ताकि frontend framework फिर client-side routing को handle कर सके।

इसके लिए, `fallback="index.html"` का उपयोग करें:

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** इस fallback का उपयोग केवल उन `GET` और `HEAD` requests के लिए करता है जो browser navigation जैसी दिखती हैं। JavaScript, CSS, और images जैसी missing files अभी भी `404` लौटाती हैं।

अन्य methods वाली requests, जैसे `POST` या `PUT`, उन paths पर जो केवल frontend fallback से match करते हैं, वे भी `404` लौटाती हैं। नियमित **FastAPI** *path operations* की priority अभी भी frontend routes से अधिक होती है।

/// tip | सुझाव

Default रूप से, `fallback` की value `fallback="auto"` होती है। अधिकतर मामलों में आपको `fallback` specify करने की ज़रूरत नहीं होगी। विवरण के लिए नीचे पढ़ें।

///

यह वही है जो आप कई frontend apps के साथ चाहेंगे जो client-side routing का उपयोग करते हैं, उदाहरण के लिए, React with TanStack Router, Vue, Angular, SvelteKit, या Solid।

## Custom 404 Page { #custom-404-page }

आप missing frontend paths के लिए static `404.html` page भी serve कर सकते हैं:

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

वह response `404` का status code बनाए रखती है।

इस मामले में, **FastAPI** missing frontend paths के लिए `index.html` serve नहीं करेगा। इसके बजाय यह `404.html` file लौटाएगा।

/// tip | सुझाव

Default रूप से, `fallback` की value `fallback="auto"` होती है। इसके साथ, अगर `404.html` file मिलती है, तो उसे अपने-आप fallback के रूप में उपयोग किया जाएगा।

इसलिए, आप सामान्यतः `fallback` argument छोड़ सकते हैं।

///

यह उन frontend tools के साथ उपयोगी है जो हर page के लिए static HTML files generate करते हैं, जैसे Astro।

## Fallback Auto { #fallback-auto }

Default रूप से, `app.frontend()` `fallback="auto"` का उपयोग करता है।

अगर frontend directory में `404.html` file है, तो missing frontend paths उस file को status code `404` के साथ serve करते हैं।

अन्यथा, अगर `index.html` file है, तो missing browser navigation paths `index.html` serve करते हैं, जो client-side routing वाले कई frontend apps अपेक्षा करते हैं।

इसलिए, अधिकतर मामलों में आप `fallback` argument specify किए बिना `app.frontend("/", directory="dist")` का उपयोग कर सकते हैं।

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## Fallback बंद करें { #disable-fallback }

अगर आप missing frontend paths के लिए fallback file serve नहीं करना चाहते, तो `fallback=None` का उपयोग करें:

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

फिर missing frontend paths सामान्य `404` लौटाते हैं।

## Directory जाँचें { #check-directory }

Default रूप से, `app.frontend()` app बनाते समय जाँचता है कि directory मौजूद है।

यह configuration errors को जल्दी पकड़ने में मदद करता है। उदाहरण के लिए, अगर frontend build output directory missing है, तो **FastAPI** startup पर error raise करेगा।

अगर आपकी frontend files बाद में बनाई जाती हैं, उदाहरण के लिए app object बनने के बाद किसी अलग build step द्वारा, तो `check_dir=False` set करें:

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

`check_dir=False` के साथ, **FastAPI** app बनाते समय directory की जाँच नहीं करेगा। अगर configured directory किसी request को handle करते समय अभी भी missing है, तो **FastAPI** तब error raise करेगा।

## इसे `APIRouter` के साथ उपयोग करें { #use-it-with-apirouter }

आप frontend files को `APIRouter` में भी जोड़ सकते हैं और उसे prefix के साथ include कर सकते हैं:

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

इस उदाहरण में, frontend paths `/app` के अंतर्गत serve किए जाते हैं।

App में कोई भी नियमित *path operations* अभी भी precedence लेंगे, अन्य routers में शामिल ones भी।

## Dependencies और Middleware { #dependencies-and-middleware }

Frontend responses सामान्य **FastAPI** application के अंदर run करती हैं, इसलिए HTTP middleware उन पर लागू होता है।

App से, `APIRouter` से, और `include_router()` से dependencies भी frontend responses पर लागू होती हैं। यह cookie authentication या इसी तरह से frontend को protect करने के लिए उपयोगी हो सकता है।

## केवल Static Build Output { #static-build-output-only }

`app.frontend()` आपके frontend build द्वारा पहले से generate की गई files serve करता है।

यह server-side rendering run नहीं करता। यह उन frontend frameworks के लिए है जो static files generate करते हैं, न कि उन frameworks के लिए जिन्हें हर request के लिए server पर dynamic rendering की ज़रूरत होती है।
