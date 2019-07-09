# -*- encoding: utf-8 -*-


PYCAKE_SETTINGS = '.pycake'


class _AppSettings(object):
    __slots__ = []
    _d = {}

    def __init__(self, *args, **kwargs):
        super(_AppSettings, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        return self._d.get(self.__class__.__uniform_key__(name), None)

    def __setattr__(self, name, val):
        self._d[self.__class__.__uniform_key__(name)] = val

    def __getitem__(self, name, default=None):
        return self._d.get(self.__class__.__uniform_key__(name), default)

    def __setitem__(self, name, val):
        self._d[self.__class__.__uniform_key__(name)] = val

    @classmethod
    def get(cls, name, default=None):
        return cls._d.get(cls.__uniform_key__(name), default)

    @classmethod
    def __uniform_key__(cls, name):
        return name.replace('.', '_')

    @classmethod
    def json(cls):
        return cls._d.copy()


def build_app_config(): # noqa
    app_settings = _AppSettings()
    _ = {}

    with open(PYCAKE_SETTINGS, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        exec(
            file_contents.replace('.', '_'),
            globals(),
            _
        )

    for k, v in _.items():
        app_settings[k] = v

    return app_settings
