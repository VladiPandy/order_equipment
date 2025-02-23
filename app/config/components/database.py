DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'db',
        #'HOST': 'host.docker.internal',
        'HOST': 'localhost',
        'PORT': 5442,
        'OPTIONS': {
           'options': '-c search_path=public,timesheets'
        }
    }
}

