# OAuth2 yenye Nenosiri (na hashing), Bearer yenye tokeni za JWT { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

Sasa kwa kuwa tuna mtiririko mzima wa usalama, tuifanye programu iwe salama kweli, kwa kutumia tokeni za <abbr title="JSON Web Tokens - Tokeni za Wavuti za JSON">JWT</abbr> na hashing salama ya nywila.

Huu ni msimbo unaoweza kuutumia katika programu yako, kuhifadhi hash za nywila kwenye hifadhidata yako, n.k.

Tutaanzia pale tulipoishia katika sura iliyotangulia na kuuongeza.

## Kuhusu JWT { #about-jwt }

JWT inamaanisha "JSON Web Tokens".

Ni kiwango cha kusimba object ya JSON kuwa mfuatano mrefu wa herufi ulioshikamana bila nafasi. Inaonekana hivi:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Haijasimbwa kwa njia fiche, kwa hivyo mtu yeyote anaweza kurejesha taarifa kutoka kwenye yaliyomo.

Lakini imetiwa saini. Kwa hivyo, unapopokea tokeni uliyotoa, unaweza kuthibitisha kuwa wewe ndiye uliyeitoa.

Kwa njia hiyo, unaweza kuunda tokeni yenye muda wa kuisha wa, tuseme, wiki 1. Kisha mtumiaji anaporudi siku inayofuata akiwa na tokeni hiyo, unajua kuwa mtumiaji huyo bado ameingia kwenye mfumo wako.

Baada ya wiki moja, tokeni itakuwa imeisha muda wake na mtumiaji hataruhusiwa kuendelea; itabidi aingie tena ili apate tokeni mpya. Na ikiwa mtumiaji (au mtu mwingine) angejaribu kurekebisha tokeni ili kubadilisha muda wake wa kuisha, ungeweza kugundua hilo, kwa sababu saini hazingelingana.

