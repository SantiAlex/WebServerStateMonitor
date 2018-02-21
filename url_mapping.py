# coding=utf-8

from controller import test
from controller.api import ticketTemplate


# url映射
handlers =[
    (r"/", test.IndexHandler),
    (r"/api", test.ApiHandler),
    (r"/search", test.SearchHandler),
    (r"/api/ticket", ticketTemplate.add),
    (r"/api/tickets", ticketTemplate.list),
    (r"/api/inputtypes", ticketTemplate.inputTypes),
    (r"/validate", test.JsonValidate),
    (r"/ip", test.IPHandler),
]

