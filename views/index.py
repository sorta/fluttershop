import cherrypy
from mako.lookup import TemplateLookup
lookup = TemplateLookup(directories=['templates'])


def serve_template(templatename, **kwargs):
    mytemplate = lookup.get_template(templatename)
    return mytemplate.render(**kwargs)


class SECOND:

    @cherrypy.expose
    def index(self):
        return serve_template("index.html", data="Bam! Outsourced!")


class MainApp:

    @cherrypy.expose
    def index(self):
        return serve_template("index.html", data="Hello world!")

    @cherrypy.expose
    def nexter(self):
        return serve_template("index.html", data="IT WORKED GOOD JOB")

    leek = SECOND()
