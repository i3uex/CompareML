import json

import cherrypy

import engine


class WebServer(object):
    @cherrypy.expose
    def index(self):
        return open('public/index.html', encoding='utf-8')


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
        """:param options: dataset, providers and algorithms selected by user.
        Example: {"providers":["p1","p2"], "algorithms":["a1","a2","a3"], "target": "target_feature" )"""
        options_dic = json.loads(options)

        return engine.execute(options_dic['dataset'], options_dic['providers'], options_dic['algorithms'],
                              options_dic['target'])
