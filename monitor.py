import pickle
import jsonschema
import json
import time, hashlib, urllib
from tornado import httpclient
import tornado.ioloop


class Task(object):
    schema = {
        'type': 'object',
        'required': ['project', 'items', 'interval'],
        "additionalProperties": False,
        'properties': {
            'project': {
                'type': 'string',
                'minLength': 1,
                'pattern': '^[A-Za-z0-9\u4e00-\u9fa5]+$',
            },
            'auth': {
                'oneOf': [
                    {
                        'type': 'object',
                        'required': ['url', 'method'],
                        'properties': {
                            'url': {
                                'type': 'string',
                                'format': 'uri',
                            },
                            'method': {
                                'type': 'string',
                                'enum': ['get'],

                            },
                        },
                    },
                    {
                        'type': 'object',
                        'required': ['url', 'method', 'body'],
                        'properties': {
                            'url': {
                                'type': 'string',
                                'format': 'uri',
                            },
                            'method': {
                                'type': 'string',
                                'enum': ['post'],
                            },
                            'body': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'required': ['key', 'value'],
                                    'properties': {
                                        'key': {'type': 'string'},
                                        'value': {'type': 'string'},
                                    }
                                },
                            }
                        },
                    },
                ]

            },
            'items': {
                'type': 'array',
                "items": [{
                    'oneOf': [
                        {
                            'type': 'object',
                            'required': ['url', 'method'],
                            'properties': {
                                'url': {
                                    'type': 'string',
                                    'format': 'uri',
                                },
                                'method': {
                                    'type': 'string',
                                    'enum': ['get'],

                                },
                            },
                        },
                        {
                            'type': 'object',
                            'required': ['url', 'method', 'body'],
                            'properties': {
                                'url': {
                                    'type': 'string',
                                    'format': 'uri',
                                },
                                'method': {
                                    'type': 'string',
                                    'enum': ['post'],
                                },
                                'body': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'required': ['key', 'value'],
                                        'properties': {
                                            'key': {'type': 'string'},
                                            'value': {'type': 'string'},
                                        }
                                    },
                                }
                            },
                        },
                    ]
                }],
            },
            'interval': {
                'type': 'number',
            },
            'is_running': {
                'type': 'boolean'
            },

        }
    }

    def __init__(self, jsonData):
        try:
            jsonschema.validate(jsonData, Task.schema, format_checker=jsonschema.FormatChecker())
            self.structured_data = jsonData
            self.json_data = json.dumps(jsonData)

            print(self.structured_data)
            self.project = self.structured_data['project']
            self.auth = self.structured_data.get('auth')
            if self.auth:
                self.auth_method = self.auth['method']
                self.auth_url = self.auth['url']
                self.auth_body = {}
                if self.auth_method == 'post':
                    for i in self.auth['body']:
                        self.auth_body[i['key']] = i['value']

            self.items = []
            for i in self.structured_data.get('items'):
                self.items.append(RequestUrl(i))
            self.interval = self.structured_data['interval']

            self.is_running = self.structured_data['is_running']
            self.cookie = ''
            self.runner = tornado.ioloop.PeriodicCallback(self.do, self.interval * 1000 * 60)
            self.run()

        except Exception as e:
            print(e)
        pass

    def run(self):
        if self.is_running:
            self.do()

            if not self.runner.is_running():
                self.runner.start()
        else:
            if self.runner.is_running():
                self.runner.stop()

    def start(self):
        self.runner.start()

    def stop(self):
        self.runner.stop()

    def result(self):
        if not self.is_running:
            return ''
        r = 'ok'
        for i in self.items:
            print(i.state)
            if i.state != 200:
                r = 'err'
        return r

    def has_5(self):
        if not self.is_running:
            return ''
        for i in self.items:
            if 599 >= i.state >= 500:
                return 'err'
        return 'ok'

    def info(self):
        r = []
        for i in self.items:
            r.append({'url': i.url, 'method': i.method, 'body': i.body, 'state': i.state, 'stats': i.stats})
        return json.dumps(r)

    def do(self):
        print("==================do=====================")

        def on_response(response):
            print('login: ',response.code)
            self.cookie = ';'.join(response.headers.get_list('Set-Cookie'))
            for j in self.items:
                self.fetch(j)

        if self.auth:
            if self.auth_method == 'post':
                a = httpclient.HTTPRequest(self.auth_url, method=self.auth_method.upper(),
                                           body=urllib.parse.urlencode(self.auth_body))
            elif self.auth_method == 'get':
                a = httpclient.HTTPRequest(self.auth_url)
            httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
            http_client = httpclient.AsyncHTTPClient()
            try:
                http_client.fetch(a, on_response)
            except httpclient.HTTPError as e:
                print("Error: " + str(e))
            except Exception as e:
                print("Error: " + str(e))

        else:
            for i in self.items:
                self.fetch(i)

    # @staticmethod
    def fetch(self, i):
        def on_response(response):
            print(response.body)
            if response.code:
                i.state = response.code
                if 500 <= response.code <= 599:
                    i.stats += 1
            else:
                i.state = 0
	
        print(self.cookie)
        if i.method == 'get':

            req = httpclient.HTTPRequest(i.url, headers={
                "cookie": self.cookie})
            #创建AsyncHTTPClient前先如此声明，可以避免DNS阻塞
            httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
            #AsyncHTTPClient异步客户端，避免请求阻塞
            http_client = httpclient.AsyncHTTPClient()

            try:
                http_client.fetch(req, on_response)

            finally:
                # http_client.close()
                pass

        elif i.method == 'post':
            #body = ''
            #for l in i.body:
            #    print(l)
            #    body += (l['key'] + '=' + l['value'] + '&')
            print(i.body)	
            req = httpclient.HTTPRequest(i.url, headers={
                "cookie": self.cookie}, method='POST', body=urllib.parse.urlencode(i.body))
            http_client = httpclient.AsyncHTTPClient()
            try:
                http_client.fetch(req, on_response)
            finally:
                # http_client.close()
                pass


