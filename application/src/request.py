# -*- encoding: utf-8 -*-

from functools import wraps
from datetime import datetime
from application.src.celeryapp import CeleryApp, BaseTask
from application.src import utils
# from application.src.models import Request

# Celery App
# celery = CeleryApp.get_instance()


def request(func):
    """
    Saves incoming requests to database.
    """
    @wraps(func)
    def with_requests(self, *args):
        try:
            url = str(self.request.uri)
            header = str(utils.get_headers(self.request.headers))
            body = str(self.request.body.decode("utf-8"))
            date = datetime.now()
            db = self.application.db
            request_async.delay(url, header, body, date, db)
        except Exception as e:
            pass

        return func(self, *args)
    return with_requests


# @celery.task(base=BaseTask, name="application.request")
def request_async(url, header, body, date, db):
    """
    Saves request asynchronously.
    :param url: request URL
    :param header: request header
    :param body: request body
    :param date: request datetime
    :param db: database connection
    :return:
    """
    try:
        request = Request(url=url, header=header, body=body, date=date)

        try:
            db.begin()
            db.add(request)
            db.commit()
        except Exception as e:
            db.rollback()

    except Exception as e:
        request_async.apply_async(args=[url, header, body, date, db], queue='application.request.error')
