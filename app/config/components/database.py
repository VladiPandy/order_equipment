DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        #'HOST': 'host.docker.internal',
        'HOST': '80.209.240.64',
        'PORT': 5442,
        'OPTIONS': {
           'options': '-c search_path=public,timesheets'
        }
    }
}

