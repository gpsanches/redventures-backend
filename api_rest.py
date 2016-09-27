# -*- encoding: utf-8 -*-

import logging
import importlib
import logging.config
import tornado.ioloop
from tornado.options import define, options
from tornado.httpserver import HTTPServer
from application.src.rewrites import Application, get_routes
import application.settings as app_settings


# Options
define("port", default=8888, help="run on the given port", type=int)
define("module", default="", help="run the given module", type=str)

# Initializing
if __name__ == "__main__":
    tornado.options.parse_command_line()

    if not options.module:
        print("You must give the parameter --module.")
        exit()

    # Logs
    logging.config.dictConfig(app_settings.LOGGING)

    # Routes
    routes = []
    for module in app_settings.REST_MODULES:
        if 'application' in module or options.module in module:
            routes += get_routes(__import__(module))

    # Databases
    module_databases = importlib.import_module("modules.{0}.v1.utils.databases".format(options.module))
    db_connections = module_databases.get_db_connections()

    # Settings
    module_settings = importlib.import_module("modules.{0}.v1.utils.settings".format(options.module))
    try:
        settings = module_settings.get_settings(db_connections)
    except Exception as e:
        print("An error occurred while configuring module settings: {0}.".format(e))
        exit()

    # App
    app = Application(
        routes,
        db=db_connections,
        settings=settings
    )

    # Start tornado with multiple processes
    server = HTTPServer(app)
    server.bind(int(options.port))
    server.start(int(app_settings.TORNADO_SOCKETS))

    tornado.ioloop.IOLoop.instance().start()
