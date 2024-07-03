INSTALLED_APPS = ["polls"]

ROOT_URLCONF = "mysite.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}
