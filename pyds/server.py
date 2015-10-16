#! /usr/bin/env python
# *-* coding: utf8 *-*

import json
import os
import subprocess

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.process
import tornado.autoreload
from tornado.options import define, options

from tornado_json.requesthandlers import APIHandler

define('version', default=None, help='Version settings')
define('debug', default=False, help='Debug mode')
define('port', default=7070, help='Port')
define('config', default='pyds.conf', help='Configuration file')

SERVERS = {}


class MainHandler(APIHandler):
    def get(self):
        if 'tag' in self.request.arguments:
            result = {}
            for tag in self.request.arguments['tag']:
                result[tag] = SERVERS.get(tag)
        else:
            result = SERVERS
        self.write(json.dumps(result))
        self.flush()

    def post(self, *args, **kwargs):
        try:
            body = json.loads(self.request.body)
        except ValueError as e:
            raise tornado.web.HTTPError(400, log_message=str(e))
        SERVERS.update(body)


class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler)
        ]

        tornado.web.Application.__init__(
            self,
            handlers
        )

def serve():
    tornado.options.parse_command_line()
    if os.path.exists(options.config):
        tornado.options.parse_config_file(options.config)

    http_server = tornado.httpserver.HTTPServer(App())
    http_server.listen(options.port)
    if options.debug:
        tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
