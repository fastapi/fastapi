# Path operation decorators میں Dependencies { #dependencies-in-path-operation-decorators }

بعض اوقات آپ کو واقعی اپنے *path operation function* کے اندر dependency کی واپسی value کی ضرورت نہیں ہوتی۔

یا dependency کوئی value واپس نہیں کرتی۔

لیکن پھر بھی آپ کو اسے execute/حل ہونے کی ضرورت ہے۔

ان صورتوں میں، `Depends` کے ساتھ *path operation function* parameter declare کرنے کے بجائے، آپ *path operation decorator* میں `dependencies` کی `list` شامل کر سکتے ہیں۔

## *path operation decorator* میں `dependencies` شامل کریں { #add-dependencies-to-the-path-operation-decorator }

*path operation decorator* ایک اختیاری argument `dependencies` وصول کرتا ہے۔

یہ `Depends()` کی ایک `list` ہونی چاہیے:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[19] *}

یہ dependencies عام dependencies کی طرح ہی execute/حل ہوں گی۔ لیکن ان کی value (اگر وہ کوئی واپس کریں) آپ کے *path operation function* میں پاس نہیں ہوگی۔

/// tip | مشورہ

کچھ editors غیر استعمال شدہ function parameters کی جانچ کرتے ہیں اور انہیں errors کے طور پر دکھاتے ہیں۔

*path operation decorator* میں ان `dependencies` کو استعمال کر کے آپ یقینی بنا سکتے ہیں کہ وہ execute ہوں جبکہ editor/tooling errors سے بچا جائے۔

یہ نئے developers کے لیے الجھن سے بچنے میں بھی مدد کر سکتا ہے جو آپ کے code میں غیر استعمال شدہ parameter دیکھ کر سوچ سکتے ہیں کہ یہ غیر ضروری ہے۔

///

/// info | معلومات

اس مثال میں ہم من گھڑت custom headers `X-Key` اور `X-Token` استعمال کر رہے ہیں۔

لیکن حقیقی صورتوں میں، security implement کرتے وقت، آپ کو مربوط [Security utilities (اگلا باب)](../security/index.md) استعمال کرنے سے زیادہ فائدہ ہوگا۔

///

## Dependencies کی errors اور واپسی values { #dependencies-errors-and-return-values }

آپ وہی dependency *functions* استعمال کر سکتے ہیں جو آپ عام طور پر استعمال کرتے ہیں۔

### Dependency کے تقاضے { #dependency-requirements }

یہ request کے تقاضے (جیسے headers) یا دیگر sub-dependencies declare کر سکتی ہیں:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[8,13] *}

### Exceptions raise کریں { #raise-exceptions }

یہ dependencies عام dependencies کی طرح exceptions `raise` کر سکتی ہیں:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[10,15] *}

### واپسی values { #return-values }

اور یہ values واپس کر سکتی ہیں یا نہیں، values استعمال نہیں ہوں گی۔

تو، آپ ایک عام dependency (جو value واپس کرتی ہے) جو آپ پہلے سے کہیں اور استعمال کر رہے ہیں، دوبارہ استعمال کر سکتے ہیں، اور اگرچہ value استعمال نہیں ہوگی، dependency execute ضرور ہوگی:

{* ../../docs_src/dependencies/tutorial006_an_py310.py hl[11,16] *}

## *path operations* کے گروپ کے لیے Dependencies { #dependencies-for-a-group-of-path-operations }

بعد میں، جب آپ بڑی ایپلیکیشنز کی ساخت کے بارے میں پڑھیں گے ([بڑی ایپلیکیشنز - متعدد فائلیں](../../tutorial/bigger-applications.md))، ممکنہ طور پر متعدد فائلوں کے ساتھ، آپ سیکھیں گے کہ *path operations* کے گروپ کے لیے ایک `dependencies` parameter کیسے declare کیا جائے۔

## Global Dependencies { #global-dependencies }

اگلے مرحلے میں ہم دیکھیں گے کہ پوری `FastAPI` ایپلیکیشن میں dependencies کیسے شامل کی جائیں، تاکہ وہ ہر *path operation* پر لاگو ہوں۔
