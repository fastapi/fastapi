# OAuth2 yenye Nenosiri (na hashing), Bearer yenye token za JWT { #oauth2-with-password-and-hashing-bearer-with-jwt-tokens }

Sasa kwa kuwa tuna mtiririko mzima wa usalama, hebu tufanye programu iwe salama kweli, kwa kutumia token za <abbr title="JSON Web Tokens - Token za Wavuti za JSON">JWT</abbr> na hashing salama ya manenosiri.

Msimbo huu ni kitu unachoweza kutumia katika programu yako, kuhifadhi hash za manenosiri katika hifadhidata yako, n.k.

Tutaanzia pale tulipoishia katika sura iliyopita na kuuongezea.

## Kuhusu JWT { #about-jwt }

JWT inamaanisha "JSON Web Tokens".

Ni kiwango cha kusimba object ya JSON kuwa string ndefu yenye msongamano bila nafasi. Inaonekana hivi:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Haijalindwa kwa encryption, kwa hiyo mtu yeyote anaweza kupata taarifa kutoka kwenye maudhui yake.

Lakini ina digital signature. Kwa hiyo, unapopokea token uliyotoa, unaweza kuthibitisha kuwa ni wewe uliyeitoa.

Kwa njia hiyo, unaweza kuunda token yenye muda wa kuisha wa, tuseme, wiki 1. Kisha mtumiaji anaporudi siku inayofuata akiwa na token hiyo, unajua kuwa mtumiaji huyo bado ameingia kwenye mfumo wako.

Baada ya wiki moja, token itakuwa imeisha muda wake na mtumiaji hatakuwa ameidhinishwa na atalazimika kuingia tena ili kupata token mpya. Na ikiwa mtumiaji (au mhusika mwingine) angejaribu kurekebisha token ili kubadilisha muda wa kuisha, ungeweza kugundua hilo, kwa sababu digital signature hazingelingana.