Ikiwa unataka kufanya majaribio na tokeni za JWT na kuona jinsi zinavyofanya kazi, angalia [https://jwt.io](https://jwt.io/).

## Sakinisha `PyJWT` { #install-pyjwt }

Tunahitaji kusakinisha `PyJWT` ili kutengeneza na kuthibitisha tokeni za JWT katika Python.

Ongeza `pyjwt` kwenye mradi wako:

<div class="termy">

```console
$ uv add pyjwt

---> 100%
```

</div>

/// note | Tanbihi

Ikiwa unapanga kutumia algoriti za saini za kidijitali kama RSA au ECDSA, unapaswa kusakinisha kitegemezi cha maktaba ya cryptography cha `pyjwt[crypto]`.

Unaweza kusoma zaidi kuhusu hilo katika [nyaraka za usakinishaji wa PyJWT](https://pyjwt.readthedocs.io/en/latest/installation.html).

///

## Hashing ya nywila { #password-hashing }

"Hashing" inamaanisha kubadilisha maudhui fulani (nenosiri katika hali hii) kuwa mfuatano wa baiti (string tu) unaoonekana kama maandishi yasiyo na maana.

Kila unapopitisha maudhui yale yale kabisa (nenosiri lile lile kabisa), unapata maandishi yale yale yasiyo na maana.

Lakini huwezi kuyabadilisha maandishi hayo kurudi kuwa nenosiri.

### Kwa nini utumie hashing ya nywila { #why-use-password-hashing }

Ikiwa hifadhidata yako itaibiwa, mwizi hatakuwa na nywila za watumiaji wako zilizo katika maandishi ya kawaida, bali hash zake tu.

Kwa hivyo, mwizi hataweza kujaribu kutumia nenosiri hilo katika mfumo mwingine (kwa kuwa watumiaji wengi hutumia nenosiri lile lile kila mahali, hilo lingekuwa hatari).

## Sakinisha `pwdlib` { #install-pwdlib }

pwdlib ni kifurushi kizuri cha Python cha kushughulikia hash za nywila.

Kinaunga mkono algoriti nyingi salama za hashing na zana za kuzitumia.

Algoriti inayopendekezwa ni "Argon2".

Ongeza `pwdlib` yenye Argon2 kwenye mradi wako:

<div class="termy">

```console
$ uv add "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | Kidokezo

Ukiwa na `pwdlib`, unaweza hata kuisanidi iweze kusoma nywila zilizoundwa na **Django**, programu-jalizi ya usalama ya **Flask** au nyingine nyingi.

Kwa hivyo, kwa mfano, ungeweza kushiriki data ile ile ya programu ya Django iliyo katika hifadhidata na programu ya FastAPI. Au kuhamisha programu ya Django hatua kwa hatua huku ukitumia hifadhidata ile ile.

Na watumiaji wako wangeweza kuingia kupitia programu yako ya Django au kupitia programu yako ya **FastAPI**, wakati huo huo.

///

## Tengeneza hash na uhakiki nywila { #hash-and-verify-the-passwords }

Ingiza zana tunazohitaji kutoka `pwdlib`.

Unda instance ya PasswordHash yenye mipangilio inayopendekezwa — itatumika kutengeneza hash na kuhakiki nywila.

/// tip | Kidokezo

pwdlib pia inaunga mkono algoriti ya hashing ya bcrypt lakini haijumuishi algoriti za zamani — ili kufanya kazi na hash zilizopitwa na wakati, inapendekezwa kutumia maktaba ya passlib.

Kwa mfano, ungeweza kuitumia kusoma na kuhakiki nywila zilizotengenezwa na mfumo mwingine (kama Django) lakini ukatengeneza hash za nywila zozote mpya kwa algoriti tofauti kama Argon2 au Bcrypt.

Na kuwa na uoanifu na zote kwa wakati mmoja.

///

Unda function saidizi ya kutengeneza hash ya nenosiri linalotoka kwa mtumiaji.

Na nyingine ya kuhakiki kama nenosiri lililopokewa linalingana na hash iliyohifadhiwa.

Na nyingine ya kuthibitisha utambulisho wa mtumiaji na kumrudisha.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

Wakati `authenticate_user` inapoitwa kwa jina la mtumiaji lisilokuwepo kwenye hifadhidata, bado tunaendesha `verify_password` dhidi ya hash mbadala.

Hii inahakikisha kuwa endpoint inachukua takribani muda ule ule kujibu iwe jina la mtumiaji ni halali au la, na hivyo kuzuia **mashambulizi ya kupima muda (timing attacks)** yanayoweza kutumiwa kubaini majina ya watumiaji yaliyopo.

/// note | Tanbihi

Ukiangalia hifadhidata mpya (ya mfano) `fake_users_db`, utaona jinsi hash ya nenosiri inavyoonekana sasa: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## Shughulikia tokeni za JWT { #handle-jwt-tokens }

Ingiza moduli zilizosakinishwa.

Unda ufunguo wa siri wa nasibu utakaotumika kutia saini tokeni za JWT.

Ili kutengeneza ufunguo wa siri wa nasibu ulio salama, tumia amri hii:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Na unakili matokeo kwenye kigeu `SECRET_KEY` (usitumie ule ulio kwenye mfano).

Unda kigeu `ALGORITHM` chenye algoriti inayotumika kutia saini tokeni ya JWT na ukipe thamani `"HS256"`.

Unda kigeu cha muda wa kuisha wa tokeni.

Fafanua modeli ya Pydantic itakayotumika katika endpoint ya tokeni kwa ajili ya jibu.

Unda function saidizi ya kutengeneza tokeni mpya ya ufikiaji.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Sasisha vitegemezi { #update-the-dependencies }

Sasisha `get_current_user` ili ipokee tokeni kama hapo awali, lakini wakati huu kwa kutumia tokeni za JWT.

Fumbua usimbaji wa tokeni iliyopokewa, ithibitishe, na urudishe mtumiaji wa sasa.

Ikiwa tokeni si halali, rudisha hitilafu ya HTTP mara moja.

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## Sasisha *operesheni ya njia* ya `/token` { #update-the-token-path-operation }

Unda `timedelta` yenye muda wa kuisha wa tokeni.

Unda tokeni halisi ya ufikiaji ya JWT na uirudishe.

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### Maelezo ya kiufundi kuhusu "subject" ya JWT `sub` { #technical-details-about-the-jwt-subject-sub }

Vipimo vya JWT vinasema kuwa kuna ufunguo `sub`, wenye mhusika wa tokeni.

Kuutumia ni hiari, lakini hapo ndipo ungeweka kitambulisho cha mtumiaji, kwa hivyo tunautumia hapa.

JWT inaweza kutumika kwa mambo mengine mbali na kumtambua mtumiaji na kumruhusu kufanya operesheni moja kwa moja kwenye API yako.

Kwa mfano, ungeweza kutambua "gari" au "chapisho la blogu".

Kisha ungeweza kuongeza ruhusa zinazohusu kitu hicho, kama "endesha" (kwa gari) au "hariri" (kwa blogu).

Na kisha, ungeweza kumpa mtumiaji (au bot) tokeni hiyo ya JWT, na angeweza kuitumia kufanya vitendo hivyo (kuendesha gari, au kuhariri chapisho la blogu) bila hata kuhitaji kuwa na akaunti, kwa kutumia tu tokeni ya JWT ambayo API yako ilitengeneza kwa ajili hiyo.

Kwa kutumia mawazo haya, JWT inaweza kutumika katika hali changamani zaidi.

Katika hali hizo, vitu kadhaa vinaweza kuwa na ID ile ile, tuseme `foo` (mtumiaji `foo`, gari `foo`, na chapisho la blogu `foo`).

Kwa hivyo, ili kuepuka migongano ya ID, unapounda tokeni ya JWT kwa ajili ya mtumiaji, ungeweza kuongeza kiambishi mwanzoni mwa thamani ya ufunguo `sub`, k.m. `username:`. Kwa hivyo, katika mfano huu, thamani ya `sub` ingeweza kuwa: `username:johndoe`.

Jambo muhimu la kukumbuka ni kwamba ufunguo `sub` unapaswa kuwa na kitambulisho cha kipekee katika programu nzima, na unapaswa kuwa string.

## Ijaribu { #check-it }

Endesha seva na uende kwenye nyaraka: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Utaona kiolesura cha mtumiaji kama hiki:

<img src="/img/tutorial/security/image07.png">

Idhinisha programu kwa njia ile ile ya awali.

Kwa kutumia taarifa hizi za kuingia:

Jina la mtumiaji: `johndoe`
Nenosiri: `secret`

/// tip | Kidokezo

Tambua kuwa hakuna mahali popote kwenye msimbo palipo na nenosiri la maandishi ya kawaida "`secret`", tuna hash yake tu.

///

<img src="/img/tutorial/security/image08.png">

Ita endpoint `/users/me/`, utapata jibu kama hili:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Ukifungua zana za msanidi programu, unaweza kuona jinsi data inayotumwa inavyojumuisha tokeni pekee; nenosiri hutumwa tu katika ombi la kwanza ili kuthibitisha utambulisho wa mtumiaji na kupata tokeni hiyo ya ufikiaji, lakini si baada ya hapo:

<img src="/img/tutorial/security/image10.png">

/// note | Tanbihi

Tambua kichwa `Authorization`, chenye thamani inayoanza na `Bearer `.

///

## Matumizi ya hali ya juu yenye `scopes` { #advanced-usage-with-scopes }

OAuth2 ina dhana ya "scopes".

Unaweza kuzitumia kuongeza seti maalumu ya ruhusa kwenye tokeni ya JWT.

Kisha unaweza kumpa mtumiaji tokeni hiyo moja kwa moja au kuipatia mhusika mwingine, ili kuwasiliana na API yako kwa kufuata vizuizi fulani.

Unaweza kujifunza jinsi ya kuzitumia na jinsi zinavyounganishwa na **FastAPI** baadaye katika **Mwongozo wa Kina wa Mtumiaji**.

## Muhtasari { #recap }

Kwa yale ambayo umeona hadi sasa, unaweza kuandaa programu salama ya **FastAPI** kwa kutumia viwango kama OAuth2 na JWT.

Katika takribani kila framework, kushughulikia usalama huwa jambo changamani kwa haraka sana.

Vifurushi vingi vinavyorahisisha jambo hilo sana hulazimika kuweka vikwazo vingi kwenye modeli ya data, hifadhidata, na vipengele vinavyopatikana. Na baadhi ya vifurushi hivi vinavyorahisisha mambo kupita kiasi kwa kweli vina dosari za usalama zisizoonekana wazi.

---

**FastAPI** haiweki vikwazo katika uchaguzi wa hifadhidata, modeli ya data au zana yoyote.

Inakupa unyumbufu wote wa kuchagua zile zinazofaa zaidi mradi wako.

Na unaweza kutumia moja kwa moja vifurushi vingi vinavyotunzwa vizuri na vinavyotumika sana kama `pwdlib` na `PyJWT`, kwa sababu **FastAPI** haihitaji mifumo changamani ya kuunganisha vifurushi vya nje.

Lakini inakupa zana za kurahisisha mchakato kadiri iwezekanavyo bila kuathiri unyumbufu, uimara, au usalama.

Na unaweza kutumia na kutekeleza itifaki salama za viwango vinavyokubalika, kama OAuth2, kwa njia rahisi kiasi.

Unaweza kujifunza zaidi katika **Mwongozo wa Kina wa Mtumiaji** kuhusu jinsi ya kutumia "scopes" za OAuth2, kwa mfumo wa ruhusa wenye udhibiti wa kina zaidi, kwa kufuata viwango hivi hivi. OAuth2 yenye scopes ndiyo njia inayotumiwa na watoa huduma wengi wakubwa wa uthibitishaji wa utambulisho, kama Facebook, Google, GitHub, Microsoft, X (Twitter), n.k. kuidhinisha programu za wahusika wengine kuwasiliana na API zao kwa niaba ya watumiaji wao.
