# -*- coding: utf-8 *-*
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from tornado import log
import logging
import Filter
import Settings
import Cache
import os
import json
import Log
import time

class MainHandler(RequestHandler):
    def get(self):
        self.write("FeedFilter")


class FilterHandler(RequestHandler):
    def get(self, name):
        settings = Settings.Settings()
        url = settings.getItem(name)[0]
        blacklist = settings.getItem("blacklist")
        p = Filter.Processor(blacklist)
        xml = p.Parse(url)
        self.set_header("Content-Type", "text/xml; charset=utf-8")
        self.write(xml)

class CacheHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._cache = Cache.Cache()
        return super(CacheHandler, self).__init__(application, request, **kwargs)

    def get(self):
        items = self._cache.get()
        self.render(os.path.join("templates", "cache.html"), title="Cache", items=items)

class LogHandler(RequestHandler):
    def get(self, count):
        items = logInstance.get(count)
        self.render(os.path.join("templates", "log.html"), title="Log", items=items)

class SettingsHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._settings = Settings.Settings()
        return super(SettingsHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self._render()

    def _render(self):
        self.render(os.path.join("templates", "settings.html"), title="Settings")

class SettingsServiceHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._settings = Settings.Settings()
        return super(SettingsServiceHandler, self).__init__(application, request, **kwargs)

    def get(self):
        self.write(self._getItems())

    def post(self):
        input = json.loads(self.request.body)
        self._settings.add(input["name"], input["value"])
        self.write(self._getItems())

    def delete(self):
        self._settings.delete(self.get_query_argument("name"))
        self.write(self._getItems())

    def _getItems(self):
        items = self._settings.get()
        return {"items": [{'name':i.name, 'value':i.value} for i in items]}


logInstance = Log.Log()

def LogRequest(handler):
    logInstance.add(handler.request._start_time, handler.request.remote_ip, handler.request.uri)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "log_function": LogRequest
}

application = Application([
    url(r"/", MainHandler),
    url(r"/filter/(.*)", FilterHandler, name="filter"),
    url(r"/cache/", CacheHandler, name="cache"),
    url(r"/log/(.*)", LogHandler, name="log"),
    url(r"/settings/", SettingsHandler, name="settings"),
    url(r"/api/settings", SettingsServiceHandler, name="settingsService"),
], **settings)


class LoggerHandler(logging.Handler):
    def emit(self, record):
        logInstance.add(time.time(), "error", self.format(record))

if __name__ == "__main__":
    application.listen(9357)
    logInstance.add(time.time(), "local", "Start")
    log.app_log.addHandler(LoggerHandler())
    IOLoop.instance().start()
    
