import os


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


API_V1_STR = "/api/v1"

SECRET_KEY = os.getenvb(b"SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days

SERVER_NAME = os.getenv("SERVER_NAME")
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://dev.couchbase-project.com, https://stag.couchbase-project.com, https://couchbase-project.com, http://local.dockertoolbox.tiangolo.com"
PROJECT_NAME = os.getenv("PROJECT_NAME")
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Couchbase server settings
COUCHBASE_MEMORY_QUOTA_MB = os.getenv("COUCHBASE_MEMORY_QUOTA_MB", "256")
COUCHBASE_INDEX_MEMORY_QUOTA_MB = os.getenv("COUCHBASE_INDEX_MEMORY_QUOTA_MB" "256")
COUCHBASE_FTS_MEMORY_QUOTA_MB = os.getenv("COUCHBASE_FTS_MEMORY_QUOTA_MB", "256")
COUCHBASE_HOST = os.getenv("COUCHBASE_HOST", "couchbase")
COUCHBASE_PORT = os.getenv("COUCHBASE_PORT", "8091")
COUCHBASE_FULL_TEXT_PORT = os.getenv("COUCHBASE_FULL_TEXT_PORT", "8094")
COUCHBASE_ENTERPRISE = getenv_boolean("COUCHBASE_ENTERPRISE")
COUCHBASE_USER = os.getenv("COUCHBASE_USER", "Administrator")
COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD", "password")
COUCHBASE_BUCKET_NAME = os.getenv("COUCHBASE_BUCKET_NAME", "app")

COUCHBASE_SYNC_GATEWAY_HOST = os.getenv("COUCHBASE_SYNC_GATEWAY_HOST", "sync-gateway")
COUCHBASE_SYNC_GATEWAY_PORT = os.getenv("COUCHBASE_SYNC_GATEWAY_PORT", "4985")
COUCHBASE_SYNC_GATEWAY_USER = os.getenv("COUCHBASE_SYNC_GATEWAY_USER")
COUCHBASE_SYNC_GATEWAY_PASSWORD = os.getenv("COUCHBASE_SYNC_GATEWAY_PASSWORD")
COUCHBASE_SYNC_GATEWAY_DATABASE = os.getenv("COUCHBASE_SYNC_GATEWAY_DATABASE")

# Couchbase query timeouts
COUCHBASE_DURABILITY_TIMEOUT_SECS = 60.0
COUCHBASE_OPERATION_TIMEOUT_SECS = 30.0
COUCHBASE_N1QL_TIMEOUT_SECS = 300.0


# Couchbase Sync Gateway settings
COUCHBASE_CORS_ORIGINS = os.getenv("COUCHBASE_CORS_ORIGINS")
# a string of origins separated by commas, e.g: "http://localhost:5984, http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://dev.couchbase-project.com, https://stag.couchbase-project.com, https://db.stag.couchbase-project.com, https://couchbase-project.com, https://db.couchbase-project.com, http://local.dockertoolbox.tiangolo.com, http://local.dockertoolbox.tiangolo.com:5984"
COUCHBASE_AUTH_TIMEOUT = ACCESS_TOKEN_EXPIRE_MINUTES * 60

COUCHBASE_FULL_TEXT_INDEX_DEFINITIONS_DIR = "/app/app/search_index_definitions/"

SMTP_TLS = getenv_boolean("SMTP_TLS", True)
SMTP_PORT = None
_SMTP_PORT = os.getenv("SMTP_PORT")
if _SMTP_PORT is not None:
    SMTP_PORT = int(_SMTP_PORT)
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAILS_FROM_EMAIL = os.getenv("EMAILS_FROM_EMAIL")
EMAILS_FROM_NAME = PROJECT_NAME
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 48
EMAIL_TEMPLATES_DIR = "/app/app/email-templates/build"
EMAILS_ENABLED = SMTP_HOST and SMTP_PORT and EMAILS_FROM_EMAIL

ROLE_SUPERUSER = "superuser"

FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

USERS_OPEN_REGISTRATION = getenv_boolean("USERS_OPEN_REGISTRATION")