class RequestUrl(object):
    def __init__(self, item):
        self.state = 0
        self.stats = 0
        self.url = item['url']
        self.method = item['method']
        self.body = {}
        if self.method == 'post':
            for i in item['body']:
                self.body[i['key']] = i['value']


class Monitor(object):
    def __init__(self):
        # self.db = pickle.load('data', False)
        try:
            with open('data', 'rb') as f:
                self.data = pickle.load(f)
            self.tasks_list = self.data['task_list']
            self.tasks = {}
            for i in self.data['task_list']:
                print(i, self.data['task_json'][i])
                self.reload(i, self.data['task_json'][i])
        except Exception as e:
            print(e)
            self.tasks_list = []
            self.tasks = {}
            self.data = {'task_list': self.tasks_list,
                         'task_json': {}}
            with open('data', 'wb') as f:
                pickle.dump(self.data, f)
        self.__start_all__()

    def __start__(self, name):
        pass

    def __stop__(self, name):
        pass

    def __restart__(self, name):
        pass

    def __start_all__(self):
        pass

    def __stop_all__(self):
        pass

    def __restart_all__(self):
        pass

    def delete(self, task):
        self.tasks[task].stop()
        self.tasks.pop(task)
        self.tasks_list.remove(task)

        self.data['task_json'].pop(task)
        with open('data', 'wb') as f:
            pickle.dump(self.data, f)

    def list(self):
        l = []
        for i in self.tasks_list:
            l.append({"hash": i,
                      "name": self.tasks[i].project})
        return json.dumps(l)
        pass

    def get(self, task):
        if task in self.tasks_list:
            return self.tasks[task].json_data
        else:
            return ''

        pass

    def add(self, data):
        data = json.loads(data)

        jsonschema.validate(data, Task.schema, format_checker=jsonschema.FormatChecker())
        task = Task(data)
        # print(task)
        t = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.tasks[t] = task
        self.tasks_list.append(t)

        print(type(self.tasks[t].json_data))
        self.data['task_json'][t] = self.tasks[t].json_data
        print(self.data)
        with open('data', 'wb') as f:
            pickle.dump(self.data, f)

    def update(self, task, data):
        data = json.loads(data)
        self.tasks[task].stop()
        self.tasks[task] = Task(data)

        self.data['task_json'][task] = self.tasks[task].json_data
        with open('data', 'wb') as f:
            pickle.dump(self.data, f)

    def reload(self, task, data):
        data = json.loads(data)
        self.tasks[task] = Task(data)

    def report_whole(self, task):
        return self.tasks[task].result()

    def report_has_err(self, task):
        return self.tasks[task].has_5()

    def report_list_info(self, task):
        return self.tasks[task].info()


monitor = Monitor()


# from tornado import httpclient
#
# a = httpclient.HTTPRequest("http://10.96.2.198/agtlysxx/pubmodule/j_security_check", method="POST",
#                            body="j_username=101000&j_password=1111")
#
# http_client = httpclient.HTTPClient()
# try:
#     response = http_client.fetch(a)
#     print(response.body.decode("utf-8"))
#     print(response.code)
#     print(response.headers)
#
# except httpclient.HTTPError as e:
#     # HTTPError is raised for non-200 responses; the response
#     # can be found in e.response.
#     print("Error: " + str(e))
# except Exception as e:
#     # Other errors are possible, such as IOError.
#     print("Error: " + str(e))
#
# # http_client = httpclient.HTTPClient()
# req = httpclient.HTTPRequest("http://10.96.2.198/agtlysxx/ztc.do", headers={
#     "cookie": "JSESSIONID=hT2bh6Fht25Zr9GLnlLrT50G6GnxnhQLQ8tpSF3vtRn1xZ0mmGnW!1249720348"})
# response = http_client.fetch(req)
# print(response.body.decode("utf-8"))
# print(response.reason, response.code)
# print(response.headers)
# print(response.effective_url)
# http_client.close()
