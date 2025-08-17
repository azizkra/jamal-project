from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent



ALLOWED_HOSTS = ['127.0.0.1', '*']

# CART
CART_SESSION_ID = 'cart'

# AUTH USER MODEL
AUTH_USER_MODEL = 'account.CustomUser'
LOGIN_URL = '/account/login/'
LOGOUT_REDIRECT_URL = '/'

# APPLICATIONS
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'account.apps.AccountConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',

    # Third-party apps
    'rosetta',
    'parler',
    'localflavor',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL CONFIGURATION
ROOT_URLCONF = 'mysite.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'account.context_processors.theme_context',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'mysite.wsgi.application'


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
    ('de', _('German')),
    ('nl', _('Dutch')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'fr'},
        {'code': 'de'},
        {'code': 'nl'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}


# STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# EMAIL CONFIGURATION (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'        # ← ضع بريدك هنا
EMAIL_HOST_PASSWORD = 'your-app-password'      # ← ضع كلمة مرور التطبيق من Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# STRIPE CONFIGURATION
STRIPE_PUBLISHABLE_KEY = 'pk_test_51NdwGBLS8MylIruVBkoLxwCRLqQDOpq49woLbSUM3NsZ88cAjDH9RfuUPsg24otsRVrwucX8POHnt8EK5BHohGuC00BsWqrva2'
STRIPE_SECRET_KEY = 'sk_test_51NdwGBLS8MylIruVRWmZW2bn58rjJ1sxLPvCsJkHtLYz5PYBPVZTjDIIVuFbronIGaPWElJAo6FiIA9QjILhCKZo00MWrfJirn'
STRIPE_API_VERSION = '2022-08-01'
STRIPE_WEBHOOK_SECRET = 'whsec_b1ebdf3d075dbd96a0930e969160abe62d04560e2dc8cc682c0ff36df12f5d4d'

# STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
# STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
# STRIPE_API_VERSION = config('STRIPE_API_VERSION')
# STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET')

# SECURITY
SECRET_KEY = 'django-insecure-3gaqo97e_sskx*b4@z6kz2ew9k)0-0euouexc=9!e)vrnfea4u'
DEBUG=True

# SECRET_KEY = config('SECRET_KEY')
# DEBUG = config('DEBUG', default=False, cast=bool)

# DEFAULT PRIMARY KEY FIELD TYPE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


  