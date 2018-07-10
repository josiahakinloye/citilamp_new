DEBUG = False

ALLOWED_HOSTS = ['localhost', 'citilamp.com', 'paypal.com', '*.paypal.com', 'bitpay.com', 'test.bitpay.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'techneti_citilamp_prod',
        'USER': 'techneti_clamp',
        'PASSWORD': 'Winteriscoming',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_URL = 'https://technetium.io/citilamp/static/'
STATIC_ROOT = '/home/techneti/www/citilamp/static/'
MEDIA_URL = 'https://technetium.io/citilamp/media/'
MEDIA_ROOT = '/home/techneti/www/citilamp/media/'

# Social login settings
SOCIAL_AUTH_FACEBOOK_KEY = '198679870931069'
SOCIAL_AUTH_FACEBOOK_SECRET = '515703354e580ae34d179f606e9a25cd'
SOCIAL_AUTH_TWITTER_KEY = 'zxkrtT2vtcN32RRCud5PTGqo9'
SOCIAL_AUTH_TWITTER_SECRET = 'yYTwUMsgEHp5jymJALWPNiWW9IxZkPlVOudIAkHiSI2Q4VRlAv'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '770740800446-kmn2255pbi0qmrtafaqi980lgfuus90m.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ZVMlgWt7VO8ScDTnfx0YBSUD'

NEWS_API_KEY = '2c49a8924d2341d3b99f22f819103504'

WEATHER_API_KEY = 'ce8d100afc7c4f17ab5181645181901'

GOOGLE_MAPS_KEY = 'AIzaSyCX35UUsEn5Q2duK_j674X-dSp-Xng5W_E'

IPSTACK_API_KEY = '53b893b7ac2a6e2ba8373815f9b93d7e'

BITPAY_API_KEY_FILE = '/home/techneti/private.pem'
BITPAY_API_TOKEN = 'AztRA3UCDY8h9Ck2iJWgS9PK5YE9KTvcZmYAf2KCR1Fc'

AMADEUS_API_KEY = "upLiGgUIJEpboZQW5R1yztAPoSNrea5V"
