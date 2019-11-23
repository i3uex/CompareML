"""
Things that can be improved:
- Saving uploaded file in a temp folder using chunks (To avoid run out of memory when too big files)
- Thread use on execute different algorithms concurrently
"""
import os
import cherrypy
from WebServer import WebServer, LoadCsvService, GetOptionsService, SetOptionsService

if __name__ == '__main__':
    server_conf = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
    }

    app_conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
        },
        '/load_csv': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/get_options': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/set_options': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.config.update(server_conf)

    webapp = WebServer()
    webapp.load_csv = LoadCsvService()
    webapp.get_options = GetOptionsService()
    webapp.set_options = SetOptionsService()
    cherrypy.quickstart(webapp, '/', app_conf)