Ikiwa unataka kujaribu token za JWT na kuona jinsi zinavyofanya kazi, angalia [https://jwt.io](https://jwt.io/).

## Sakinisha `PyJWT` { #install-pyjwt }

Tunahitaji kusakinisha `PyJWT` ili kutengeneza na kuthibitisha token za JWT katika Python.

Ongeza `pyjwt` kwenye mradi wako:

<div class="termy">

```console
$ uv add pyjwt

---> 100%
```

</div>

/// note | Tanbihi

Ikiwa unapanga kutumia algoriti za digital signature kama RSA au ECDSA, unapaswa kusakinisha kitegemezi cha maktaba ya cryptography, `pyjwt[crypto]`.

Unaweza kusoma zaidi kuhusu hilo katika [nyaraka za Usakinishaji wa PyJWT](https://pyjwt.readthedocs.io/en/latest/installation.html).

///

## Hashing ya manenosiri { #password-hashing }

"Hashing" inamaanisha kubadilisha maudhui fulani (nenosiri katika hali hii) kuwa mfuatano wa byte (string tu) unaoonekana kutokuwa na maana.

Kila unapopitisha maudhui yaleyale kabisa (nenosiri lilelile kabisa), unapata mfuatano uleule kabisa usioeleweka.

Lakini huwezi kubadilisha mfuatano huo kurudi kuwa nenosiri.

### Kwa nini utumie hashing ya manenosiri { #why-use-password-hashing }

Hifadhidata yako ikiibiwa, mwizi hatakuwa na manenosiri ya watumiaji wako katika plaintext, bali hash pekee.

Kwa hiyo, mwizi hataweza kujaribu kutumia nenosiri hilo katika mfumo mwingine (kwa kuwa watumiaji wengi hutumia nenosiri lilelile kila mahali, hili lingekuwa hatari).

## Sakinisha `pwdlib` { #install-pwdlib }

pwdlib ni package nzuri sana ya Python ya kushughulikia hash za manenosiri.

Inatumia algoriti nyingi salama za hashing na zana za kufanya kazi nazo.

Algoriti inayopendekezwa ni "Argon2".

Ongeza `pwdlib` yenye Argon2 kwenye mradi wako:

<div class="termy">

```console
$ uv add "pwdlib[argon2]"

---> 100%
```

</div>

/// tip | Kidokezo

Kwa kutumia `pwdlib`, unaweza hata kuisanidi ili iweze kusoma manenosiri yaliyoundwa na **Django**, plug-in ya usalama ya **Flask** au nyingine nyingi.

Kwa hiyo, kwa mfano, ungeweza kutumia data ileile ya programu ya Django iliyo katika hifadhidata pamoja na programu ya FastAPI. Au kuhamisha programu ya Django hatua kwa hatua huku ukitumia hifadhidata ileile.

Na watumiaji wako wangeweza kuingia kutoka kwenye programu yako ya Django au kutoka kwenye programu yako ya **FastAPI**, kwa wakati mmoja.

///

## Fanya hashing na uthibitishe manenosiri { #hash-and-verify-the-passwords }

Import zana tunazohitaji kutoka `pwdlib`.

Unda instance ya PasswordHash yenye mipangilio inayopendekezwa — itatumika kufanya hashing na kuthibitisha manenosiri.

/// tip | Kidokezo

pwdlib pia inatumia algoriti ya hashing ya bcrypt lakini haijumuishi algoriti za zamani — ili kufanya kazi na hash zilizopitwa na wakati, inashauriwa kutumia maktaba ya passlib.

Kwa mfano, ungeweza kuitumia kusoma na kuthibitisha manenosiri yaliyotengenezwa na mfumo mwingine (kama Django) lakini ukafanya hashing ya manenosiri yote mapya kwa algoriti tofauti kama Argon2 au Bcrypt.

Na hivyo kuweza kufanya kazi na zote kwa wakati mmoja.

///

Unda function saidizi ya kufanya hashing ya nenosiri linalotoka kwa mtumiaji.

Na nyingine ya kuthibitisha ikiwa nenosiri lililopokelewa linalingana na hash iliyohifadhiwa.

Na nyingine ya kuthibitisha utambulisho wa mtumiaji na kumrudisha.

{* ../../docs_src/security/tutorial004_an_py310.py hl[8,49,51,58:59,62:63,72:79] *}

Wakati `authenticate_user` inapoitwa kwa jina la mtumiaji ambalo halipo katika hifadhidata, bado tunaendesha `verify_password` dhidi ya hash mbadala.

Hii inahakikisha kuwa endpoint inachukua takriban muda uleule kujibu iwe jina la mtumiaji ni halali au la, na kuzuia **timing attacks** zinazoweza kutumiwa kubaini majina ya watumiaji yaliyopo.

/// note | Tanbihi

Ukiangalia hifadhidata mpya (ya kuigiza) `fake_users_db`, utaona jinsi nenosiri lililofanyiwa hashing linavyoonekana sasa: `"$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"`.

///

## Shughulikia token za JWT { #handle-jwt-tokens }

Import module zilizosakinishwa.

Unda secret key ya nasibu itakayotumika kuweka digital signature kwenye token za JWT.

Ili kutengeneza secret key salama ya nasibu tumia amri:

<div class="termy">

```console
$ openssl rand -hex 32

09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

</div>

Na unakili output kwenye kigeu `SECRET_KEY` (usitumie ile iliyo katika mfano).

Unda kigeu `ALGORITHM` chenye algoriti inayotumika kuweka digital signature kwenye token ya JWT na uweke thamani yake kuwa `"HS256"`.

Unda kigeu cha muda wa kuisha wa token.

Fafanua Model ya Pydantic itakayotumika katika endpoint ya token kwa ajili ya response.

Unda function saidizi ya kutengeneza access token mpya.

{* ../../docs_src/security/tutorial004_an_py310.py hl[4,7,13:15,29:31,82:90] *}

## Sasisha vitegemezi { #update-the-dependencies }

Sasisha `get_current_user` ili ipokee token ileile kama awali, lakini safari hii, kwa kutumia token za JWT.

Fanya decoding ya token iliyopokelewa, ithibitishe, na urudishe mtumiaji wa sasa.

Ikiwa token si halali, rudisha hitilafu ya HTTP mara moja.

{* ../../docs_src/security/tutorial004_an_py310.py hl[93:110] *}

## Sasisha *path operation* ya `/token` { #update-the-token-path-operation }

Unda `timedelta` yenye muda wa kuisha wa token.

Unda access token halisi ya JWT na uirudishe.

{* ../../docs_src/security/tutorial004_an_py310.py hl[121:136] *}

### Maelezo ya kiufundi kuhusu "subject" ya JWT `sub` { #technical-details-about-the-jwt-subject-sub }

Uainisho wa JWT unasema kuwa kuna key `sub`, yenye subject ya token.

Si lazima kuitumia, lakini hapo ndipo unapoweza kuweka kitambulisho cha mtumiaji, kwa hiyo tunaitumia hapa.

JWT inaweza kutumika kwa mambo mengine mbali na kumtambua mtumiaji na kumruhusu kufanya operesheni moja kwa moja kwenye API yako.

Kwa mfano, ungeweza kutambua "gari" au "chapisho la blogu".

Kisha ungeweza kuongeza ruhusa zinazohusu entity hiyo, kama "kuendesha" (kwa gari) au "kuhariri" (kwa blogu).

Na kisha, ungeweza kumpa mtumiaji (au bot) token hiyo ya JWT, naye angeweza kuitumia kufanya vitendo hivyo (kuendesha gari, au kuhariri chapisho la blogu) bila hata kuhitaji kuwa na akaunti, kwa kutumia tu token ya JWT ambayo API yako ilitengeneza kwa ajili hiyo.

Kwa kutumia mawazo haya, JWT inaweza kutumika katika hali changamano zaidi.

Katika hali hizo, baadhi ya entity hizo zinaweza kuwa na ID ileile, tuseme `foo` (mtumiaji `foo`, gari `foo`, na chapisho la blogu `foo`).

Kwa hiyo, ili kuzuia migongano ya ID, unapounda token ya JWT kwa mtumiaji, ungeweza kuongeza kiambishi awali kwenye thamani ya key ya `sub`, kwa mfano `username:`. Kwa hiyo, katika mfano huu, thamani ya `sub` ingeweza kuwa: `username:johndoe`.

Jambo muhimu la kukumbuka ni kuwa key ya `sub` inapaswa kuwa na kitambulisho cha kipekee katika programu nzima, na kinapaswa kuwa string.

## Ijaribu { #check-it }

Endesha server na uende kwenye nyaraka: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Utaona kiolesura cha mtumiaji kama hiki:

<img src="/img/tutorial/security/image07.png">

Idhinisha programu kwa njia ileile kama awali.

Kwa kutumia taarifa za kuingia:

Jina la mtumiaji: `johndoe`
Nenosiri: `secret`

/// tip | Kidokezo

Tambua kuwa hakuna sehemu yoyote katika msimbo iliyo na nenosiri la plaintext "`secret`", tuna toleo lililofanyiwa hashing pekee.

///

<img src="/img/tutorial/security/image08.png">

Ita endpoint `/users/me/`, utapata response kama hii:

```JSON
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "full_name": "John Doe",
  "disabled": false
}
```

<img src="/img/tutorial/security/image09.png">

Ukifungua zana za wasanidi programu, unaweza kuona jinsi data inayotumwa inavyojumuisha token pekee; nenosiri hutumwa tu katika request ya kwanza ili kuthibitisha utambulisho wa mtumiaji na kupata access token hiyo, lakini si baada ya hapo:

<img src="/img/tutorial/security/image10.png">

/// note | Tanbihi

Angalia header ya `Authorization`, yenye thamani inayoanza na `Bearer `.

///

## Matumizi ya kiwango cha juu yenye `scopes` { #advanced-usage-with-scopes }

OAuth2 ina dhana ya "scopes".

Unaweza kuzitumia kuongeza seti mahususi ya ruhusa kwenye token ya JWT.

Kisha unaweza kumpa token hii mtumiaji moja kwa moja au mhusika mwingine, ili kuwasiliana na API yako kwa kuzingatia vikwazo fulani.

Unaweza kujifunza jinsi ya kuzitumia na jinsi zilivyounganishwa katika **FastAPI** baadaye katika **Mwongozo wa Mtumiaji wa Kiwango cha Juu**.

## Muhtasari { #recap }

Kwa ulichokiona hadi sasa, unaweza kuandaa programu salama ya **FastAPI** kwa kutumia viwango kama OAuth2 na JWT.

Katika karibu framework yoyote, kushughulikia usalama huwa jambo changamano kwa haraka.

Package nyingi zinazorahisisha jambo hili kwa kiasi kikubwa hulazimika kuweka vikwazo vingi kwenye data model, hifadhidata, na vipengele vinavyopatikana. Na baadhi ya package hizi zinazorahisisha mambo kupita kiasi kwa kweli zina kasoro za usalama zisizoonekana wazi.

---

**FastAPI** haiweki vikwazo kwenye hifadhidata yoyote, data model au zana yoyote.

Inakupa uhuru kamili wa kuchagua zile zinazofaa zaidi mradi wako.

Na unaweza kutumia moja kwa moja package nyingi zinazotunzwa vizuri na kutumiwa sana kama `pwdlib` na `PyJWT`, kwa sababu **FastAPI** haihitaji mifumo yoyote changamano ili kuunganisha package za nje.

Lakini inakupa zana za kurahisisha mchakato kadiri iwezekanavyo bila kupunguza unyumbufu, uimara, au usalama.

Na unaweza kutumia na kutekeleza itifaki salama, za kawaida, kama OAuth2 kwa njia rahisi kwa kiasi.

Unaweza kujifunza zaidi katika **Mwongozo wa Mtumiaji wa Kiwango cha Juu** kuhusu jinsi ya kutumia "scopes" za OAuth2, ili kupata mfumo wenye udhibiti wa ruhusa wa kina zaidi, kwa kufuata viwango hivi hivi. OAuth2 yenye scopes ni utaratibu unaotumiwa na watoa huduma wengi wakubwa wa uthibitishaji wa utambulisho, kama Facebook, Google, GitHub, Microsoft, X (Twitter), n.k. kuidhinisha programu za wahusika wengine kuwasiliana na API zao kwa niaba ya watumiaji wao.
