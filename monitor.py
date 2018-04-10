import pickledb
import jsonschema
import json
import time, hashlib
from tornado import httpclient


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
                self.auth_body = []
                if self.auth_method == 'post':
                    for i in self.auth['body']:
                        self.auth_body.append({i['key']: i['value']})
            self.items = []
            for i in self.structured_data.get('items'):
                self.items.append(RequestUrl(i))
            self.interval = self.structured_data['interval']

            self.is_running = True
        except Exception as e:
            print(e)
        pass

    def start(self):
        pass


class RequestUrl(object):
    def __init__(self, item):
        self.url = item['url']
        self.method = item['method']
        self.body = []
        if self.method == 'post':
            for i in item['body']:
                self.body.append({i['key']: i['value']})


class Monitor(object):
    def __init__(self):
        self.db = pickledb.load('data', False)
        # self.db.dump()
        self.tasks_list = []
        self.tasks = {}
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
        self.tasks.pop(task)
        self.tasks_list.remove(task)
        pass

    def list(self):
        l = []
        for i in self.tasks_list:
            print(i)
            print(self.tasks)
            print(self.tasks[i])
            l.append({"hash": i,
                      "name": self.tasks[i].project})
        return (json.dumps(l))
        pass

    def get(self, task):
        return self.tasks[task].json_data

        pass

    def add(self, data):
        data = json.loads(data)
        
        jsonschema.validate(data, Task.schema, format_checker=jsonschema.FormatChecker())
        task = Task(data)

        t = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.tasks[t] = task
        self.tasks_list.append(t)


    def update(self, task, data):
        self.tasks[task] = Task(data)


monitor = Monitor()

'''
from tornado import httpclient

a = httpclient.HTTPRequest("http://10.96.2.198/agtlysxx/pubmodule/j_security_check", method="POST",
                           body="j_username=101000&j_password=1111")

http_client = httpclient.HTTPClient()
try:
    response = http_client.fetch(a)
    print(response.body.decode("utf-8"))
    print(response.code)
    print(response.headers)

except httpclient.HTTPError as e:
    # HTTPError is raised for non-200 responses; the response
    # can be found in e.response.
    print("Error: " + str(e))
except Exception as e:
    # Other errors are possible, such as IOError.
    print("Error: " + str(e))

# http_client = httpclient.HTTPClient()
req = httpclient.HTTPRequest("http://10.96.2.198/agtlysxx/ztc.do", headers={
    "cookie": "JSESSIONID=hT2bh6Fht25Zr9GLnlLrT50G6GnxnhQLQ8tpSF3vtRn1xZ0mmGnW!1249720348"})
response = http_client.fetch(req)
print(response.body.decode("utf-8"))
print(response.reason, response.code)
print(response.headers)
print(response.effective_url)
http_client.close()
'''
