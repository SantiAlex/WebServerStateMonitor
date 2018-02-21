import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

task_list = []

def task():
    print("task...")

def task1():
    print("task1111...")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        t1 = tornado.ioloop.PeriodicCallback(task, 1000)  # 1秒为周期
        t2 = tornado.ioloop.PeriodicCallback(task1, 2000)  # 2秒为周期
        task_list.append(t1)
        task_list.append(t2)
        for i in task_list:
            i.start()
        # tornado.ioloop.IOLoop.instance().start()
        # self.write()

class StopHandler(tornado.web.RequestHandler):
    def get(self):
        for i in task_list:
            if i.is_running():
                print(str(i.is_running()))
                i.stop()
        self.write("stop")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler),(r"/s", StopHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()