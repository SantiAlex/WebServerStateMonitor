import jsonschema
from jsonschema import *

schema = {
    'type': 'object',
    'required': ['project'],
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

        }

    }
}

json = {
    'project': '12312412@qqc.c',
    'auth': {
        'url': 'http://1.1.1.1',
        'method': 'get',
    },
}
validate(json, schema, format_checker=FormatChecker())
# print(isinstance('asd', str))

# validate("-12", {"format": "date-time"}, format_checker=FormatChecker(), )
