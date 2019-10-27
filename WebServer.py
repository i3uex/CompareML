import cherrypy


class WebServer(object):

    @cherrypy.expose
    def index(self):
        return open('public/index.html', encoding='utf-8')


@cherrypy.expose
class WebServerAPI(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, csv):
        cherrypy.log(csv)
        return 'ok'
