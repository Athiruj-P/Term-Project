from datetime import date , datetime
today = date.today()
date_folder = today.strftime("%Y-%m-%d")

dict_config = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s:%(name)s] {%(funcName)s:%(lineno)d} [SYSTEM]:%(message)s',
        },
        'user': {
            'format': '%(asctime)s [%(levelname)s:%(name)s] {%(funcName)s:%(lineno)d} [USER]:%(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "log/{}.log".format(date_folder),
            'maxBytes': 10000000,
            'backupCount': 10
        },
        'user': {
            'level': 'DEBUG',
            'formatter': 'user',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "log/{}.log".format(date_folder),
            'maxBytes': 10000000,
            'backupCount': 10
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'main': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'model_management_api': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'MLManager_obj': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'log_management_api': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'LogManager': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'Login_api': {
            'handlers': ["default"],
            'level': 'DEBUG',
        },
        'user_management' : {
            'handlers': ["user"],
            'level': 'DEBUG',
        },
        'image_measurement' : {
            'handlers': ["user"],
            'level': 'DEBUG',
        },
        'image_processing_api' : {
            'handlers': ["user"],
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ["console"],
        'level': 'DEBUG',
    },
}