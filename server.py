import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import monitor
import auth
import os

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

task_list = []


def task():
    print("task...")


def task1():
    print(monitor.monitor)


class BaseHandler(tornado.web.RequestHandler):
    # def get_current_user(self):
    #     return self.get_secure_cookie("username")

    def prepare(self):
        print('come in ' + str(self.get_cookie("id")))

        if not auth.auth.check(self.get_cookie("id")):
            self.finish('{"code":1,"message":"need to login","data":{}}')

    @staticmethod
    def ok(data):
        return '{"code":0,"message":"ok","data":' + data + '}'


class LoginHandler(tornado.web.RequestHandler):

    def post(self):
        a = auth.auth.login(self.get_argument("username"), self.get_argument("password"))
        if a:
            self.set_cookie("id", a)
            # self.redirect("/app/console.html")
            self.write('{"code":1,"message":"seccess"}')
        else:
            self.write('{"code":0,"message":"wrong input"}')


class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/login")


#
# class IndexHandler(BaseHandler):
#     def get(self):
#         t1 = tornado.ioloop.PeriodicCallback(task, 1000)  # 1秒为周期
#         t2 = tornado.ioloop.PeriodicCallback(task1, 2000)  # 2秒为周期
#         task_list.append(t1)
#         task_list.append(t2)
#         for i in task_list:
#             i.start()
#             # tornado.ioloop.IOLoop.instance().start()
#             # self.write()
#
#
# class StopHandler(BaseHandler):
#     def get(self):
#         for i in task_list:
#             if i.is_running():
#                 print(str(i.is_running()))
#                 i.stop()
#         self.write("stop")


#
# txt = ''
#
#
# class ClientHandler(BaseHandler):
#     def get(self):
#         from tornado import httpclient
#
#         def handle_response(response):
#             if response.error:
#                 print("Error: %s" % response.error)
#
#             else:
#                 print(response.body)
#                 global txt
#                 txt = response.body.decode('utf-8')
#
#         http_client = httpclient.AsyncHTTPClient()
#         http_client.fetch("http://www.baidu.com/", handle_response)
#         self.write(txt)


class ListHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.list()))


class AddHandler(BaseHandler):

    def post(self):
        param = self.request.body.decode('utf-8')
        monitor.monitor.add(param)
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.list()))


class TaskHandler(BaseHandler):
    def get(self, task):
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.get(task)))

    def post(self, task):
        param = self.request.body.decode('utf-8')
        monitor.monitor.update(task, param)
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.get(task)))

    def delete(self, task):
        monitor.monitor.delete(task)
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.list()))


class ReportHandler(tornado.web.RequestHandler):
    def get(self, task):
        self.set_header("Content-Type", "application/json")
        self.write(monitor.monitor.report_whole(task))


class HasErrHandler(tornado.web.RequestHandler):
    def get(self, task):
        self.set_header("Content-Type", "application/json")
        self.write(monitor.monitor.report_has_err(task))


class InfoHandler(BaseHandler):
    def get(self, task):
        self.set_header("Content-Type", "application/json")
        self.write(self.ok(monitor.monitor.report_list_info(task)))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates/"),
        # "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        # "xsrf_cookies": True,
        # "login_url": "/login"
    }
    app = tornado.web.Application(
        handlers=[
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r"/tasks", ListHandler),
            (r"/tasks/add", AddHandler),
            (r"/tasks/(?P<task>[0-9a-z]*)", TaskHandler),
            (r"/report/whole/(?P<task>[0-9a-z]*)", ReportHandler),
            (r"/report/haserr/(?P<task>[0-9a-z]*)", HasErrHandler),
            (r"/report/info/(?P<task>[0-9a-z]*)", InfoHandler),
        ],
        static_path=os.path.join(os.path.dirname(__file__), "app"),
        static_url_prefix="/app/",
        **settings
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
