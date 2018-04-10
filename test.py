import jsonschema
from jsonschema import *
import monitor

schema = {
    'type': 'object',
    'required': ['project', 'item'],
    "additionalProperties": False,
    'properties': {
        'project': {
            'type': 'string',
            'format': 'email',
            'pattern': '^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',
        },
        'auth': {
            # 'type': 'object',
            'oneOf': [
                {
                    'type': 'object',
                    'required': ['url', 'method'],
                    'properties': {
                        'url': {
                            'type': 'string',
                            'format': 'uri',
                            # 'pattern': '/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/',
                        },
                        'method': {
                            'type': 'string',
                            'enum': ['get', 'aaa'],

                        },
                    },
                },
                {
                    'type': 'object',
                    'required': ['url', 'method', 'body'],
                    'properties': {
                        'url': {'type': 'string'},
                        'method': {'type': 'string',
                                   'enum': ['post'],
                                   },
                        'body': {
                            'type': 'object',
                            'properties': {
                                'key': {'type': 'string'},
                                'value': {'type': 'string'},
                            },
                        }
                    },
                },
            ]

        },
        'item': {
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

    }
}

json = {
    'project': '231你好2412@qqc.c',
    'auth': {
        'url': 'https://1.1.1.1',
        'method': 'get',
    },
    'item': [
        {'url': 'https://1.1.1.1',
         'method': 'get', },
        {'url': 'https://1.1.1.1',
         'method': 'post',
         'body': [{'1key': 'sad', 'value': 'sda'}, {'key': 'sad', 'value': 'sda'}]}
    ]
}
json = {"project": "123123",
        "is_running": True,
        "auth": {"method": "post",
                 "url": "http://1.1.1.1",
                 "body": [{"key": "a", "value": "2"}]
                 },
        "items": [{"url": "http://123.1.1.12", "method": "get"}],
        "interval": 5
        }
try:
    validate(json, monitor.Task.schema, format_checker=FormatChecker())
except Exception as e:
    print(e)
# print(isinstance('asd', str))

# validate("-12", {"format": "date-time"}, format_checker=FormatChecker(), )
