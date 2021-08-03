from .datautil import datautil
from datetime import timedelta
import re
import orjson
from configparser import RawConfigParser
from flask_jwt_extended import create_access_token
import time
from random import randint
config = RawConfigParser()
config.read('./config.properties')
EXPIRY = config.get('auth_info', 'expiry')
EXPIRY_TIME_UNIT = config.get('auth_info', 'expiry_time_unit')

domain_regex = re.compile(".+@gmail.com")
email_regex = re.compile("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")

ACCESS_TOKEN_EXPIRY = timedelta(**{EXPIRY_TIME_UNIT: float(EXPIRY)})


def full_init():
    try:
        # Init and train your service here, this code emulates this with a big delay
        time.sleep(90)
        datautil.set_already_ran_init_flag()
        return "", 204
    except BaseException as e:
        return {"status": f"{type(e).__name__} - {str(e)}"}, 500


def predict(data):
    try:
        # Retrieve your trained model from the redis database and use it to estimate the given values
        # This process is emulated by saving and retrieving data to the redis database.
        # Also it checks if the initialization/training ran already

        datautil.validate_already_ran_init_flag()
        last_json = datautil.get_last_post_request_body()
        last_rand = datautil.get_last_request_random()

        json_data = orjson.loads(data)
        datautil.set_post_request_body(json_data)

        result = randint(1, 100)
        datautil.set_request_random(result)

        return {
            "current_random": result,
            "current_post_json": json_data,
            "last_post_json": last_json,
            "last_random": last_rand
        }
    except ValueError as ve:
        return {"status": "Did you init the service"}, 424
    except BaseException as e:
        return {"status": f"{type(e).__name__} - {str(e)}"}, 500


def create_token_if_credentials_are_valid(username, password):
    if bool(email_regex.match(username)) and bool(domain_regex.match(username)):
        access_token = create_access_token(identity=f"{username}:{password}", expires_delta=ACCESS_TOKEN_EXPIRY)
        return {"token": access_token}
    else:
        return {"status": "Bad username or password"}, 401


def check_task_status(celery, task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        return {
            'done': False,
            'status': 'Pending...'
        }
    elif task.state == 'STARTED':
        return {
            'done': False,
            'status': 'In progress...'
        }
    elif task.state != 'FAILURE':
        return {
            'done': True,
            'status': "Done"
        }
    else:
        return {
            'done': False,
            'status': str(task.info),  # this is the exception raised
        }
