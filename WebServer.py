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
            'algorithms': engine.getAlgorithms(),
            'default_datasets': engine.getAllDefaultDatasets()
        })


@cherrypy.expose
class SetOptionsService(object):
    @cherrypy.tools.accept(media='text/plain')
    def POST(self, options):
        """ Use the options selected by the user to execute all algorithms
        :param options: {
                    is_default_dataset: bool,
                    dataset: str,
                    providers: []
                    algorithms: []
                    target: str
                }
       if is_default_dataset is true, dataset will contain the name of the default_dataset"""

        options_dic = json.loads(options)

        return engine.execute(options_dic['is_default_dataset'], options_dic['dataset'], options_dic['providers'],
                              options_dic['algorithms'],
                              options_dic['target'])


@cherrypy.expose
@cherrypy.tools.json_out()
class GetDefaultDatasetHeadersService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, default_dataset_name):
        return {'headers': engine.getDefaultDatasetHeaders(default_dataset_name)}
