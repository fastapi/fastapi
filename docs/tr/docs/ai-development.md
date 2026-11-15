# Yapay Zekâ ile Geliştirme { #develop-with-ai }

FastAPI, Python paketiyle birlikte gelen resmî bir **agent skill** (ajan becerisi) içerir. Bu skill, projenizde kurulu sürüme yönelik rehberlik sağlar.

## Skill'i Yükleyin { #install-the-skill }

[FastAPI'ı yükledikten](tutorial/index.md#install-fastapi) sonra proje dizininizde [Library Skills](https://library-skills.io/use/) aracını çalıştırın:

```bash
uvx library-skills
```

FastAPI skill'ini seçin. Codex ve çoğu ajan için `.agents/skills`, Claude Code için ise `.claude/skills` dizinini seçin. İkisini birden de seçebilirsiniz.

Böylece ajanınız FastAPI kodu üzerinde çalışırken bu skill'i otomatik olarak kullanabilir.

### Etkileşimli Onay Olmadan Yükleme { #install-without-prompts }

Ajanlar ve betikler için FastAPI skill'ini etkileşimli sorular olmadan seçip yükleyin:

```bash
uvx library-skills install --skill fastapi --yes
```

Claude Code için skill'i ayrıca `.claude/skills` dizinine yüklemek üzere `--claude` ekleyin:

```bash
uvx library-skills install --skill fastapi --yes --claude
```

## Uygulamanızı Yapılandırın { #configure-your-app }

FastAPI araçlarının uygulamanızı bulabilmesi için `pyproject.toml` dosyasında [uygulamanın giriş noktasını](fastapi-cli.md#configure-the-app-entrypoint-in-pyproject-toml) yapılandırın:

```toml
[tool.fastapi]
entrypoint = "main:app"
```

Uygulamanızın modül ve değişken adını kullanın. Burada `main:app`, `main.py` dosyasındaki `app` nesnesini ifade eder.

## Uygulamanızı Çalıştırın { #run-your-app }

Yerel geliştirme için [FastAPI CLI](fastapi-cli.md) kullanın:

```bash
uv run fastapi dev
```

Üretim ortamında `uv run fastapi run` kullanın.

## SDK Oluşturun { #generate-an-sdk }

Frontend ve API istemcisi geliştirmek için [SDK Oluşturma](advanced/generate-clients.md) sayfasına bakın.

## Uygulamanızı Yayına Alın { #deploy-your-app }

Uygulamanızı FastAPI ekibinin resmî, yönetilen dağıtım platformu olan [FastAPI Cloud](deployment/fastapicloud.md) üzerinde yayına almak için:

```bash
uv run fastapi deploy
```

Başka bir bulut sağlayıcısında veya kendi sunucunuzda [manuel olarak dağıtım](deployment/manually.md) da yapabilirsiniz.

## Ajan Eklentileri { #agent-plugins }

[Codex ve Claude Code için FastAPI Cloud eklentileri](https://fastapicloud.com/docs/other-resources/coding-agent-plugins/), proje oluşturmaya ve bağımlılıklarınızla birlikte gelen kütüphane skill'lerini kullanmaya yönelik talimatlar içerir. FastAPI Cloud kullanmasanız bile bu eklentilerden yararlanabilirsiniz.

Bu eklentiler ayrıca FastAPI Cloud üzerinde dağıtımı, log'ları ve ortam değişkenlerini de kapsar.
