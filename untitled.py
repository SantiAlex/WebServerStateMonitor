import tornado
from tornado import web,gen


class AsyncResponseHandler():
    @web.asynchronous
    @gen.coroutine
    def get(self):

        url = 'https://api.github.com/'
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = yield tornado.gen.Task(http_client.fetch, url)
        print(response.code)
        print(response.body)

a=AsyncResponseHandler()
a.get()