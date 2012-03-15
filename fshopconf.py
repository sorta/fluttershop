from os import path


class FSSettings:

    def __init__(self, current_dir):

        self._current_dir = current_dir
        self._standard_settings = {}

        self._global_settings = {
            'global': {
                'server.socket_port': 8080,
                'server.socket_host': "127.0.0.1",
                'server.socket_queue_size': 5,
                'server.protocol_version': "HTTP/1.0",
                'server.log_to_screen': True,
                'server.reverse_dns': False,
                'server.thread_pool': 10,
                'server.environment': "development"
            },
        }

        self.add_resource("bootstrap", "css", "bootstrap.css", ["bootstrap"])
        self.add_resource("bootstrap", "js", "bootstrap.js", ["bootstrap"])
        self.add_resource("fshop", "css", "ws1.css")
        self.add_resource("jquery", "js", "jquery-1.7.1.min.js")

    def add_resource(self, output_name, resource_type, filename, extra_dirs=None):

        working_path = path.join(self._current_dir, "static")
        if extra_dirs:
            for d in extra_dirs:
                working_path = path.join(working_path, d)

        working_path = path.join(working_path, resource_type, filename)

        self._standard_settings['/{0}/{1}.{0}'.format(resource_type, output_name)] = {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': working_path
        }

    @property
    def global_settings(self):
        return self._global_settings

    @property
    def standard_settings(self):
        return self._standard_settings
