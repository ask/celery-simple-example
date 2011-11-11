BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IMPORTS = ('tasks', )

CELERY_RESULT_BACKEND = 'amqp'
CELERY_RESULT_PERSISTENT = True
CELERY_TASK_RESULT_EXPIRES = None

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    'default': {
        'binding_key': 'task.#',
    },
    'compute': {
        'binding_key': 'compute.#',
    },
    'result': {
        'binding_key': 'result.#',
    },
}
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'
CELERY_ROUTES = {
    'tasks.compute': {
        'queue': 'compute',
        'routing_key': 'compute.a_result'
    },
    'tasks.handle_result': {
        'queue': 'result',
        'routing_key': 'result.handle',
    },
}
