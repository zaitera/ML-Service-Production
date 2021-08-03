if __name__ == "__main__":
    from os import environ
    environ["HOST"] = "localhost"
    environ["MASTER_USER"] = ""
    environ["REDIS_MASTER_PW"] = ""
    environ["REDIS_CELERY_PW"] = ""
    from app.app import app
    app.run(host="0.0.0.0")
    pass
