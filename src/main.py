# -*- coding: utf-8 *-*
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import processor


class MainHandler(RequestHandler):
    def get(self):
        self.write("FeedFilter")


class FilterHandler(RequestHandler):
    def get(self, url):
        p = processor.Processor()
        xml = p.Parse(url)
        self.write(xml)

application = Application([
    url(r"/", MainHandler),
    url(r"/filter/(.*)", FilterHandler, name="filter")
])

if __name__ == "__main__":
    application.listen(9356)
    IOLoop.instance().start()

