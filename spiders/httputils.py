from aiohttp_requests import requests
import requests as reqs
async def get(url, param=None): 

    while(True):
        try:
            response = await requests.get(url)
            ret = await response.text()
            return ret
        except Exception as e:
            print('error request %s, retrying'% url)
    

async def post(url, data=None): 
    while(True):
        try:
            response = await requests.post(url, data=data)
            ret = await response.text()
            return ret
        except Exception as e:
            print('error request %s, retrying'% url)

async def image(url):
    # lazy way ...
    while(True):
        try:
            response = reqs.get(url)
            return response.content
        except Exception as e:
            print(e)
            pass
    