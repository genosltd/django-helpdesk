import pathlib

BASE_DIR = pathlib.Path(__file__).parent

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "test_app",
    "django_helpdesk",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
