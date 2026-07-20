# Deployment { #deployment }

**FastAPI** application को deploy करना अपेक्षाकृत आसान है।

## Deployment का क्या अर्थ है { #what-does-deployment-mean }

किसी application को **deploy** करने का अर्थ है उसे **users के लिए उपलब्ध** कराने के लिए आवश्यक चरण पूरे करना।

किसी **web API** के लिए, इसमें सामान्यतः उसे एक **remote machine** में रखना शामिल होता है, एक **server program** के साथ जो अच्छा performance, stability आदि प्रदान करता है, ताकि आपके **users** application को कुशलता से और बिना रुकावटों या समस्याओं के **access** कर सकें।

यह **development** चरणों के विपरीत है, जहाँ आप लगातार code बदल रहे होते हैं, उसे तोड़ते और ठीक करते हैं, development server को रोकते और फिर से शुरू करते हैं, आदि।

## Deployment Strategies { #deployment-strategies }

इसे करने के कई तरीके हैं, जो आपके विशिष्ट use case और आपके द्वारा उपयोग किए जाने वाले tools पर निर्भर करते हैं।

आप tools के संयोजन का उपयोग करके स्वयं **server deploy** कर सकते हैं, आप कोई **cloud service** उपयोग कर सकते हैं जो आपके लिए काम का कुछ हिस्सा करती है, या अन्य संभावित विकल्प चुन सकते हैं।

उदाहरण के लिए, हमने, FastAPI के पीछे की team ने, [**FastAPI Cloud**](https://fastapicloud.com) बनाया, ताकि FastAPI apps को cloud पर deploy करना जितना संभव हो उतना streamlined हो, FastAPI के साथ काम करने के समान developer experience के साथ।

मैं आपको कुछ मुख्य concepts दिखाऊँगा जिन्हें **FastAPI** application deploy करते समय शायद ध्यान में रखना चाहिए (हालाँकि इनमें से अधिकतर किसी भी अन्य प्रकार की web application पर लागू होता है)।

अगले sections में आपको ध्यान में रखने के लिए अधिक details और इसे करने की कुछ techniques दिखेंगी। ✨
