import json
import cherrypy
from Engine import Engine

engine = Engine()


class WebServer(object):

    @cherrypy.expose
    def index(self):
        return open('public/index.html', encoding='utf-8')


@cherrypy.expose
class LoadCsvService(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, csv: str):
        engine.setDataset(csv)
        return 'ok'


@cherrypy.expose
class GetOptionsService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return json.dumps({
            'providers': engine.getProviders(),
            'algorithms': engine.getAlgorithms()
        })


@cherrypy.expose
class SetOptionsService(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, options):
        cherrypy.log(options)
        options2 = json.loads(options)

        return ''
