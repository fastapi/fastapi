# Global Dependencies { #global-dependencies }

بعض قسم کی ایپلیکیشنز کے لیے آپ پوری ایپلیکیشن میں dependencies شامل کرنا چاہ سکتے ہیں۔

جس طرح آپ [*path operation decorators* میں `dependencies` شامل](dependencies-in-path-operation-decorators.md) کر سکتے ہیں، اسی طرح آپ انہیں `FastAPI` ایپلیکیشن میں شامل کر سکتے ہیں۔

اس صورت میں، یہ ایپلیکیشن کے تمام *path operations* پر لاگو ہوں گی:

{* ../../docs_src/dependencies/tutorial012_an_py310.py hl[17] *}


اور [*path operation decorators* میں `dependencies` شامل کرنے](dependencies-in-path-operation-decorators.md) کے سیکشن کے تمام تصورات ابھی بھی لاگو ہوتے ہیں، لیکن اس صورت میں، ایپ کے تمام *path operations* پر۔

## *path operations* کے گروپوں کے لیے Dependencies { #dependencies-for-groups-of-path-operations }

بعد میں، جب آپ بڑی ایپلیکیشنز کی ساخت کے بارے میں پڑھیں گے ([بڑی ایپلیکیشنز - متعدد فائلیں](../../tutorial/bigger-applications.md))، ممکنہ طور پر متعدد فائلوں کے ساتھ، آپ سیکھیں گے کہ *path operations* کے گروپ کے لیے ایک `dependencies` parameter کیسے declare کیا جائے۔
