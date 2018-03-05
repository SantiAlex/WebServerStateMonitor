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
                            'method': {
                                'type': 'string',
                                'enum': ['get'],
                            },
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
    'project': '@www.a你啊哈达哦sd||\\++!@#!@#>><<><>>>>,.,....,1.25151229879310930-'
}
validate(json, schema, format_checker=FormatChecker())
print(isinstance('asd', str))

validate("-12", {"format": "date-time"}, format_checker=FormatChecker(), )
