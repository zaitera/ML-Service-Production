from os import environ

import redis
import orjson
cache = redis.Redis(host=environ['HOST'], port=6379, username=environ['MASTER_USER'],
                    password=environ['REDIS_MASTER_PW'])


def str2bool(string):
    try:
        return string.lower() in ("y", "yes", "true", "t", "1")
    except:
        return False


def get_last_post_request_body():
    post_request_body = cache.get(f"post_request_body")
    return orjson.loads(post_request_body) if post_request_body is not None else ""


def set_post_request_body(post_request_body):
    cache.set(f"post_request_body", orjson.dumps(post_request_body))


def get_last_request_random():
    last_rand_value = cache.get(f"last_request_value")
    return int(last_rand_value) if last_rand_value is not None else 0


def set_request_random(last_request_value):
    cache.set(f"last_request_value", last_request_value)


def validate_already_ran_init_flag():
    result = cache.get(f"already_ran")
    if result is None:
        raise ValueError("Did you init the service")
    return bool(result)


def set_already_ran_init_flag():
    cache.set(f"already_ran", "True")

