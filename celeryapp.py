# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from application.src.celeryapp import CeleryApp

# Celery App
celery_app = CeleryApp.get_instance()

# Starts Celery
celery_app.start()
