INSTALLED_APPS = ["polls"]

ROOT_URLCONF = "mysite.urls"
USE_TZ = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}
