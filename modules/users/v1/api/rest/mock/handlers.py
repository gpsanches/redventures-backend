# -*- encoding: utf-8 -*-

import logging
import random
from application.src.rewrites import APIHandler

# Log
log = logging.getLogger(__name__)

# Settings
partner_name = 'users'
api_version = 'v1/mock'


class MockHandler(APIHandler):
    __urls__ = [r"/{0}/{1}/name".format(partner_name, api_version),
                r"/{0}/{1}/name/".format(partner_name, api_version)]

    def get(self):

        names = ["Murilo", "Marcio", "Guilherme"]
        sizes = [22, 18, 11]

        return self.success({"success": 1, "name": random.choice(names), "size": random.choice(sizes)})
