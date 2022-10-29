# அம்சங்கள்

## FastAPIயின் அம்சங்கள்

**FastAPI** கீழே உள்ள அம்சங்களை கொடுக்கிறது:

### திறந்த தரநிலைகளின் அடிப்படையில்

* API உருவாக்குவதற்க்கு, <abbr title="also known as: endpoints, routes">பாதை</abbr> <abbr title="also known as HTTP methods, as POST, GET, PUT, DELETE">செயல்பாடுகள் அறிவித்தல்</abbr>, <abbr title="parameters">அளவுருவிகள்</abbr>, வேண்டுதலின் உடல், பாதுகாப்பு போன்றவைகள் <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> சார்ந்தன.
* <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>ஜசான் ஸ்கிமா</strong></a> கொண்ட தரவு மாதிரி ஆவணம் தானாகவே இருக்கும் (OpenAPIயும் ஜசான் ஸ்கிமா சார்ந்தது).
* ஏதோ தானோ என்று இல்லாமல், கவனமான ஆழ்ந்த படித்தலுக்கு பிறகு செந்தரங்களை சார்ந்தது வடிவமைக்கபட்டது.
* இது தானாகவே பல மொழிகளில் **பயனாளி குறீயிடு உருவாக்குதலுக்கு** வழி வகுக்கிறது.

## தானாகவே உருவாகும் ஆவணம்

ஊடாடும் API ஆவணம் மற்றும் ஆராய்வதற்க்கு வலைய பயணர் இடைமுகங்கள். வரைசட்டம் OpenAPI அடிப்படையில் இருப்பதால், ஆவணத்திற்க்கு பல வழிகள் இருக்கின்றன. முன்னிருப்பாக 2

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a> கொண்டு, நேராக மேலோடியில் APIயுடன் ஊடாடி ஆராய்ந்து, அழைத்து சோதிக்கலாம்.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a> மூலம் வேறொரு API ஆவணம்.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### வெறும் பைத்தான்

அனைத்தும் **பைத்தான் 3.6 வகை** அறிவிப்புகளை சார்ந்த்து, பைடான்டிக் காரணமாக. புதிதாக ஒர் இலக்கணம் கற்க வேண்டும் என அவசியமில்லை.

பைத்தான் வகைகளை பயன்படுத்துவதை பற்றி 2 நிமிடத்தில், இந்த சிறிய பாடத்தை பார்க்கலாம்: [Python Types](python-types.md){.internal-link target=_blank}.

பைத்தானை வகைகளுடன் இவ்வாறு எழுதுவிர்:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

That can then be used like:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! குறிப்பு
    `**second_user_data`வின் பொருள்:

    `second_user_data` அகராதியின் சாவி மற்றும் அளவிடுகளை நேராக சாவி-அளவிடு ஜோடியாக அனுப்புக, அதாவது `User(id=4, name="Mary", joined="2018-11-30")` யாக.
    
### தொகுப்பி துணை

சிறந்த உருவாக்குதல் அனுபவத்திற்காக, அனைத்து வரைசட்டங்களும் உள்ளுணர்வோடு எளிதாக பயன்படுத்த வடிவமைக்கபட்டது. மேலும், அனைத்து முடிவுகளும் பல தொகுப்பிகளில் வேலை ஆரம்பிபதற்க்கு முன்பே சோதிக்கபட்டது.

கடைசி பைத்தான் கணக்கெடுப்பில், <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">"தானேமுடித்தலே" அதிகமாக பயன்படுத்திய அம்சம் என தெரியவந்தது</a>.

**FastAPI** வரைசட்டம் தானேமுடித்தலை எங்கும் சாத்தியபடுத்தும்.

உங்கள் தொகுப்பி உங்களுக்கு இவ்வாறு உதவும்:

* in <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* in <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

நிங்கள் 