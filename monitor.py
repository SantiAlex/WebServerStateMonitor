import pickledb
from tornado import httpclient

class Monitor(object):
    def __init__(self):
        self.db = pickledb.load('data', False)
        # self.db.dump()

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

    def write(self, json):
        if validate(json):
            if self.db.get(json.key):
                self.__stop__(json.key)

            self.db.set(json.key, json.value)
            self.db.dump()
            self.__start__(json.key)
            return True

        return False

    def delete(self, name):
        if self.db.get(name):
            self.__stop__(name)
            self.db.rem(name)
            self.db.dump()
        pass

    def list(self):
        return self.db.dgetall()
        pass

    def __client__(self,request):
        
        pass

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