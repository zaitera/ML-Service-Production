redis_password = "TEMPLATE_CELERY_PW"
host = "redis"
broker_url = f"redis://:{redis_password}@{host}:6379/0"
result_backend = f"redis://:{redis_password}@{host}:6379/0"
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
