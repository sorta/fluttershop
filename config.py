
# import ConfigParser
from bottle import template, functools, DictMixin


SITE_NAME = 'Sorta Software'
HOST_ADDRESS = '127.0.0.1'
HOST_PORT = '8080'
AUTORELOAD = True
DEBUG = False


#### Config ####
# def read_config_from_file(path='fshop.conf'):
#     def_conf = {
#         'site_name': 'Flutter Shop',
#         'host_address': '127.0.0.1',
#         'host_port': '80',
#         'autoreload': True,
#         'debug': False
#     }
#     conf = ConfigParser.RawConfigParser(def_conf)
#     conf.read(path)
#     return {
#         'site_name': conf.get('general', 'site_name'),
#         'host_address': conf.get('general', 'host_address'),
#         'host_port': conf.get('general', 'host_port'),
#         'autoreload': conf.getboolean('general', 'autoreload'),
#         'debug': conf.getboolean('general', 'debug')
#     }


def my_view(tpl_name, **defaults):
    ''' Decorator: renders a template for a handler.
        The handler can control its behavior like that:

          - return a dict of template vars to fill out the template
          - return something other than a dict and the view decorator will not
            process the template, but return the handler result as is.
            This includes returning a HTTPResponse(dict) to get,
            for instance, JSON with autojson or other castfilters.
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (dict, DictMixin)):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, site_name=SITE_NAME, **tplvars)
            return result
        return wrapper
    return decorator
