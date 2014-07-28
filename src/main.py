# -*- coding: utf-8 *-*
import tornado.ioloop
import tornado.web
import processor


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("Feed requested")
        p = processor.Processor()
        xml = p.Parse(u"http://some_url_from_parameter")
        self.write(xml)
        print("Feed sended")
        #print "Request coming..."
        #self.write("Hello")
        #print "Reply sended."

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    p = processor.Processor()
    p.Parse(u"http://some_url_for_test")
    print "Initializing"
    #application.listen(8888)
    #tornado.ioloop.IOLoop.instance().start()
    print "Stopped"
