import logging
from logging.handlers import RotatingFileHandler

import flask

from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from secrets import token_urlsafe
from .controller import controller
from .celery import celery

# noinspection PyArgumentList
logging.basicConfig(level=logging.DEBUG,
                    handlers=[RotatingFileHandler('./info.log', maxBytes=1024 * 1024, backupCount=1)])
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config["JWT_SECRET_KEY"] = token_urlsafe(32)
jwt = JWTManager(app)


@jwt.invalid_token_loader
def local_invalid_token_callback(__):
    return {"status": "Invalid token"}, 401


@jwt.expired_token_loader
def local_expired_token_callback(__, ___):
    return {"status": "Expired token"}, 401


@celery.task(bind=True, track_started=True)
def async_init(self):
    app.logger.debug("STARTED ASYNC")
    self.update_state(state="STARTED")
    result = controller.full_init()
    self.update_state(state="SUCCESS")
    return result


@app.route('/resource/init', methods=['GET'])
@jwt_required()
def handle_get():
    is_async = flask.request.args.get('async')
    if controller.datautil.str2bool(is_async):
        task = async_init.apply_async()
        return '', 202, {'Location': flask.url_for('task_status', task_id=task.id, _external=True)}
    else:
        return controller.full_init()


@app.route('/resource/predict', methods=['POST'])
@jwt_required()
def handle_post():
    app.logger.debug(flask.request.data.decode("utf-8"))
    return controller.predict(flask.request.data)


@app.route('/resource/auth', methods=['GET'])
def handle_token_gen():
    username = flask.request.authorization["username"]
    password = flask.request.authorization["password"]
    return controller.create_token_if_credentials_are_valid(username, password)


@app.route('/resource/task/status/<task_id>')
def task_status(task_id):
    return controller.check_task_status(celery, task_id)
