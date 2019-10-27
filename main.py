"""
Things that can be improved:
- Saving uploaded file in a temp folder using chunks (To avoid run out of memory when too big files)
"""
import os
import cherrypy
from WebServer import WebServer, WebServerAPI

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
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.config.update(server_conf)

    webapp = WebServer()
    webapp.load_csv = WebServerAPI()
    cherrypy.quickstart(webapp, '/', app_conf)
