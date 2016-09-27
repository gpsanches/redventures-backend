# -*- encoding: utf-8 -*-

from application.src.rewrites import APIHandler
# from application.src.models import Config
from application.src.auth import internal
from application.src import utils


class ConfigHandler(APIHandler):
    """
    This API is used to CRUD application configs.
    """
    __urls__ = [r"/config", r"/config/"]

    @internal
    def get(self):
        db = self.application.db
        configs = utils.get_config_map(db.query(Config).all())
        return self.success(configs)

    @internal
    def post(self):
        db = self.application.db

        key = self.get_argument('key', None, strip=True)
        value = self.get_argument('value', None, strip=True)

        if not key or not value:
            return self.error({"message": "Key or Value not found"})

        config = db.query(Config).filter_by(key=key).all()

        if config:
            return self.error({"message": "Key {0} already in use, try update it with PUT method".format(key)})

        config = Config(key=key, value=value)

        try:
            db.begin()
            db.add(config)
            db.commit()

            return self.success({"message": "{0}:{1} successfully added".format(key, value)})
        except Exception as e:
            db.rollback()
            return self.error({"message": "Could not add config."})

    @internal
    def put(self):
        db = self.application.db

        key = self.get_argument('key', None, strip=True)
        value = self.get_argument('value', None, strip=True)

        if not key or not value:
            return self.error({"message": "Key or Value not found"})

        try:
            config = db.query(Config).filter_by(key=key).one()
            config.value = value
        except Exception as e:
            return self.error({"message": "Key not in use, try create it with POST method"})

        try:
            db.begin()
            db.add(config)
            db.commit()

            return self.success({"message": "{0}:{1} successfully updated".format(key, value)})
        except Exception as e:
            db.rollback()
            return self.error({"message": "Could not update config."})

    @internal
    def delete(self):
        db = self.application.db
        key = self.get_argument('key', None, strip=True)

        if not key:
            return self.error({"message": "Key not found"})

        try:
            config = db.query(Config).filter_by(key=key).one()

            db.begin()
            db.delete(config)
            db.commit()

            return self.success({"message": "{0} successfully removed".format(key)})
        except Exception as e:
            db.rollback()
            return self.error({"message": "Could not delete"})


class ConfigCacheHandler(APIHandler):
    """
    This API is used to CRUD application cached configs.
    """
    __urls__ = [r"/config/cache", r"/config/cache/"]

    @internal
    def get(self):
        configs = self.application.settings['config']
        return self.success(configs)

    @internal
    def post(self):
        db = self.application.db
        self.application.settings['config'] = utils.get_config_map(db.query(Config).all())
        return self.success({"message": "Config cache successfully updated"})
